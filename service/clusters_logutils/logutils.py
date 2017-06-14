""" Capture request info and logs it.

    Logs all requests with log level info. If request take longer than
    REQUEST_TIME_THRESHOLD, log level warningis used.
    
    Based on: https://github.com/jsmits/django-logutils
"""
import time
# import logging
from functools import wraps, partial
import inspect

import logging.config

from django.db import connection
from django.conf import settings

# from clusters_logutils.settings import LOGGING
from .settings import  LOGGING
settings.LOGGING_CONFIG = None

LOGUTILS_MIDDLEWARE_EVENT = "logutils-event"
LOGUTILS_REQUEST_TIME_THRESHOLD = 100.0 # ms
LOGUTILS_MIDDLEWARE_FORMAT = None

LOGUTILS_LOGGED_EVENT = "logutils-logged"
LOGUTILS_LOGGED_FORMAT = None

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('clusters_logutils.logutils')

def get_log_dict(request, response):
    """
    Create a dictionary with logging data.
    """
    log_dict = {}
    # log_dict['event'] = LOGUTILS_MIDDLEWARE_EVENT

    # ip address
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
        remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
    log_dict['remote_address'] = remote_addr
    
    # email address of login user
    user_email = "-"
    if hasattr(request, 'user'):
        user_email = getattr(request.user, 'email', '-')
    log_dict['user_email'] = user_email
    
    # content length
    if response.streaming:
        content_length = 'streaming'
    else:
        content_length = len(response.content)
    log_dict['content_length'] = content_length
    
    log_dict['method'] = request.method
    log_dict['url'] = request.get_full_path()
    log_dict['status'] = response.status_code
           
    # sql information
    sql_time = sum(float(q['time']) for q in connection.queries) * 1000
    log_dict['nr_queries'] = len(connection.queries) # SQL queries
    log_dict['sql_time'] = sql_time # ms
        
    return log_dict
  
def format_log_message(log_dict, log_format=None):
    """ Create the logging message string.
    
    """
    if log_format is None:
        log_format = (
            "{remote_address} {user_email} {method} {url} {status} "
            "{content_length} ({request_time:.2f} seconds)"
        )
    
    return log_format.format(**log_dict)

class LogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_time = None
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.start_time = time.time()
        
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        try:
            log_dict = get_log_dict(request, response)
            log_dict['event'] = LOGUTILS_MIDDLEWARE_EVENT
            # add the request time to the log_dict; if no start time is
            # available, use -1 as NA value
            request_time = (
                time.time() - self.start_time if hasattr(self, 'start_time')
                and self.start_time else -1)
            log_dict.update({'request_time': request_time})

            is_request_time_too_high = (
                request_time > float(LOGUTILS_REQUEST_TIME_THRESHOLD))

            log_msg = format_log_message(log_dict, LOGUTILS_MIDDLEWARE_FORMAT)

            if is_request_time_too_high:
                logger.warning(log_msg, extra=log_dict)
            else:
                logger.warning(log_msg, extra=log_dict)
                
        except Exception as e:
            logger.exception(e)
            
        return response

# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    
    setattr(obj, func.__name__, func)
    return func

def view_logged(func=None, *, level=logging.DEBUG, module=None, view=None):
    '''Add django view logging to a function.
    @param level: level is the logging level;
    @param module: module is the logger name, 
                   if not set, default valuse is the function's module.
    @param view: view is the function name,
                 if not set, default valuse is the function's name. 
    
    example:
        @view_logged(logging.DEBUG)
        def hello(name, message):
            return message + name
            
        hello.set_message('First time.')
        
        @view_logged(level=logging.WARNING, name='CheckView')
        def get(self, request, *args, **kwargs):
            template_name = 'sclog/check.html'
            result = {}
            return render(request, template_name, result)
    '''
    def decorate(func):
        if func is None:
            return partial(view_logged, level=level, module=module, view=view)
        
        logname = module if module else func.__module__
        log = logging.getLogger(logname)
        logview = view if view else func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_args = inspect.getcallargs(func, *args, **kwargs)
            # request, reponse
            request = func_args.get('request', None)
            
            start_time = time.time()
            response = func(*args, **kwargs)
            request_time = (time.time() - start_time)
            
            log_dict = get_log_dict(request, response)
            log_dict.update({'request_time': request_time})
            log_dict['event'] = LOGUTILS_LOGGED_EVENT
            logmsg = '{} '.format(logview)
            logmsg = logmsg + format_log_message(log_dict, LOGUTILS_LOGGED_FORMAT)
            log.log(level, logmsg)
            
            return response
    
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel
            
        @attach_wrapper(wrapper)
        def set_message(newview):
            nonlocal logview
            logview = newview
        
        return wrapper
        
    return decorate  


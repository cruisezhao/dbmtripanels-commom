"""self define middleware"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import \
    (get_user_model,get_user,load_backend,constant_time_compare,REDIRECT_FIELD_NAME, \
    _get_user_session_key,
     HASH_SESSION_KEY,BACKEND_SESSION_KEY,SESSION_KEY,login)
User = get_user_model()
from django.conf import settings

from rest_framework_jwt.utils import jwt_decode_handler
from jwt import DecodeError,ExpiredSignatureError

def get_cache_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = get_user(request)
    return request._cached_user

def get_user(request):
    """
    Returns the user model instance associated with the given request session.
    If no user is retrieved an instance of `AnonymousUser` is returned.
    """
    user = None
    try:
        payload = jwt_decode_handler(request.token)
        user_id = payload.get('user_id',None)
    except (DecodeError, ExpiredSignatureError):
         return AnonymousUser()
    try:
        backend_path = request.session[BACKEND_SESSION_KEY]
        user_id_in_session = _get_user_session_key(request)
    except KeyError:
        user = User.objects.get(pk = user_id)
        login(request,user)
        backend_path = request.session[BACKEND_SESSION_KEY]
    else:
        if user_id_in_session != user_id:
            user = User.objects.get(pk = user_id)
            login(request,user)
            backend_path = request.session[BACKEND_SESSION_KEY]
            
    if backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        user = backend.get_user(user_id)
        # Verify the session
        if hasattr(user, 'get_session_auth_hash'):
            session_hash = request.session.get(HASH_SESSION_KEY)
            session_hash_verified = session_hash and constant_time_compare(
                session_hash,
                user.get_session_auth_hash()
            )
            if not session_hash_verified:
                request.session.flush()
                user = None

    return user or AnonymousUser()

class TokenAuthenticationMiddleware(MiddlewareMixin):
    """token middleware use to authenticate"""
    def process_request(self,request):
        request.token = request.COOKIES.get('token',None)
        request.user = get_cache_user(request)
        
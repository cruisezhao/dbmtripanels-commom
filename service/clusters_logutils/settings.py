"""
 logutils middleware config
"""
import os
import logging

from django.conf import settings

# logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },       
    'handlers': {
        'info_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'info.log'),
        },
        'warnging_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'warning.log'),
            'formatter': 'simple'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(settings.BASE_DIR, 'error.log'),
        },
        'warnging_socket': {
            'level': 'WARNING',
            '()': 'logging.handlers.SocketHandler',
            'host': 'localhost',
            'port': logging.handlers.DEFAULT_TCP_LOGGING_PORT,
        },
    },
    'loggers': {
        'clusters_logutils': {
            'handlers': ['warnging_socket'],
            'level': 'WARNING',
            'propagate': False,
        },
        'clusters_logutils.logutils': {
            'handlers': ['error_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}
"""

from os import path, makedirs
import logging


log_dir = path.join(path.dirname(__file__), 'logs')
if not path.exists(log_dir):
    makedirs(log_dir)


xena_rest_server_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'filename': path.join(log_dir, 'xenavalkyrie_rest.log'),
            'formatter': 'standard',
            'maxBytes': 4194304,
            'mode': 'w+',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': True
        },
    }
}

gunicorn_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'filename': path.join(log_dir, 'gunicorn.log'),
            'formatter': 'standard',
            'maxBytes': 4194304,
            'mode': 'w+',
        },
        'gunicorn.error.file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'filename': path.join(log_dir, 'gunicorn.error.log'),
            'formatter': 'standard',
            'maxBytes': 4194304,
            'mode': 'w+',
        },
        'gunicorn.access.file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'filename': path.join(log_dir, 'gunicorn.access.log'),
            'formatter': 'standard',
            'maxBytes': 4194304,
            'mode': 'w+',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': True
        },
        'gunicorn.error': {
            'handlers': ['console', 'gunicorn.error.file'],
            'level': logging.DEBUG,
            'propagate': True
        },
        'gunicorn.access': {
            'handlers': ['console', 'gunicorn.access.file'],
            'level': logging.DEBUG,
            'propagate': True
        },
    }
}

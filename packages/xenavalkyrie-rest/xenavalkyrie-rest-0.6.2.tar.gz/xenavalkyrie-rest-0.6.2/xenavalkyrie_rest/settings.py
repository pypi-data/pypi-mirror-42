
from xenavalkyrie_rest.logging_dicts import gunicorn_dict

# Gunicorn settings

bind = '0.0.0.0:57911'
workers = 1
logconfig_dict = gunicorn_dict


# Xena rest_server settings.

configs_folder = '/tmp/xena_rest_server_configs'
session_timeout = 360
debug = True

# Flask settings
FLASK_SERVER_NAME = bind
FLASK_DEBUG = True

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_SWAGGER_UI_JSONEDITOR = True

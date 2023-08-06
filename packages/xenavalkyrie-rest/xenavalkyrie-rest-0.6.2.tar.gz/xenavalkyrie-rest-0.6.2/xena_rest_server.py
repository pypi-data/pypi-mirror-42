#!/usr/bin/env python
# encoding: utf-8

# Order matters. This imports actually execute code.

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter


import xenavalkyrie_rest
import xenavalkyrie_rest.settings as settings

# Start logger, app and api
from xenavalkyrie_rest.namespaces.base_ns import logger, app

# Build namespaces.
from xenavalkyrie_rest.namespaces.session_ns import session_ns
from xenavalkyrie_rest.namespaces.chassis_ns import chassis_ns
from xenavalkyrie_rest.namespaces.module_ns import module_ns
from xenavalkyrie_rest.namespaces.port_ns import port_ns
from xenavalkyrie_rest.namespaces.stream_ns import stream_ns
from xenavalkyrie_rest.namespaces.modifier_ns import modifier_ns, xmodifier_ns
from xenavalkyrie_rest.namespaces.capture_ns import capture_ns
from xenavalkyrie_rest.namespaces.server_ns import management_ns


def standalone_server(args=None):

    # Setup argument parser
    parser = ArgumentParser(description='Xena REST server', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=xenavalkyrie_rest.__version__)
    parser.add_argument("-s", "--server", help="server", default=settings.FLASK_SERVER_NAME)

    parsed_args = parser.parse_args(args)

    host, port = parsed_args.server.split(':')

    app.config['DEBUG'] = settings.FLASK_DEBUG

    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    app.config['SWAGGER_UI_JSONEDITOR'] = settings.RESTPLUS_SWAGGER_UI_JSONEDITOR

    logger.info('>>>>> Starting server version {} at http://{}/api/ <<<<<'.
                format(xenavalkyrie_rest.__version__, parsed_args.server))
    app.run(host=host, port=port, debug=xenavalkyrie_rest.settings.FLASK_DEBUG)


if __name__ == "__main__":
    sys.exit(standalone_server((sys.argv[1:])))

"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from os import path, system
from collections import OrderedDict
from io import BytesIO
import zipfile
import logging
from flask import request, send_file
import time

from trafficgenerator.tgn_utils import ApiType, is_true
from xenavalkyrie.xena_object import XenaAttributeError
from xenavalkyrie_rest import __version__
from xenavalkyrie.xena_app import init_xena

import xenavalkyrie_rest.settings as settings
from xenavalkyrie_rest.namespaces.serializers import (management_operation, command_description, route_info,
                                                      default_management_oper, counters_group, out_attribute,
                                                      in_attribute)
from xenavalkyrie_rest.namespaces.base_ns import (api, logger, XenaRestBase, ObjectNotFound, get_sub_routes,
                                                  build_route_info, build_out_attributes, start_time)


management_ns = api.namespace('management', description='Manage Xena Valkyrie REST API server')


@management_ns.route('', endpoint='Manage server')
class XenaRestManagement(XenaRestBase):

    @api.marshal_with(route_info)
    def get(self):
        """
        Returns sub-routes.
        """
        return build_route_info(routes=get_sub_routes(self), objects=[])


@management_ns.route('/attributes', endpoint='REST server management attributes')
class XenaRestManagementAttrs(XenaRestBase):

    @api.marshal_list_with(out_attribute)
    def get(self):
        """
        Returns REST server attributes.
        """
        return build_out_attributes(debug=XenaRestBase.debug,
                                    sessions=' '.join(XenaRestBase.sessions.keys()),
                                    timeout=XenaRestBase.timeout,
                                    version=__version__)

    @api.expect([in_attribute])
    def patch(self):
        """
        Set REST server attributes.
        """

        for name_value in request.json:
            if name_value['name'] == 'debug':
                XenaRestBase.debug = is_true(name_value['value'].lower())
                for handler in logger.handlers:
                    handler.setLevel(logging.DEBUG if XenaRestBase.debug else logging.INFO)
            elif name_value['name'] == 'timeout':
                XenaRestBase.timeout = int(name_value['value'])
            elif name_value['name'] in ['sessions', 'version']:
                raise XenaAttributeError('Attribute {} <NOTWRITABLE>'.format(name_value['name']))
            else:
                raise XenaAttributeError('Attribute {} not found'.format(name_value['name']))


@management_ns.route('/statistics', endpoint='REST server management statistics')
class XenaRestManagementStats(XenaRestBase):

    @api.marshal_list_with(counters_group)
    def get(self):
        """
        Returns REST server statistics.
        """

        counters_groups = [{'name': 'c_reststats',
                            'counters': [{'name': 'num_sessions', 'value': len(XenaRestBase.sessions)},
                                         {'name': 'start_time', 'value': start_time},
                                         {'name': 'current_time', 'value': time.time()}]}]
        return counters_groups


@management_ns.route('/operations', endpoint='REST server management operations')
class XenaRestManagementOpers(XenaRestBase):

    @api.marshal_list_with(command_description)
    def get(self):
        """
        Returns REST management operations list.
        """

        operations = [{'name': 'restart', 'description': 'restart service'}]
        if XenaRestBase.debug:
            operations.extend([{'name': 'reset', 'description': 'remove all sessions'},
                               {'name': 'reserve', 'description': 'reserve list of ports under user'}])
        return operations


@management_ns.route('/operations/<string:oper>', endpoint='REST server management operation')
@api.param('oper', 'Management operation.', type=str, default=default_management_oper)
class XenaRestManagementOper(XenaRestBase):

    @api.expect(management_operation)
    def post(self, oper):
        """
        Performs REST server management operation.
        """

        parameters = request.json.get('parameters', None)
        if oper == 'restart':
            try:
                system('/etc/init.d/xenarestserver restart')
            except Exception as _:
                try:
                    system('systemctl start xenarestserver.service')
                except Exception as _:
                    pass
        elif oper == 'reset':
            XenaRestBase.sessions = OrderedDict()
            XenaRestBase.timeout = settings.session_timeout
            XenaRestBase.debug = settings.debug
        elif oper == 'reserve':
            user = parameters[0]
            if user not in XenaRestBase.sessions:
                XenaRestBase.sessions[user] = init_xena(ApiType.rest, logger, user).session
            for param in request.json['parameters'][1:]:
                XenaRestBase.sessions[user].add_chassis(str(param.split('/')[0]))
                XenaRestBase.sessions[user].reserve_ports([param], force=True, reset=True)
        else:
            raise ObjectNotFound('operation', oper, [oper['name'] for oper in XenaRestManagementOpers().get()])


@management_ns.route('/files', endpoint='REST server management logs')
class XenaRestManagementFiles(XenaRestBase):

    def get(self):
        """
        Returns REST server log files (as zip file).
        """

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zip_file:
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    zip_file.write(handler.baseFilename, path.basename(handler.baseFilename))
        memory_file.seek(0)
        return send_file(memory_file, attachment_filename='logs.zip', as_attachment=True)

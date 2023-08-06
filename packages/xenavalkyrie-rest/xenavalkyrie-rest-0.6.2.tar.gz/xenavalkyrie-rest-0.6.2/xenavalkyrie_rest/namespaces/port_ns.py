"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
import os
from flask import request, send_from_directory
from werkzeug.utils import secure_filename

from xenavalkyrie_rest.settings import configs_folder
from xenavalkyrie_rest.namespaces.base_ns import (api, get_object, perform_command, get_attributes, set_attributes,
                                                  build_route_info, get_sub_routes)
from xenavalkyrie_rest.namespaces.module_ns import module_path, XenaRestModuleBase
from xenavalkyrie_rest.namespaces.serializers import (in_attribute, out_attribute, object_command, route_info,
                                                      counters_group, default_port, command_description,
                                                      default_tpld, upload_parser)

port_path = module_path + '/port/<int:port>'
port_ns = api.namespace('port', path=port_path, description='Manage Xena port')
ports_ns = api.namespace('port', path=module_path + '/port', description='Manage Xena port')


@api.param('port', 'Port index.', type=int, default=default_port)
class XenaRestPortBase(XenaRestModuleBase):
    pass


@api.param('tpld', 'TPLD index.', type=int, default=default_tpld)
class XenaRestTpldBase(XenaRestPortBase):
    pass


@ports_ns.route('', endpoint='Manage ports')
class XenaRestPorts(XenaRestModuleBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module):
        """
        Returns all ports.
        """

        module_obj = get_object(user, chassis=chassis, module=module)
        return build_route_info(routes=get_sub_routes(self), objects=module_obj.ports.keys())


@port_ns.route('', endpoint='Manage port')
class XenaRestPort(XenaRestPortBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module, port):
        """
        Returns port sub-routes list.
        """

        return build_route_info(routes=get_sub_routes(self), objects=[])


@port_ns.route('/attributes', endpoint='Port attributes')
class XenaRestPortAttrs(XenaRestPortBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port):
        """
        Returns port attributes.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        return get_attributes(port_obj)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module, port):
        """
        Set port attributes.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        return set_attributes(port_obj, request)


@port_ns.route('/commands', endpoint='Port commands')
class XenaRestPortCommands(XenaRestPortBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module, port):
        """
        Returns all commands.
        """

        return None, 501


@port_ns.route('/commands/<string:command>', endpoint='Port command')
@api.param('command', 'CLI command name.')
class XenaRestPortCommand(XenaRestPortBase):

    @api.expect(object_command)
    def post(self, user, chassis, module, port, command):
        """
        Performs port command.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        return perform_command(port_obj, request, command)


@port_ns.route('/statistics', endpoint='Port statistics')
class XenaRestPortStats(XenaRestPortBase):

    @api.marshal_list_with(counters_group)
    def get(self, user, chassis, module, port):
        """
        Returns port statistics.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        stats = port_obj.read_port_stats()
        counters_groups = []
        for group, counters in stats.items():
            counters_groups.append({'name': group,
                                    'counters': [{'name': name, 'value': value} for name, value in counters.items()]})
        return counters_groups


@port_ns.route('/files', endpoint='Port configuration files')
class XenaRestPortFiles(XenaRestPortBase):

    @api.response(201, 'File uploaded.')
    @api.expect(upload_parser)
    def post(self, user, chassis, module, port):
        """
        Uploads configuration file (xpc).
        """

        file_obj = request.files['file']
        filename = secure_filename(file_obj.filename)
        if not os.path.exists(configs_folder):
            os.makedirs(configs_folder)
        full_path = os.path.join(configs_folder, filename)
        file_obj.save(full_path)
        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        port_obj.load_config(full_path)
        return None, 201

    def get(self, user, chassis, module, port):
        """
        Returns configuration file (xpc).
        """

        full_path = os.path.join(configs_folder, 'downloaded_config.xpc')
        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        port_obj.save_config(full_path)
        return send_from_directory(configs_folder, 'downloaded_config.xpc', as_attachment=True)


@port_ns.route('/tpld', endpoint='Manage TPLDs')
class XenaRestTplds(XenaRestPortBase):

    @api.marshal_list_with(route_info)
    def get(self, user, chassis, module, port):
        """
        Returns TPLDs.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        return build_route_info(routes=get_sub_routes(self), objects=port_obj.tplds.keys())


@port_ns.route('/tpld/<int:tpld>/commands', endpoint='TPLD commands')
class XenaRestTpldCommands(XenaRestTpldBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module, port, tpld):
        """
        Returns all commands.
        """

        return None, 501


@port_ns.route('/tpld/<int:tpld>/commands/<string:command>', endpoint='TPLD command')
@api.param('command', 'CLI command name.')
class XenaRestTpldCommand(XenaRestTpldBase):

    @api.expect(object_command)
    def post(self, user, chassis, module, port, tpld, command):
        """
        Performs TPLD command.
        """

        tpld_obj = get_object(user, chassis=chassis, module=module, port=port, tpld=tpld)
        return perform_command(tpld_obj, request, command)


@port_ns.route('/tpld/<int:tpld>/statistics', endpoint='TPLD statistics')
class XenaRestTpldStats(XenaRestTpldBase):

    @api.marshal_list_with(counters_group)
    def get(self, user, chassis, module, port, tpld):
        """
        Returns TPLD statistics.
        """

        tpld_obj = get_object(user, chassis=chassis, module=module, port=port, tpld=tpld)
        stats = tpld_obj.read_stats()
        counters_groups = []
        for group, counters in stats.items():
            counters_groups.append({'name': group,
                                    'counters': [{'name': name, 'value': value} for name, value in counters.items()]})
        return counters_groups

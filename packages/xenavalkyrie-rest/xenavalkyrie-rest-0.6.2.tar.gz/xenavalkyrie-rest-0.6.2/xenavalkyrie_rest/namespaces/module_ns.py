"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from flask import request

from xenavalkyrie_rest.namespaces.base_ns import (api, get_object, perform_command, build_route_info, get_sub_routes,
                                                  get_attributes)
from xenavalkyrie_rest.namespaces.chassis_ns import chassis_path, XenaRestChassisBase
from xenavalkyrie_rest.namespaces.serializers import (in_attribute, out_attribute, object_command, route_info,
                                                      default_module, command_description)

module_path = chassis_path + '/module/<int:module>'
module_ns = api.namespace('module', path=module_path, description='Manage Xena module')
modules_ns = api.namespace('module', path=chassis_path + '/module', description='Manage Xena module')


@api.param('module', 'Module index.', type=int, default=default_module)
class XenaRestModuleBase(XenaRestChassisBase):
    pass


@modules_ns.route('', endpoint='Manage modules')
class XenaRestModules(XenaRestChassisBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis):
        """
        Returns all modules.
        """

        chassis_obj = get_object(user, chassis=chassis)
        return build_route_info(routes=get_sub_routes(self), objects=chassis_obj.modules.keys())


@module_ns.route('', endpoint='Manage module')
class XenaRestModule(XenaRestModuleBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module):
        """
        Returns module sub-routes.
        """

        return build_route_info(routes=get_sub_routes(self), objects=[])


@module_ns.route('/attributes', endpoint='Get/Set module attributes')
class XenaRestModuleAttributes(XenaRestModuleBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module):
        """
        Returns module attributes.
        """

        module_obj = get_object(user, chassis=chassis, module=module)
        return get_attributes(module_obj)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module):
        """
        Set module attributes.
        """

        module = get_object(user, chassis=chassis, module=module)
        names_values = {}
        for name_value in request.json:
            names_values[name_value['name']] = name_value['value']
        module.set_attributes(**names_values)
        return None


@module_ns.route('/commands', endpoint='Module commands')
class XenaRestModuleCommands(XenaRestModuleBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module):
        """
        Returns all commands.
        """

        return None, 501


@module_ns.route('/commands/<string:command>', endpoint='Module command')
@api.param('command', 'CLI command name.')
class XenaRestModuleCommand(XenaRestModuleBase):

    @api.expect(object_command)
    def post(self, user, chassis, module, command):
        """
        Performs module command.
        """

        module = get_object(user, chassis=chassis, module=module)
        return perform_command(module, request, command)

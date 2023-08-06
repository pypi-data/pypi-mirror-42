"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from flask import request

from xenavalkyrie_rest.namespaces.serializers import (api, in_attribute, out_attribute, object_command,
                                                      session_route_info, default_chassis, command_description,
                                                      backdoor_command, chassis_parser, route_info)
from xenavalkyrie_rest.namespaces.base_ns import (get_object, perform_command, get_sub_routes, get_attributes,
                                                  CommandReturnType, build_route_info)
from xenavalkyrie_rest.namespaces.session_ns import session_path, XenaRestSessionBase

chassis_path = session_path + '/chassis/<string:chassis>'
chassis_ns = api.namespace('chassis', path=chassis_path, description='Manage Xena chassis')
chassises_ns = api.namespace('chassis', path=session_path + '/chassis', description='Manage Xena chassis')


@api.param('chassis', 'Chassis IP.', default=default_chassis)
class XenaRestChassisBase(XenaRestSessionBase):
    pass


@chassises_ns.route('', endpoint='Manage chassis list')
class XenaRestChassises(XenaRestSessionBase):

    @api.marshal_with(session_route_info)
    def get(self, user):
        """
        Returns chassis list.
        """

        session = get_object(user)
        return {'routes': get_sub_routes(self),
                'chassis': [{'ip': c} for c in session.chassis_list.keys()]}

    @api.response(200, 'Already connected to chassis.')
    @api.response(201, 'Connected to chassis.')
    @api.expect(chassis_parser)
    def post(self, user):
        """
        Add chassis.
        """

        session = get_object(user)
        ip = request.args.get('ip')
        if request.host.split(':')[0] == ip:
            if set(session.chassis_list).intersection(set(['localhost', '127.0.0.1'])):
                return
        port = int(request.args.get('port', 22611))
        password = request.args.get('password', 'xena')
        session.add_chassis(ip, port, password)
        return None, 201


@chassis_ns.route('', endpoint='Manage chassis')
class XenaRestChassis(XenaRestChassisBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis):
        """
        Returns chassis sub-routes list.
        """

        return build_route_info(routes=get_sub_routes(self), objects=[])


@chassis_ns.route('/attributes', endpoint='Chassis attributes')
class XenaRestChassisAttributes(XenaRestChassisBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis):
        """
        Returns chassis attributes.
        """

        chassis_obj = get_object(user, chassis=chassis)
        return get_attributes(chassis_obj)

    @api.expect([in_attribute])
    def patch(self, user, chassis):
        """
        Sets chassis attributes.
        """

        chassis_obj = get_object(user, chassis=chassis)
        names_values = {}
        for name_value in request.json:
            names_values[name_value['name']] = name_value['value']
        chassis_obj.set_attributes(**names_values)
        return None


@chassis_ns.route('/statistics', endpoint='Chassis statistics')
class XenaRestChassisStats(XenaRestChassisBase):

    def get(self, user, chassis):
        """
        Returns chassis statistics.
        """

        chassis_obj = get_object(user, chassis=chassis)
        return None, 501


@chassis_ns.route('/commands', endpoint='Chassis commands')
class XenaRestChassisCommands(XenaRestChassisBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis):
        """
        Returns all commands.
        """

        return None, 501


@chassis_ns.route('/commands/<string:command>', endpoint='Chassis command')
@api.param('command', 'CLI command name.')
class XenaRestChassisCommand(XenaRestChassisBase):

    @api.expect(object_command)
    def post(self, user, chassis, command):
        """
        Performs chassis command.
        """

        chassis_obj = get_object(user, chassis=chassis)
        return perform_command(chassis_obj, request, command)


@chassis_ns.route('/backdoor', endpoint='Chassis back-door to execute any CLI command')
class XenaRestChassisBackdoor(XenaRestChassisBase):

    @api.expect(backdoor_command)
    def post(self, user, chassis):
        """
        Performs ANY native CLI command.
        """

        chassis_obj = get_object(user, chassis=chassis)
        if request.json['return_type'] == CommandReturnType.no_output.value:
            return chassis_obj.api.send_command(chassis_obj, request.json['command'])
        elif request.json['return_type'] == CommandReturnType.line_output.value:
            return chassis_obj.api.send_command_return(chassis_obj, request.json['command'])
        else:
            return chassis_obj.api.send_command_return_multilines(chassis_obj, request.json['command'])

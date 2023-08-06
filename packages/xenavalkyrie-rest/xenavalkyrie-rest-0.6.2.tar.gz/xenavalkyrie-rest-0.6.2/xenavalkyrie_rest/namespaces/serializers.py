
from flask_restplus import fields, reqparse
from werkzeug.datastructures import FileStorage

from xenavalkyrie_rest.namespaces.base_ns import api, CommandReturnType

# To speed testing with swagger API we set the following defaults. Should be emptied before release.
default_user = ''
default_chassis = 'localhost'
default_module = 0
default_port = 0
default_port_2 = 1
# For some reason, if default==0 swagger UI shows empty field, maybe due to 'if not None' condition somewhere...
default_stream = '0'
default_packet = '0'
default_tpld = '0'
default_management_oper = 'reserve'


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

session_parser = reqparse.RequestParser()
session_parser.add_argument('user', type=str, required=True, help='User name', default=default_user)

chassis_parser = reqparse.RequestParser()
chassis_parser.add_argument('ip', type=str, required=True, help='Chassis IP.', default=default_chassis)
chassis_parser.add_argument('port', type=int, required=False, help='Chassis TCP port.', default=22611)
chassis_parser.add_argument('password', type=str, required=False, help='Chassis password', default='xena')

session = api.model('Automation session', {
    'user': fields.String(required=True, description='User name')
})

xena_object = api.model('Xena object', {
    'id': fields.Integer(required=True, description='Object index')
})

chassis = api.model('Xena chassis', {
    'ip': fields.String(required=True, description='Chassis IP address.'),
    'port': fields.Integer(description='Chassis TCP port.'),
    'password': fields.String(description='Chassis password.'),
})

out_attribute = api.model('Object attribute details', {
    'name': fields.String(required=True, description='Attribute name.'),
    'value': fields.String(required=True, description='Attribute value.'),
    'description': fields.String(description='Object description.'),
})

in_attribute = api.model('Object attribute', {
    'name': fields.String(required=True, description='Attribute name.'),
    'value': fields.String(required=True, description='Attribute value.'),
})

ep_info = api.model('Endpoint info', {
    'name': fields.String(required=True, description='Endpoint name.'),
    'description': fields.String(required=False, description='Endpoint description.'),
})

xena_object = api.model('Xena object', {
    'id': fields.Integer(required=True, description='Object index used in CLI commands.'),
    'name': fields.String(required=False, description='Object name/description if available.'),
})

command_description = api.model('Xena command', {
    'name': fields.String(required=True, description='Command name.'),
    'description': fields.String(required=False, description='Command description.'),
    'parameters': fields.String(required=False, description='Command parameters description.'),
})

backdoor_command = api.model('Backdoor Command', {
    'return_type': fields.String(required=True, description='Return type.', enum=CommandReturnType._member_names_,
                                 default=CommandReturnType.no_output.value),
    'command': fields.String(required=True, description='Native Xena CLI command to send over socket as is.')
})

object_command = api.model('Object Command', {
    'return_type': fields.String(required=True, description='Return type.', enum=CommandReturnType._member_names_,
                                 default=CommandReturnType.no_output.value),
    'parameters': fields.List(fields.String, required=True, description='List of parameters.'),
})

management_operation = api.model('Server management operation', {
    'parameters': fields.List(fields.String, required=False, description='List of parameters.',
                              example=[default_user,
                                       '{}/{}/{}'.format(default_chassis, default_module, default_port),
                                       '{}/{}/{}'.format(default_chassis, default_module, default_port_2)]),
})

server_route_info = api.model('Server route information', {
    'routes': fields.List(fields.String, required=True, description='List of sub-routes.'),
    'sessions': fields.List(fields.Nested(session), required=True, description='List of users.'),
})

session_route_info = api.model('Session route information', {
    'routes': fields.List(fields.String, required=True, description='List of sub-routes.'),
    'chassis': fields.List(fields.Nested(chassis), required=True, description='List of Xena chassis.'),
})

route_info = api.model('Route information', {
    'routes': fields.List(fields.Nested(ep_info), required=False, description='List of sub-routes.'),
    'objects': fields.List(fields.Nested(xena_object), required=False, description='List of Xena object children.'),
})

counter = api.model('Statistics counter', {
    'name': fields.String(required=True, description='Counter name.'),
    'value': fields.Integer(required=True, description='Counter value.'),
})

counters_group = api.model('Group of statistics counters', {
    'name': fields.String(required=True, description='Group name.'),
    'counters': fields.List(fields.Nested(counter), required=True, description='List of statistics counters.'),
})

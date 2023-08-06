"""
@author yoram@ignissoft.com
"""

import logging.config
from enum import Enum
from collections import OrderedDict
import socket
import time
from flask import Flask, request
from flask_restplus import Api, errors, Resource
from werkzeug.contrib.fixers import ProxyFix

from xenavalkyrie.api.xena_socket import XenaCommandError
from xenavalkyrie.xena_object import XenaAttributeError

from xenavalkyrie_rest.logging_dicts import xena_rest_server_dict
import xenavalkyrie_rest.settings as settings


def before_request():
    if not request.view_args:
        return
    user = request.view_args.get('user', None)
    if user in XenaRestBase.sessions:
        XenaRestBase.sessions[user].timestamp = time.time()
    for user in XenaRestBase.sessions:
        if time.time() - XenaRestBase.sessions[user].timestamp > XenaRestBase.timeout:
            logger.info('Session {} timeout'.format(user))
            XenaRestBase.sessions[user].disconnect()
            del XenaRestBase.sessions[user]
            logger.info('Session {} deleted'.format(user))


logging.config.dictConfig(xena_rest_server_dict)
logger = logging.getLogger()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Xena Valkyrie REST API', description='Xena Valkyrie REST API')


app.before_request(before_request)

start_time = time.time()


class ObjectNotFound(errors.RestError):
    def __init__(self, obj_type, obj_name, available_objects):
        message = '{} {} not found, available {}s: {}'.format(obj_type, obj_name, obj_type, available_objects)
        super(ObjectNotFound, self).__init__(message)

    def __repr__(self):
        return self.__str__()


@api.errorhandler(Exception)
@api.errorhandler(KeyError)
@api.errorhandler(ValueError)
@api.errorhandler(IOError)
@api.errorhandler(OSError)
@api.errorhandler(TypeError)
@api.errorhandler(AttributeError)
@api.errorhandler(socket.error)
@api.errorhandler(XenaCommandError)
@api.errorhandler(XenaAttributeError)
@api.errorhandler(ObjectNotFound)
def application_exception(error):
    error_code = 404 if type(error) is ObjectNotFound else 500
    logger.warning(repr(error))
    return {'message': repr(error)}, error_code


class XenaRestBase(Resource):
    sessions = OrderedDict()
    debug = settings.debug
    timeout = settings.session_timeout


class CommandReturnType(Enum):
    no_output = 'no_output'
    line_output = 'line_output'
    multiline_output = 'multiline_output'


def get_object(user, **path):
    if user not in XenaRestBase.sessions:
        raise ObjectNotFound('session', user, XenaRestBase.sessions.keys())
    xena_object = XenaRestBase.sessions[user]
    if 'chassis' in path:
        localhost_addresses = ['localhost', '127.0.0.1', request.host.split(':')[0]]
        chassis = localhost_addresses if path['chassis'] in localhost_addresses else [path['chassis']]
        chassis_name_in_list = set(xena_object.chassis_list).intersection(chassis)
        if not chassis_name_in_list:
            raise ObjectNotFound('chassis', path['chassis'], xena_object.chassis_list.keys())
        xena_object = xena_object.chassis_list[list(chassis_name_in_list)[0]]
    if 'module' in path:
        if path['module'] not in xena_object.modules:
            raise ObjectNotFound('module', path['module'], xena_object.modules.keys())
        xena_object = xena_object.modules[path['module']]
    if 'port' in path:
        if path['port'] not in xena_object.ports:
            raise ObjectNotFound('port', path['port'], xena_object.ports.keys())
        xena_object = xena_object.ports[path['port']]
    if 'stream' in path:
        if path['stream'] not in xena_object.streams:
            raise ObjectNotFound('stream', path['stream'], xena_object.streams.keys())
        xena_object = xena_object.streams[path['stream']]
    if 'modifier' in path:
        if path['modifier'] not in xena_object.modifiers:
            raise ObjectNotFound('modifier', path['modifier'], xena_object.modifiers.keys())
        xena_object = xena_object.modifiers[path['modifier']]
    if 'xmodifier' in path:
        if path['xmodifier'] not in xena_object.xmodifiers:
            raise ObjectNotFound('xmodifier', path['xmodifier'], xena_object.xmodifiers.keys())
        xena_object = xena_object.xmodifiers[path['xmodifier']]
    if 'tpld' in path:
        if path['tpld'] not in xena_object.tplds:
            raise ObjectNotFound('tpld', path['tpld'], xena_object.tplds.keys())
        xena_object = xena_object.tplds[path['tpld']]
    if 'packet' in path:
        if path['packet'] not in xena_object.capture.packets:
            raise ObjectNotFound('packet', path['packet'], xena_object.capture.packets.keys())
        xena_object = xena_object.capture.packets[path['packet']]
    return xena_object


def perform_command(xena_object, request, command):
    parameters = ' '.join(request.json['parameters']).strip()
    if request.json['return_type'] == CommandReturnType.no_output.value:
        return xena_object.send_command(command, parameters)
    elif request.json['return_type'] == CommandReturnType.line_output.value:
        return xena_object.send_command_return(command, parameters)
    else:
        return xena_object.send_command_return_multilines(command, parameters)


def get_attributes(xena_object):
    return build_out_attributes(**xena_object.get_attributes())


def build_out_attributes(**attributes):
    return [{'name': name, 'value': value} for name, value in attributes.items()]


def set_attributes(xena_object, request):
    names_values = {}
    for name_value in request.json:
        names_values[name_value['name']] = name_value['value']
    xena_object.set_attributes(**names_values)


def build_route_info(routes, objects):
    route_info = {}
    route_info['routes'] = routes
    route_info['objects'] = [{'id': o} for o in objects]
    return route_info


def get_sub_routes(route):
    route_rule = app.url_map._rules_by_endpoint[route.endpoint][0].rule
    route_rule_len = len(route_rule.split('/'))
    rules = {}
    for rule in app.url_map._rules:
        if route_rule in rule.rule:
            rule_len = len(rule.rule.split('/'))
            if rule_len > route_rule_len:
                if ':' not in rule.rule.split('/')[route_rule_len]:
                    rules[rule.rule.split('/')[route_rule_len]] = rule.endpoint
    return [{'name': k, 'description': v} for k, v in rules.items()]

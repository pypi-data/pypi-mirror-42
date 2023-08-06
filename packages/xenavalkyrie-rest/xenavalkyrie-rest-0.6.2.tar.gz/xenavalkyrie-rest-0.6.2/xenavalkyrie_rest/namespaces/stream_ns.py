"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from flask import request

from xenavalkyrie.xena_stream import XenaStreamState

from xenavalkyrie_rest.namespaces.base_ns import (api, get_object, perform_command, get_attributes, set_attributes,
                                                  build_route_info, get_sub_routes)
from xenavalkyrie_rest.namespaces.port_ns import port_path, XenaRestPortBase
from xenavalkyrie_rest.namespaces.serializers import (in_attribute, out_attribute, object_command, xena_object,
                                                      route_info, default_stream, counters_group, command_description)

stream_path = port_path + '/stream/<int:stream>'
stream_ns = api.namespace('stream', path=stream_path, description='Manage Xena stream')
streams_ns = api.namespace('stream', path=port_path + '/stream', description='Manage Xena stream')


@streams_ns.route('', endpoint='Manage streams')
class XenaRestStreams(XenaRestPortBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module, port):
        """
        Returns all streams.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        return build_route_info(routes=get_sub_routes(self), objects=port_obj.streams.keys())

    @api.response(201, 'Stream created.')
    @api.marshal_with(xena_object)
    def post(self, user, chassis, module, port):
        """
        Add stream.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        stream_obj = port_obj.add_stream(name='', state=XenaStreamState.disabled)
        return {'id': stream_obj.id}, 201


@api.param('stream', 'Stream index.', type=int, default=default_stream)
class XenaRestStreamBase(XenaRestPortBase):
    pass


@stream_ns.route('', endpoint='Manage stream')
class XenaRestStream(XenaRestStreamBase):

    @api.marshal_list_with(route_info)
    def get(self, user, chassis, module, port, stream):
        """
        Returns sub-routes list.
        """

        return build_route_info(routes=get_sub_routes(self), objects=[])

    @api.response(204, 'Stream removed.')
    def delete(self, user, chassis, module, port, stream):
        """
        Remove stream.
        """

        port_obj = get_object(user, chassis=chassis, module=module, port=port)
        port_obj.remove_stream(stream)
        return None, 204


@stream_ns.route('/attributes', endpoint='Stream attributes')
class XenaRestStreamAttrs(XenaRestStreamBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port, stream):
        """
        Returns stream attributes.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        return get_attributes(stream_obj)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module, port, stream):
        """
        Set stream attributes.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        return set_attributes(stream_obj, request)


@stream_ns.route('/commands', endpoint='Stream commands')
class XenaRestStreamCommands(XenaRestStreamBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module, port, stream):
        """
        Returns all commands.
        """

        return None, 501


@stream_ns.route('/commands/<string:command>', endpoint='Stream command')
@api.param('command', 'CLI command name.')
class XenaRestStreamCommand(XenaRestStreamBase):

    @api.expect(object_command)
    def post(self, user, chassis, module, port, stream, command):
        """
        Performs stream command.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        return perform_command(stream_obj, request, command)


@stream_ns.route('/statistics', endpoint='Stream statistics')
class XenaRestStreamStats(XenaRestStreamBase):

    @api.marshal_list_with(counters_group)
    def get(self, user, chassis, module, port, stream):
        """
        Returns stream statistics.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        stats = stream_obj.read_stats()
        counters_groups = [{'name': 'pt_stream',
                            'counters': [{'name': name, 'value': value} for name, value in stats.items()]}]
        return counters_groups

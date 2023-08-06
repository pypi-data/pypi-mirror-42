"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from flask import request

from xenavalkyrie_rest.namespaces.base_ns import (api, get_object, perform_command, get_attributes, set_attributes,
                                                  build_route_info, get_sub_routes)
from xenavalkyrie_rest.namespaces.port_ns import port_path, XenaRestPortBase
from xenavalkyrie_rest.namespaces.serializers import (in_attribute, out_attribute, route_info,
                                                      counters_group, default_packet, command_description)

capture_path = port_path + '/capture'
capture_ns = api.namespace('capture', path=capture_path, description='Manage Xena capture buffer')


@api.param('packet', 'Packet index.', type=int, default=default_packet)
class XenaRestCaptureBase(XenaRestPortBase):
    pass


@capture_ns.route('', endpoint='Manage capture buffer')
class XenaRestCapture(XenaRestPortBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module, port):
        """
        Returns sub-routes and packets list.
        """

        capture_obj = get_object(user, chassis=chassis, module=module, port=port).capture
        return build_route_info(routes=get_sub_routes(self), objects=capture_obj.packets.keys())


@capture_ns.route('/commands', endpoint='Capture buffer commands')
class XenaRestCaptureCommands(XenaRestPortBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module, port):
        """
        Returns all commands.
        """

        return None, 501


@capture_ns.route('/commands/<string:command>', endpoint='Capture buffer command')
@api.param('command', 'CLI command name.')
class XenaRestCaptureCommand(XenaRestPortBase):

    def post(self, user, chassis, module, port, command):
        """
        Performs capture command.
        """

        capture_obj = get_object(user, chassis=chassis, module=module, port=port).capture
        return perform_command(capture_obj, request, command)


@capture_ns.route('/attributes', endpoint='Capture buffer attributes')
class XenaRestCaptureAttrs(XenaRestPortBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port):
        """
        Returns capture attributes.
        """

        capture_obj = get_object(user, chassis=chassis, module=module, port=port).capture
        return get_attributes(capture_obj)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module, port):
        """
        Set capture attributes.
        """

        capture_obj = get_object(user, chassis=chassis, module=module, port=port).capture
        return set_attributes(capture_obj, request)


@capture_ns.route('/statistics', endpoint='Capture buffer statistics')
class XenaRestCaptureStats(XenaRestPortBase):

    @api.marshal_list_with(counters_group)
    def get(self, user, chassis, module, port):
        """
        Returns capture statistics.
        """

        capture_obj = get_object(user, chassis=chassis, module=module, port=port).capture
        pc_stats = capture_obj.get_attribute('pc_stats').split()
        counters_groups = [{'name': 'pc_stats',
                            'counters': [{'name': 'status', 'value': pc_stats[0]},
                                         {'name': 'packets', 'value':  pc_stats[1]},
                                         {'name': 'starttime', 'value':  pc_stats[2]}]}]
        return counters_groups


@capture_ns.route('/<int:packet>', endpoint='Manage captured packet')
class XenaRestCapturePacket(XenaRestCaptureBase):

    @api.marshal_list_with(route_info)
    def get(self, user, chassis, module, port, packet):
        """
        Returns captured packet.
        """

        return build_route_info(routes=get_sub_routes(self), objects=[])


@capture_ns.route('/<int:packet>/commands', endpoint='Captured packet commands')
class XenaRestCapturePacketCommands(XenaRestCaptureBase):

    @api.marshal_list_with(command_description)
    def get(self, user, chassis, module, port):
        """
        Returns all commands.
        """

        return None, 501


@capture_ns.route('/<int:packet>/commands/<string:command>', endpoint='Captured packet command')
@api.param('command', 'CLI command name.')
class XenaRestCapturePacketCommand(XenaRestCaptureBase):

    def post(self, user, chassis, module, port, packet, command):
        """
        Performs capture command.
        """

        packet_obj = get_object(user, chassis=chassis, module=module, port=port, packet=packet)
        return perform_command(packet_obj, request, command)


@capture_ns.route('/<int:packet>/attributes', endpoint='Captured packet attributes')
class XenaRestCapturePacketAttr(XenaRestCaptureBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port, packet):
        """
        Returns captured packet.
        """

        packet_obj = get_object(user, chassis=chassis, module=module, port=port, packet=packet)
        return get_attributes(packet_obj)

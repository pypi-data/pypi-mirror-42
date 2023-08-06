"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
from flask import request

from xenavalkyrie.xena_stream import XenaModifierType, XenaModifierAction

from xenavalkyrie_rest.namespaces.base_ns import api, get_object, build_route_info, get_attributes
from xenavalkyrie_rest.namespaces.stream_ns import stream_path, XenaRestStreamBase, get_sub_routes
from xenavalkyrie_rest.namespaces.serializers import in_attribute, out_attribute, xena_object, route_info

modifier_path = stream_path + '/modifier/<int:modifier>'
modifier_ns = api.namespace('modifier', path=modifier_path, description='Manage Xena modifier')
modifiers_ns = api.namespace('modifier', path=stream_path + '/modifier', description='Manage Xena modifier')

xmodifier_path = stream_path + '/xmodifier/<int:modifier>'
xmodifier_ns = api.namespace('modifier', path=xmodifier_path, description='Manage Xena modifier')
xmodifiers_ns = api.namespace('modifier', path=stream_path + '/xmodifier', description='Manage Xena modifier')


@modifiers_ns.route('', endpoint='Manage modifiers')
class XenaRestModifiers(XenaRestStreamBase):

    @api.marshal_list_with(route_info)
    def get(self, user, chassis, module, port, stream):
        """
        Returns all modifiers.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        return build_route_info(routes=get_sub_routes(self), objects=stream_obj.modifiers.keys())

    @api.response(201, 'Modifier created.')
    @api.marshal_with(xena_object)
    def post(self, user, chassis, module, port, stream):
        """
        Add modifier.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        modifier_obj = stream_obj.add_modifier(m_type=XenaModifierType.standard)
        return {'id': modifier_obj.id}, 201


@xmodifiers_ns.route('', endpoint='Manage extended modifiers')
class XenaRestXModifiers(XenaRestStreamBase):

    @api.marshal_list_with(route_info)
    def get(self, user, chassis, module, port, stream):
        """
        Returns all extended modifiers.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        return build_route_info(routes=get_sub_routes(self), objects=stream_obj.xmodifiers.keys())

    @api.response(201, 'Modifier created.')
    @api.marshal_with(xena_object)
    def post(self, user, chassis, module, port, stream):
        """
        Add modifier.
        """

        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        modifier_obj = stream_obj.add_modifier(m_type=XenaModifierType.extended)
        modifier_obj.get()
        return {'id': modifier_obj.id}, 201


@api.param('modifier', 'Modifier index.', type=int, default='10')
class XenaRestModifierBase(XenaRestStreamBase):

    def _get(self):
        return build_route_info(routes=get_sub_routes(self), objects=[])

    def _delete(self, user, chassis, module, port, stream, modifier):
        stream_obj = get_object(user, chassis=chassis, module=module, port=port, stream=stream)
        m_type = XenaModifierType.standard if 'XModifier' not in self.__class__.__name__ else XenaModifierType.extended
        stream_obj.remove_modifier(modifier, m_type)
        return None, 204

    def _get_modifier_obj(self, user, chassis, module, port, stream, modifier):
        if 'XModifier' not in self.__class__.__name__:
            return get_object(user, chassis=chassis, module=module, port=port, stream=stream, modifier=modifier)
        else:
            return get_object(user, chassis=chassis, module=module, port=port, stream=stream, xmodifier=modifier)

    def _get_attributes(self, user, chassis, module, port, stream, modifier):
        """
        Returns modifier attributes.
        """

        modifier_obj = self._get_modifier_obj(user, chassis, module, port, stream, modifier)
        return get_attributes(modifier_obj)

    def _patch(self, user, chassis, module, port, stream, modifier):
        """
        Set modifier attributes.
        """

        modifier_obj = self._get_modifier_obj(user, chassis, module, port, stream, modifier)
        attributes = {name_value['name']: name_value['value'] for name_value in request.json}
        if 'action' in attributes:
            attributes['action'] = XenaModifierAction(attributes['action'].upper())
        modifier_obj.set(**attributes)


@modifier_ns.route('', endpoint='Manage modifier')
class XenaRestModifier(XenaRestModifierBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module, port, stream, modifier):
        """
        Returns sub-routes list.
        """

        return self._get()

    @api.response(204, 'Modifier removed.')
    def delete(self, user, chassis, module, port, stream, modifier):
        """
        Remove modifier.
        """
        return self._delete(user, chassis, module, port, stream, modifier)


@xmodifier_ns.route('', endpoint='Manage extended modifier')
class XenaRestXModifier(XenaRestModifierBase):

    @api.marshal_with(route_info)
    def get(self, user, chassis, module, port, stream, modifier):
        """
        Returns sub-routes list.
        """

        return self._get()

    @api.response(204, 'Extended modifier removed.')
    def delete(self, user, chassis, module, port, stream, modifier):
        """
        Remove extended modifier.
        """
        return self._delete(user, chassis, module, port, stream, modifier)


@modifier_ns.route('/attributes', endpoint='Modifier attributes')
class XenaRestModifierAttrs(XenaRestModifierBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port, stream, modifier):
        """
        Returns modifier attributes.
        """

        return self._get_attributes(user, chassis, module, port, stream, modifier)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module, port, stream, modifier):
        """
        Set modifier attributes.
        """

        return self._patch(user, chassis, module, port, stream, modifier)


@xmodifier_ns.route('/attributes', endpoint='Extended modifier attributes')
class XenaRestXModifierAttrs(XenaRestModifierBase):

    @api.marshal_list_with(out_attribute)
    def get(self, user, chassis, module, port, stream, modifier):
        """
        Returns extended modifier attributes.
        """

        return self._get_attributes(user, chassis, module, port, stream, modifier)

    @api.expect([in_attribute])
    def patch(self, user, chassis, module, port, stream, modifier):
        """
        Set extended modifier attributes.
        """

        return self._patch(user, chassis, module, port, stream, modifier)

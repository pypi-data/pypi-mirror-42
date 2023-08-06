"""
@author yoram@ignissoft.com
"""

from __future__ import unicode_literals
import os
import time
from flask import request

from trafficgenerator.tgn_utils import ApiType
from xenavalkyrie.xena_app import init_xena
from xenavalkyrie_rest.namespaces.serializers import (route_info, default_user, server_route_info, session_parser)
from xenavalkyrie_rest.namespaces.base_ns import (api, logger, XenaRestBase, get_object, get_sub_routes,
                                                  build_route_info)

session_path = '/session/<string:user>'
session_ns = api.namespace('session', description='Manage Xena Valkyrie test sessions')


@session_ns.route('', endpoint='Manage REST sessions')
class XenaRestSessions(XenaRestBase):

    @api.marshal_with(server_route_info)
    def get(self):
        """
        Returns sub-routes and sessions list (== users names).
        """

        return {'routes': get_sub_routes(self),
                'sessions': [{'user': user} for user in XenaRestBase.sessions.keys()]}

    @api.response(201, 'Session created.')
    @api.response(409, 'Session already exists.')
    @api.expect(session_parser)
    def post(self):
        """
        Creates new session.
        """

        user = request.args['user']
        if user in XenaRestBase.sessions:
            return None, 409
        XenaRestBase.sessions[user] = init_xena(ApiType.socket, logger, user).session
        XenaRestBase.sessions[user].timestamp = time.time()
        logger.info('Session {} created'.format(user))
        # Add local chassis by default if running on Xena Valkyrie chassis.
        if os.path.exists('/xbin'):
            # Use default port and password so it might fail, in which case the user should add the chassis manually.
            try:
                XenaRestBase.sessions[user].add_chassis('localhost')
            except Exception as _:
                pass
        return None, 201


@api.param('user', 'User name.', default=default_user)
@api.response(404, 'Object not found.')
class XenaRestSessionBase(XenaRestBase):
    pass


@session_ns.route('/<string:user>', endpoint='Manage REST session')
class XenaRestSession(XenaRestSessionBase):

    @api.response(204, 'Session deleted.')
    def delete(self, user):
        """
        Delete session.
        """

        get_object(user)
        XenaRestBase.sessions[user].disconnect()
        del XenaRestBase.sessions[user]
        logger.info('Session {} deleted'.format(user))
        return None, 204

    @api.marshal_list_with(route_info)
    def get(self, user):
        """
        Returns sub-routes and chassis list.
        """
        return build_route_info(routes=get_sub_routes(self), objects=[])


@session_ns.route('/<string:user>/statistics', endpoint='REST session statistics')
class XenaRestSessionStats(XenaRestSessionBase):

    def get(self, user):
        """
        Returns session statistics.
        """

        return None, 501

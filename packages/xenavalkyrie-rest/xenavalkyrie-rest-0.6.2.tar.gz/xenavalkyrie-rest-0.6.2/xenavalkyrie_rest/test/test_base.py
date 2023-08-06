
from builtins import str
import sys
from os import path
import requests
import flask
import logging
import json
from configparser import SafeConfigParser
from enum import Enum
import pytest


class CommandReturnType(Enum):
    no_output = 'no_output'
    line_output = 'line_output'
    multiline_output = 'multiline_output'


class RestMethod(Enum):
    get = 'GET'
    delete = 'DELETE'
    patch = 'PATCH'
    post = 'POST'


class MyResponse():

    def __init__(self, res):
        self.res = res

    def json(self):
        if type(self.res) is flask.wrappers.Response:
            return self.res.json
        else:
            return self.res.json()

    @property
    def status_code(self):
        return self.res.status_code

    @property
    def content(self):
        if type(self.res) is flask.wrappers.Response:
            return self.res.data
        else:
            return self.res.content


class TestXenaRestBase(object):

    config_file = path.join(path.dirname(__file__), 'XenaRestClient.ini')

    config = None
    logger = logging.getLogger('log')

    client = None

    def setup_class(self):

        TestXenaRestBase.config = SafeConfigParser(allow_no_value=True)
        TestXenaRestBase.config.read(TestXenaRestBase.config_file)

        TestXenaRestBase.logger.setLevel(TestXenaRestBase.config.get('Logging', 'level'))
        if TestXenaRestBase.config.get('Logging', 'file_name'):
            file_name = TestXenaRestBase.config.get('Logging', 'file_name')
            TestXenaRestBase.logger.addHandler(logging.FileHandler(file_name))
        TestXenaRestBase.logger.addHandler(logging.StreamHandler(sys.stdout))

    def setup(self):

        self._get_config()

        self.base_url = 'http://{}:{}'.format(self.server_ip, self.server_port)
        self.user_url = None
        self.resources_urls = {}

        # To start requests package logging (will send client log messages twice...)
        # logging.basicConfig(level=TestBaseXenaRest.config.get('Logging', 'level'))

        self.session_url = '/session'
        self.reset_url = '/management/operations/reset'
        res = self._post(self.reset_url, json={})
        assert(res.status_code == 200)

    def teardown(self):
        if self.user_url:
            self._release_resources()
            self._request(RestMethod.delete, self.user_url)

    def test_hello_world(self, server):
        pass

    def _get_config(self):

        self.server_ip = pytest.config.getoption('--server')  # @UndefinedVariable
        self.chassis_ip = pytest.config.getoption('--chassis')  # @UndefinedVariable
        self.port1 = '{}/{}'.format(self.chassis_ip, pytest.config.getoption('--port1'))  # @UndefinedVariable
        self.port2 = '{}/{}'.format(self.chassis_ip, pytest.config.getoption('--port2'))  # @UndefinedVariable
        self.port3 = pytest.config.getoption('--port3')  # @UndefinedVariable
        if self.server_ip:
            self.server_ip = self.server_ip.split(':')[0]
            self.server_port = self.server_ip.split(':')[1] if len(self.server_ip.split(':')) == 2 else '57911'
        else:
            self.server_ip = self.chassis_ip
            self.server_port = '57911'

        self.chassis2_ip = self.config.get('Chassis', 'ip2')
        self.user = self.config.get('Session', 'user')

    #
    # testers. Do not use atomic operations here.
    #

    def _test_get_chassis(self, num_objects):
        res = self._request(RestMethod.get, '{}/chassis'.format(self.user_url))
        assert(res.status_code == 200)
        assert(len(res.json()['chassis']) == num_objects)
        return [c['ip'] for c in res.json()['chassis']]

    def _test_get_subroutes(self, url, routes):
        res = self._request(RestMethod.get, url)
        assert(res.status_code == 200)
        assert(sorted((r['name'] for r in res.json()['routes'])) == sorted(routes))

    def _test_get_objects(self, url, *num_objects):
        res = self._request(RestMethod.get, url)
        assert(res.status_code == 200)
        assert(len(res.json()['objects']) in num_objects)

    def _test_get_attributes(self, url, *num_attributes):
        attributes_url = '{}/attributes'.format(url)
        res = self._request(RestMethod.get, attributes_url)
        assert(res.status_code == 200)
        assert(len(res.json()) in num_attributes)
        return {a['name']: a['value'] for a in res.json()}

    def _test_get_command(self, url, command, value):
        """ Basic command test.

        Any object has command with get (?) with expected output so we use it for basic commands test.
        """

        command_url = '{}/commands/{}'.format(url, command)
        res = self._post(command_url, json={'return_type': CommandReturnType.line_output.value, 'parameters': ['?']})
        assert(res.status_code == 200)
        assert(res.json().lower() == value.lower())

    #
    # Auxiliary operations.
    #

    def _create_user(self, user):
        res = self._post(self.session_url, params={'user': user})
        assert(res.status_code == 201)
        self.user_url = '{}/{}'.format(self.session_url, user)

    def _add_chassis(self, user, chassis):
        self._create_user(user)
        res = self._post('{}/chassis'.format(self.user_url), params={'ip': chassis})
        assert(res.status_code in [200, 201])
        return '{}/chassis/{}'.format(self.user_url, chassis)

    def _reserve_resources(self, *resources):

        for resource in resources:
            if len(resource.split('/')) == 1:
                reservation = 'c_reservation'
                reservedby = 'c_reservedby'
                resource_url = '{}/chassis/{}'.format(self.user_url, resource)
            elif len(resource.split('/')) == 2:
                reservation = 'm_reservation'
                reservedby = 'm_reservedby'
                resource_url = '{}/chassis/{}/module/{}'.format(self.user_url, *resource.split('/'))
            else:
                reservation = 'p_reservation'
                reservedby = 'p_reservedby'
                resource_url = '{}/chassis/{}/module/{}/port/{}'.format(self.user_url, *resource.split('/'))
            self.resources_urls[resource] = resource_url
            attributes = self._get_attributes(self.resources_urls[resource])
            if attributes[reservation] == 'RESERVED_BY_OTHER':
                if attributes[reservedby] != self.user:
                    raise Exception('{} reserved by {}'.format(resource, attributes[reservedby]))
                else:
                    # Its actually me but from different session...
                    self._perform_command(self.resources_urls[resource], reservation,
                                          CommandReturnType.no_output, 'relinquish')

            self._perform_command(self.resources_urls[resource], reservation, CommandReturnType.no_output, 'reserve')
            if len(resource.split('/')) == 3:
                self._perform_command(self.resources_urls[resource], 'p_reset', CommandReturnType.no_output)

    def _release_resources(self):
        for resource, resource_url in self.resources_urls.items():
            if len(resource.split('/')) == 1:
                reservation = 'c_reservation'
            elif len(resource.split('/')) == 2:
                reservation = 'm_reservation'
            else:
                reservation = 'p_reservation'
            self._perform_command(resource_url, reservation, CommandReturnType.no_output, 'release')

    def _add_stream(self, port):
        """ Add stream to reserved port.

        :param port: port location.
        :return: stream url.
        """
        streams_url = '{}/stream'.format(self.resources_urls[port])
        res = self._post(streams_url)
        return '{}/{}'.format(streams_url, res.json()['id'])

    #
    # Atomic operations.
    #

    def _get_children(self, object_url):
        return [c['id'] for c in self._request(RestMethod.get, object_url).json()['objects']]

    def _get_list_attribute(self, object_url, attribute):
        return self._get_attribute(object_url, attribute).split()

    def _get_attribute(self, object_url, attribute):
        return self._perform_command(object_url, attribute, CommandReturnType.line_output, '?').json()

    def _get_attributes(self, object_url):
        attributes_url = '{}/attributes'.format(object_url)
        return {a['name']: a['value'] for a in self._request(RestMethod.get, attributes_url).json()}

    def _set_attributes(self, object_url, **attributes):

        attributes_url = '{}/attributes'.format(object_url)
        attributes_list = [{u'name': str(name), u'value': str(value)} for name, value in attributes.items()]
        self._request(RestMethod.patch, attributes_url, headers={'Content-Type': 'application/json'},
                      data=json.dumps(attributes_list))

    def _perform_command(self, object_url, command, return_type, *parameters):
        command_url = '{}/commands/{}'.format(object_url, command)
        return self._post(command_url, json={'return_type': return_type.value, 'parameters': parameters})

    def _get_stats(self, object_url):
        statistics_url = '{}/statistics'.format(object_url)
        res = self._request(RestMethod.get, statistics_url)
        return {g['name']: {c['name']: c['value'] for c in g['counters']} for g in res.json()}

    def _post(self, url, **kwargs):
        if self.client:
            if 'params' in kwargs:
                kwargs['query_string'] = kwargs.pop('params')
        return self._request(RestMethod.post, url, **kwargs)

    def _request(self, method, url, **kwargs):
        self.logger.debug('method: {}, url: {}, kwargs={}'.format(method.value, url, kwargs))
        ignore = kwargs.pop('ignore', False)
        if self.client:
            if method == RestMethod.get:
                res = self.client.get(url, **kwargs)
            elif method == RestMethod.post:
                res = self.client.post(url, **kwargs)
            elif method == RestMethod.patch:
                res = self.client.patch(url, **kwargs)
            elif method == RestMethod.delete:
                res = self.client.delete(url, **kwargs)
            res = MyResponse(res)
        else:
            res = MyResponse(requests.request(method.value, '{}{}'.format(self.base_url, url), **kwargs))
        self.logger.debug('status_code: {}'.format(res.status_code))
        if not ignore and res.status_code >= 400:
            raise Exception('status_code: {}, content: {}'.format(res.status_code, res.content))
        if res.content:
            self.logger.debug('json: {}'.format(res.json()))
        return res


from os import path
import requests
import json
from io import BytesIO
from zipfile import ZipFile
import time
import re
import pytest

from trafficgenerator.tgn_utils import is_true
import xenavalkyrie_rest.settings as settings
from xenavalkyrie_rest import __version__
from xenavalkyrie_rest.test.test_base import TestXenaRestBase, CommandReturnType, RestMethod


class TestXenaRestOffline(TestXenaRestBase):

    def test_management(self, server):

        # Get.

        management_url = '/management'
        self._test_get_objects(management_url, 0)
        self._test_get_subroutes(management_url, ['attributes', 'statistics', 'operations', 'files'])
        operations_url = '{}/operations'.format(management_url)

        # Attributes.

        attrs = self._test_get_attributes(management_url, 4)
        assert(is_true(attrs['debug']) == settings.debug)
        assert(not attrs['sessions'].split())
        assert(int(attrs['timeout']) == settings.session_timeout)

        # debug level.

        self._set_attributes(management_url, debug=False)
        res = self._request(RestMethod.get, operations_url)
        assert(len(res.json()) == 1)

        self._set_attributes(management_url, debug=True)
        res = self._request(RestMethod.get, operations_url)
        assert(len(res.json()) == 3)

        # Statistics.

        time.sleep(1)
        stats = self._get_stats(management_url)['c_reststats']
        assert(stats['num_sessions'] == 0)
        assert(int(stats['current_time']) > int(stats['start_time']))

        # Create session and re-test attributes and statistics.

        res = self._post(self.session_url, params={'user': self.user})
        assert(res.status_code == 201)

        attrs = self._test_get_attributes(management_url, 4)
        assert(attrs['debug'])
        assert(attrs['sessions'].split() == [self.user])

        stats = self._get_stats(management_url)['c_reststats']
        assert(stats['num_sessions'] == 1)

        # session timeout.

        res = self._post(self.session_url, params={'user': 'second_user'})
        assert(res.status_code == 201)

        stats = self._get_stats(management_url)['c_reststats']
        assert(stats['num_sessions'] == 2)

        self._set_attributes(management_url, timeout=4)
        for _ in range(0, 4):
            time.sleep(1)
            self._request(RestMethod.get, '{}/{}'.format(self.session_url, self.user))

        stats = self._get_stats(management_url)['c_reststats']
        assert(stats['num_sessions'] == 1)

        # Files.

        if not self.client:

            res = requests.get('{}{}/files'.format(self.base_url, management_url))
            memory_file = BytesIO()
            memory_file.write(res.content)
            memory_file.seek(0)
            with ZipFile(memory_file, 'r') as zip_file:
                assert('xenavalkyrie_rest.log' in zip_file.namelist())

        # Negative.

        with pytest.raises(Exception) as excinfo:
            self._set_attributes(management_url, invalid=False)
        assert('XenaAttributeError' in str(excinfo.value))
        assert('not found' in repr(excinfo.value))

        with pytest.raises(Exception) as excinfo:
            self._set_attributes(management_url, sessions={})
        assert('XenaAttributeError' in repr(excinfo.value))
        assert('<notwritable>' in repr(excinfo.value).lower())

        with pytest.raises(Exception) as excinfo:
            self._set_attributes(management_url, timeout='invalid')
        assert('ValueError' in repr(excinfo.value))

        invalid_opration = '{}/invalid'.format(operations_url)
        with pytest.raises(Exception) as excinfo:
            self._post(invalid_opration, json={})
        assert('not found' in repr(excinfo.value))

        assert(attrs['version'] == __version__)

    def test_session(self, server):

        # No sessions.

        res = self._request(RestMethod.get, self.session_url)
        assert(res.status_code == 200)
        assert(res.json()['routes'] == [])
        assert(len(res.json()['sessions']) == 0)

        # Create session.

        res = self._post(self.session_url, params={'user': self.user})
        assert(res.status_code == 201)
        res = self._request(RestMethod.get, self.session_url)
        assert(len(res.json()['sessions']) == 1)
        assert(res.json()['sessions'][0]['user'] == self.user)

        # Get session.

        res = self._request(RestMethod.get, '{}/{}'.format(self.session_url, self.user))
        assert(sorted((r['name'] for r in res.json()['routes'])) == sorted(['chassis', 'statistics']))

        # Delete session.

        res = self._request(RestMethod.delete, '{}/{}'.format(self.session_url, self.user))
        assert(res.status_code == 204)
        res = self._request(RestMethod.get, self.session_url)
        assert(res.status_code == 200)
        assert(len(res.json()['sessions']) == 0)

        # Negative.

        res = self._request(RestMethod.delete, '{}/{}'.format(self.session_url, self.user), ignore=True)
        assert(res.status_code == 404)

        res = self._post(self.session_url, params={'user': self.user})
        res = self._post(self.session_url, params={'user': self.user}, ignore=True)
        assert(res.status_code == 409)

    def test_chassis(self, server):

        self._create_user(self.user)
        chassises_url = '{}/chassis'.format(self.user_url)

        # As there is no delete for chassis we start with negative tests while the list is empty.

        res = self._post(chassises_url, params={'ip': 'Invalid IP'}, ignore=True)
        assert(res.status_code == 500)
        assert('OSError' in res.json()['message'] or 'IOError' in res.json()['message'])

        res = self._post(chassises_url, params={'ip': self.chassis_ip, 'port': 22612}, ignore=True)
        if self.server_ip == self.chassis_ip:
            assert(res.status_code == 200)
        else:
            assert(res.status_code == 500)
            assert('OSError' in res.json()['message'] or 'IOError' in res.json()['message'])

        res = self._post(chassises_url, params={'ip': self.chassis_ip, 'port': 22611, 'password': 'Invalid password'},
                         ignore=True)
        if self.server_ip == self.chassis_ip:
            assert(res.status_code == 200)
        else:
            assert(res.status_code == 500)
            assert('XenaCommandError' in res.json()['message'])

        # No chassis or default chassis.

        res = self._request(RestMethod.get, self.user_url)
        assert(res.status_code == 200)

        if self.server_ip == self.chassis_ip:
            self._test_get_chassis(1)
        else:
            self._test_get_chassis(0)

        # Connect to chassis.

        res = self._post(chassises_url, params={'ip': self.chassis_ip})
        if self.server_ip == self.chassis_ip:
            assert(res.status_code == 200)
            res = self._test_get_chassis(1)
            assert('localhost' in res)
        else:
            assert(res.status_code == 201)
            res = self._test_get_chassis(1)
            assert(self.chassis_ip in res)

        chassis_url = '{}/{}'.format(chassises_url, self.chassis_ip)

        # Get.

        self._test_get_subroutes(chassis_url, ['attributes', 'commands', 'statistics', 'backdoor', 'module'])

        # Attributes.

        attributes = self._test_get_attributes(chassis_url, 18, 19)

        # Command.

        self._test_get_command(chassis_url, 'c_model', '"{}"'.format(attributes['c_model']))

        # Multiple chassis.

        if self.chassis2_ip:
            res = self._post(self.user_url, params={'ip': self.chassis2_ip})
            assert(res.status_code == 201)
            res = self._test_get_chassis(2)
            assert(self.chassis2_ip in res)

        # Backdoor.

        self._reserve_resources(self.port1)

        port1 = self.port1.split('/', 1)[1]
        backdoor_url = '{}/backdoor'.format(chassis_url)
        res = self._post(backdoor_url, json={'return_type': CommandReturnType.line_output.value,
                                             'command': '{} p_comment ?'.format(port1)})
        comment = re.sub('{}\s*P_COMMENT\s*'.format(port1), '', res.json())[1:-1]
        res = self._post(backdoor_url, json={'return_type': CommandReturnType.no_output.value,
                                             'command': '{} p_comment "new {}"'.format(port1, comment)})
        assert(not res.json())
        res = self._post(backdoor_url, json={'return_type': CommandReturnType.multiline_output.value,
                                             'command': '{} p_config ?'.format(port1)})
        for config in res.json():
            if 'P_COMMENT' in config:
                assert('"new {}"'.format(comment) in config)
                return
        raise Exception('No new comment')

    def test_module(self, server):

        chassis_url = self._add_chassis(self.user, self.chassis_ip)
        modules_url = '{}/module'.format(chassis_url)
        module = int(self.port1.split('/')[1])
        module_url = '{}/{}'.format(modules_url, module)

        # Get.

        self._test_get_objects(modules_url, 1, 3, 11)
        self._test_get_subroutes(module_url, ['attributes', 'commands', 'port'])

        # Attributes.

        self._reserve_resources('{}/{}'.format(self.chassis_ip, module))
        attributes = self._test_get_attributes(module_url, 15, 16, 18, 19)
        m_comment = attributes['m_comment']
        self._set_attributes(module_url, m_comment='"new {}"'.format(m_comment))
        attributes = self._test_get_attributes(module_url, 15, 16, 18, 19)
        assert(attributes['m_comment'] == 'new {}'.format(m_comment))
        self._set_attributes(module_url, m_comment='"{}"'.format(m_comment))

        # commands.

        self._test_get_command(module_url, 'm_model', '"{}"'.format(attributes['m_model']))

        # Negative.

    def test_port(self, server):

        chassis_url = self._add_chassis(self.user, self.chassis_ip)
        ports_url = '{}/module/{}/port'.format(chassis_url, self.port1.split('/')[1])
        port_url = '{}/{}'.format(ports_url, int(self.port1.split('/')[2]))

        # Get.

        self._test_get_objects(ports_url, 2)
        self._test_get_subroutes(port_url,
                                 ['attributes', 'commands', 'statistics', 'stream', 'tpld', 'capture', 'files'])

        # Attributes.

        attributes = self._test_get_attributes(port_url, 49, 51, 52, 53, 54)

        # Reserve (this also tests commands).

        commands_url = '{}/commands'.format(port_url)
        if attributes['p_reservation'] == 'RESERVED_BY_OTHER':
            if attributes['p_reservedby'] != self.user:
                raise Exception('Port {} reserved by {}'.format(self.port2, attributes['p_reservedby']))
            else:
                p_reservation_command = '{}/p_reservation'.format(commands_url)
                res = self._post(p_reservation_command, json={'return_type': CommandReturnType.no_output.value,
                                                              'parameters': ['relinquish']})
                assert(res.status_code == 200)
        p_reservation_command = '{}/p_reservation'.format(commands_url)
        res = self._post(p_reservation_command, json={'return_type': CommandReturnType.no_output.value,
                                                      'parameters': ['reserve']})
        assert(res.status_code == 200)

        # Set

        attributes_url = '{}/attributes'.format(port_url)
        res = self._request(RestMethod.patch, attributes_url, headers={'Content-Type': 'application/json'},
                            data=json.dumps([{u'name': u'p_comment', u'value': u'"NewComment"'}]))
        assert(res.status_code == 200)
        res = self._request(RestMethod.get, attributes_url)
        attributes = {a['name']: a['value'] for a in res.json()}
        assert(attributes['p_comment'] == 'NewComment')

        # Statistics.

        statistics_url = '{}/statistics'.format(port_url)
        res = self._request(RestMethod.get, statistics_url)
        assert(res.status_code == 200)
        statistics = {g['name']: {c['name']: c['value'] for c in g['counters']} for g in res.json()}
        assert(len(statistics) == 7)

        # Files.

        if not self.client:

            config_file = path.join(path.dirname(__file__), 'configs', 'test_config_loopback.xpc')
            files_url = '{}{}/files'.format(self.base_url, port_url)
            files = {'file': open(config_file, 'r')}
            data = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
            res = requests.post(files_url, files=files, data=data)
            assert(res.status_code == 201)

            res = requests.get(files_url)
            print(res.content)

        # Negative.

    def test_stream(self, server):

        self._add_chassis(self.user, self.chassis_ip)
        self._reserve_resources(self.port2)
        streams_url = '{}/stream'.format(self.resources_urls[self.port2])

        # Get.

        self._test_get_objects(streams_url, 0)
        self._test_get_subroutes(streams_url, [])

        # Add stream.

        res = self._request(RestMethod.post, streams_url)
        assert(res.status_code == 201)
        self._test_get_objects(streams_url, 1)
        assert(int(res.json()['id']) == 0)
        stream_url = '{}/{}'.format(streams_url, res.json()['id'])
        self._test_get_subroutes(stream_url, ['attributes', 'commands', 'statistics', 'modifier', 'xmodifier'])

        # Attributes.

        attributes = self._test_get_attributes(stream_url, 14, 15, 16)
        assert(attributes['ps_comment'] == '')

        # Set

        attributes_url = '{}/attributes'.format(stream_url)
        res = self._request(RestMethod.patch, attributes_url, headers={'Content-Type': 'application/json'},
                            data=json.dumps([{u'name': u'ps_comment', u'value': u'"NewComment"'}]))
        assert(res.status_code == 200)
        res = self._request(RestMethod.get, attributes_url)
        attributes = {a['name']: a['value'] for a in res.json()}
        assert(attributes['ps_comment'] == 'NewComment')

        # Command

        commands_url = '{}/commands'.format(stream_url)
        ps_enable_command = '{}/ps_enable'.format(commands_url)
        res = self._request(RestMethod.post, ps_enable_command,
                            json={'return_type': CommandReturnType.no_output.value, 'parameters': ['ON']})
        assert(res.status_code == 200)

        # Statistics.

        statistics_url = '{}/statistics'.format(stream_url)
        res = self._request(RestMethod.get, statistics_url)
        assert(res.status_code == 200)
        statistics = {g['name']: {c['name']: c['value'] for c in g['counters']} for g in res.json()}
        assert(len(statistics) == 1)

        # Delete stream.

        res = self._request(RestMethod.delete, stream_url)
        assert(res.status_code == 204)
        self._test_get_objects(streams_url, 0)

        # Negative.

    def _test_modifier_base(self, modifiers_url, ps_modifier):

        # Get.

        self._test_get_objects(modifiers_url, 0)
        self._test_get_subroutes(modifiers_url, [])

        # Add modifier.

        res = self._post(modifiers_url, params={'position': 10})
        assert(res.status_code == 201)
        self._test_get_objects(modifiers_url, 1)
        assert(int(res.json()['id']) == 0)
        modifier_url = '{}/{}'.format(modifiers_url, res.json()['id'])

        # Get.

        self._test_get_objects(modifier_url, 0)
        self._test_get_subroutes(modifier_url, ['attributes'])

        # Attributes.

        attributes = self._test_get_attributes(modifier_url, 2)
        assert('INC' in attributes[ps_modifier])

        # Set

        attributes_url = '{}/attributes'.format(modifier_url)
        res = self._request(RestMethod.patch, attributes_url, headers={'Content-Type': 'application/json'},
                            data=json.dumps([{u'name': u'action', u'value': u'DEC'}]))
        assert(res.status_code == 200)
        res = self._request(RestMethod.get, attributes_url)
        attributes = {a['name']: a['value'] for a in res.json()}
        assert('DEC' in attributes[ps_modifier])

        # Delete modifier.

        res = self._request(RestMethod.delete, modifier_url)
        assert(res.status_code == 204)
        self._test_get_objects(modifiers_url, 0)

        # Negative.

    def test_modifier(self, server):

        self._add_chassis(self.user, self.chassis_ip)
        self._reserve_resources(self.port2)
        stream_url = self._add_stream(self.port2)
        self._test_modifier_base('{}/modifier'.format(stream_url), 'ps_modifier')

    def test_xmodifier(self, server):

        if not self.port3:
            pytest.skip('Skip test - port that supports extended modifiers not found')
        self._add_chassis(self.user, self.port3.split('/')[0])
        self._reserve_resources(self.port3)
        stream_url = self._add_stream(self.port3)
        self._test_modifier_base('{}/xmodifier'.format(stream_url), 'ps_modifierext')

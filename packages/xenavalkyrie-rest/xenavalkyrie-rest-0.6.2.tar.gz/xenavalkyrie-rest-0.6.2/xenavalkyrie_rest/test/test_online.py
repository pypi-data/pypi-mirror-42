
import time
import json

from xenavalkyrie_rest.test.test_base import TestXenaRestBase, CommandReturnType


class TestXenaRestOnline(TestXenaRestBase):

    def test_traffic(self, server):

        self._add_chassis(self.user, self.chassis_ip)
        self._reserve_resources(self.port1, self.port2)

        # Add stream.
        stream1_url = self._add_stream(self.port1)
        stream2_url = self._add_stream(self.port2)

        # Set stream attribute.
        self._set_attributes(stream1_url, ps_enable='ON', ps_tpldid=self.port1.split('/')[1], ps_ratepps=1000,
                             ps_packetlimit=6000)
        self._set_attributes(stream2_url, ps_enable='ON', ps_tpldid=self.port2.split('/')[1], ps_ratepps=1000,
                             ps_packetlimit=4000)

        # Run traffic and get statistics.
        self._perform_command(self.resources_urls[self.port1], 'p_capture', CommandReturnType.no_output, 'ON')
        self._perform_command(self.resources_urls[self.port2], 'p_capture', CommandReturnType.no_output, 'ON')
        self._perform_command(self.resources_urls[self.port1], 'p_traffic', CommandReturnType.no_output, 'ON')
        self._perform_command(self.resources_urls[self.port2], 'p_traffic', CommandReturnType.no_output, 'ON')
        time.sleep(8)
        self._perform_command(self.resources_urls[self.port1], 'p_capture', CommandReturnType.no_output, 'OFF')
        self._perform_command(self.resources_urls[self.port2], 'p_capture', CommandReturnType.no_output, 'OFF')

        # Get statistics.
        stats = self._get_stats(self.resources_urls[self.port1])
        print(json.dumps(stats, indent=2))
        assert(stats['pt_total']['packets'] == 6000)
        stats = self._get_stats(self.resources_urls[self.port2])
        print(json.dumps(stats, indent=2))
        assert(stats['pt_total']['packets'] == 4000)

        pr_tplds = self._get_list_attribute(self.resources_urls[self.port1], 'pr_tplds')
        tplds = self._get_children('{}/tpld'.format(self.resources_urls[self.port1]))
        assert(len(pr_tplds) == len(tplds))
        stats = self._get_stats('{}/tpld/{}'.format(self.resources_urls[self.port1], tplds[0]))
        print(json.dumps(stats, indent=2))

        pr_tplds = self._get_list_attribute(self.resources_urls[self.port2], 'pr_tplds')
        tplds = self._get_children('{}/tpld'.format(self.resources_urls[self.port2]))
        assert(len(pr_tplds) == len(tplds))
        stats = self._get_stats('{}/tpld/{}'.format(self.resources_urls[self.port2], tplds[0]))
        print(json.dumps(stats, indent=2))

        # Get capture.
        port_capture_url = '{}/capture'.format(self.resources_urls[self.port1])
        self._get_attributes(port_capture_url)
        packets = int(self._get_list_attribute(port_capture_url, 'pc_stats')[1])
        captures = self._get_children(port_capture_url)
        assert(len(captures) == packets)

        port_capture_url = '{}/capture'.format(self.resources_urls[self.port2])
        packets = int(self._get_list_attribute(port_capture_url, 'pc_stats')[1])
        captures = self._get_children(port_capture_url)
        assert(len(captures) == packets)
        self._get_attributes('{}/{}'.format(port_capture_url, 0))

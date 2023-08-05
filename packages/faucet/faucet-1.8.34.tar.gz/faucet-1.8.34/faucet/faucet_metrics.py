"""Implement Prometheus statistics."""

# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2015 Brad Cowie, Christopher Lorier and Joe Stringer.
# Copyright (C) 2015 Research and Education Advanced Network New Zealand Ltd.
# Copyright (C) 2015--2018 The Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from prometheus_client import Gauge as PromGauge
from prometheus_client import Counter, Histogram

from faucet.prom_client import PromClient


class FaucetMetrics(PromClient):
    """Container class for objects that can be exported to Prometheus."""

    _dpid_counters = None # type: dict
    _dpid_gauges = None # type: dict

    def __init__(self, reg=None):
        super(FaucetMetrics, self).__init__(reg=reg)
        self.PORT_REQUIRED_LABELS = self.REQUIRED_LABELS + ['port', 'port_description']
        self._dpid_counters = {}
        self._dpid_gauges = {}
        self.faucet_config_reload_requests = self._counter(
            'faucet_config_reload_requests',
            'number of config reload requests', [])
        self.faucet_config_load_error = self._gauge(
            'faucet_config_load_error',
            '1 if last attempt to re/load config failed', [])
        self.faucet_event_id = self._gauge(
            'faucet_event_id',
            'highest/most recent event ID to be sent', [])
        self.faucet_config_reload_warm = self._dpid_counter(
            'faucet_config_reload_warm',
            'number of warm, differences only config reloads executed')
        self.faucet_config_reload_cold = self._dpid_counter(
            'faucet_config_reload_cold',
            'number of cold, complete reprovision config reloads executed')
        self.of_ignored_packet_ins = self._dpid_counter(
            'of_ignored_packet_ins',
            'number of OF packet_ins received but ignored from DP (due to rate limiting)')
        self.of_unexpected_packet_ins = self._dpid_counter(
            'of_unexpected_packet_ins',
            'number of OF packet_ins received that are unexpected from DP (e.g. for VLAN that is not configured)')
        self.of_packet_ins = self._dpid_counter(
            'of_packet_ins',
            'number of OF packet_ins received from DP')
        self.of_non_vlan_packet_ins = self._dpid_counter(
            'of_non_vlan_packet_ins',
            'number of OF packet_ins received from DP, not associated with a FAUCET VLAN')
        self.of_vlan_packet_ins = self._dpid_counter(
            'of_vlan_packet_ins',
            'number of OF packet_ins received from DP, associated with a FAUCET VLAN')
        self.of_flowmsgs_sent = self._dpid_counter(
            'of_flowmsgs_sent',
            'number of OF flow messages (and packet outs) sent to DP')
        self.of_errors = self._dpid_counter(
            'of_errors',
            'number of OF errors received from DP')
        self.of_dp_connections = self._dpid_counter(
            'of_dp_connections',
            'number of OF connections from a DP')
        self.of_dp_disconnections = self._dpid_counter(
            'of_dp_disconnections',
            'number of OF connections from a DP')
        self.vlan_hosts_learned = self._gauge(
            'vlan_hosts_learned',
            'number of hosts learned on a VLAN',
            self.REQUIRED_LABELS + ['vlan'])
        self.port_vlan_hosts_learned = self._gauge(
            'port_vlan_hosts_learned',
            'number of hosts learned on a port and VLAN',
            self.PORT_REQUIRED_LABELS + ['vlan'])
        self.vlan_neighbors = self._gauge(
            'vlan_neighbors',
            'number of L3 neighbors on a VLAN (whether resolved to L2 addresses, or not)',
            self.REQUIRED_LABELS + ['vlan', 'ipv'])
        self.vlan_learn_bans = self._gauge(
            'vlan_learn_bans',
            'number of times learning was banned on a VLAN',
            self.REQUIRED_LABELS + ['vlan'])
        self.faucet_config_table_names = self._gauge(
            'faucet_config_table_names',
            'number to names map of FAUCET pipeline tables',
            self.REQUIRED_LABELS + ['table_name'])
        self.faucet_packet_in_secs = self._histogram(
            'faucet_packet_in_secs',
            'FAUCET packet in processing time',
            self.REQUIRED_LABELS,
            (0.0001, 0.001, 0.01, 0.1, 1))
        self.faucet_valve_service_secs = self._histogram(
            'faucet_valve_service_secs',
            'FAUCET valve service processing time',
            self.REQUIRED_LABELS + ['valve_service'],
            (0.0001, 0.001, 0.01, 0.1, 1))
        self.bgp_neighbor_uptime_seconds = self._gauge(
            'bgp_neighbor_uptime',
            'BGP neighbor uptime in seconds',
            self.REQUIRED_LABELS + ['vlan', 'neighbor'])
        self.bgp_neighbor_routes = self._gauge(
            'bgp_neighbor_routes',
            'BGP neighbor route count',
            self.REQUIRED_LABELS + ['vlan', 'neighbor', 'ipv'])
        self.learned_macs = self._gauge(
            'learned_macs',
            ('MAC address stored as 64bit number to DP ID, port, VLAN, '
             'and n (discrete index)'),
            self.PORT_REQUIRED_LABELS + ['vlan', 'n'])
        self.port_status = self._gauge(
            'port_status',
            'status of switch ports',
            self.PORT_REQUIRED_LABELS)
        self.port_stack_state = self._gauge(
            'port_stack_state',
            'state of stacking on a port',
            self.PORT_REQUIRED_LABELS)
        self.port_learn_bans = self._gauge(
            'port_learn_bans',
            'number of times learning was banned on a port',
            self.PORT_REQUIRED_LABELS)
        self.port_lacp_status = self._gauge(
            'port_lacp_status',
            'status of LACP on port',
            self.PORT_REQUIRED_LABELS)
        self.dp_status = self._dpid_gauge(
            'dp_status',
            'status of datapaths')
        self.of_dp_desc_stats = self._gauge(
            'of_dp_desc_stats',
            'DP description (OFPDescStatsReply)',
            self.REQUIRED_LABELS + ['mfr_desc', 'hw_desc', 'sw_desc', 'serial_num', 'dp_desc'])
        self.stack_cabling_errors = self._dpid_counter(
            'stack_cabling_errors',
            'number of cabling errors detected in all FAUCET stacks')
        self.stack_probes_received = self._dpid_counter(
            'stack_probes_received',
            'number of stacking messages received')
        self.dp_dot1x_success = self._dpid_counter(
            'dp_dot1x_success',
            'number of successful authentications on dp')
        self.dp_dot1x_failure = self._dpid_counter(
            'dp_dot1x_failure',
            'number of authentications attempts failed on dp')
        self.dp_dot1x_logoff = self._dpid_counter(
            'dp_dot1x_logoff',
            'number of eap-logoff events on dp')
        self.port_dot1x_success = self._counter(
            'port_dot1x_success',
            'number of successful authentications on port',
            self.PORT_REQUIRED_LABELS)
        self.port_dot1x_failure = self._counter(
            'port_dot1x_failure',
            'number of authentications attempts failed on port',
            self.PORT_REQUIRED_LABELS)
        self.port_dot1x_logoff = self._counter(
            'port_dot1x_logoff',
            'number of eap-logoff events on port',
            self.PORT_REQUIRED_LABELS)

    def _counter(self, var, var_help, labels):
        return Counter(var, var_help, labels, registry=self._reg) # pylint: disable=unexpected-keyword-arg

    def _gauge(self, var, var_help, labels):
        return PromGauge(var, var_help, labels, registry=self._reg) # pylint: disable=unexpected-keyword-arg

    def _histogram(self, var, var_help, labels, buckets):
        return Histogram(var, var_help, labels, buckets=buckets, registry=self._reg) # pylint: disable=unexpected-keyword-arg

    def _dpid_counter(self, var, var_help):
        counter = self._counter(var, var_help, self.REQUIRED_LABELS)
        self._dpid_counters[var] = counter
        return counter

    def _dpid_gauge(self, var, var_help):
        gauge = self._gauge(var, var_help, self.REQUIRED_LABELS)
        self._dpid_gauges[var] = gauge
        return gauge

    def reset_dpid(self, dp_labels):
        """Set all DPID-only counter/gauges to 0."""
        for counter in self._dpid_counters.values():
            counter.labels(**dp_labels).inc(0)
        for gauge in self._dpid_gauges.values():
            gauge.labels(**dp_labels).set(0)

    def inc_var(self, var, labels, val=1):
        assert labels is not None
        metrics_var = getattr(self, var)
        metrics_var.labels(**labels).inc(val)

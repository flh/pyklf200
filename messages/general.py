# -*- coding: utf-8 -*-

from . import commands
from .base import KlfGwResponse, KlfGwRequest, KlfSuccessOneMixin
from datetime import datetime

class GetVersionReq(KlfGwRequest):
    klf_command = commands.GW_GET_VERSION_REQ

class GetVersionCfm(KlfGwResponse):
    klf_command = commands.GW_GET_VERSION_CFM
    arguments_format = '6sBBB'

    def fill_arguments(self):
        self.software_version = self.raw_arguments[0]
        self.hardware_version = self.raw_arguments[1]
        # Velux technical doc states that product_group should always be 14.
        self.product_group = self.raw_arguments[2]
        # Velux technical doc states that product_type should always be 3.
        self.product_type = self.raw_arguments[3]

class GetProtocolVersionReq(KlfGwRequest):
    klf_command = commands.GW_GET_PROTOCOL_VERSION_REQ

class GetProtocolVersionCfm(KlfGwResponse):
    klf_command = commands.GW_GET_PROTOCOL_VERSION_CFM
    arguments_format = 'HH'

    def fill_arguments(self):
        self.major_version = self.raw_arguments[0]
        self.minor_version = self.raw_arguments[1]

class GetStateReq(KlfGwRequest):
    klf_command = commands.GW_GET_STATE_REQ

    def get_arguments(self):
        return ()

class GetStateCfm(KlfGwResponse):
    klf_command = commands.GW_GET_STATE_CFM
    arguments_format = 'BB4s'

    def fill_arguments(self):
        self.gateway_state = self.raw_arguments[0]
        self.sub_state = self.raw_arguments[1]
        self.state_data = self.raw_arguments[2]

class LeaveLearnStateReq(KlfGwRequest):
    klf_command = commands.GW_LEAVE_LEARN_STATE_REQ

class LeaveLearnStateCfm(KlfSuccessOneMixin, KlfGwResponse):
    klf_command = commands.GW_LEAVE_LEARN_STATE_CFM

class SetUTCReq(KlfGwRequest):
    klf_command = commands.GW_SET_UTC_REQ

    def __init__(self, dt=None):
        self.datetime = dt

    def get_arguments(self):
        if self.datetime is None:
            dt = datetime.now()
        else:
            dt = self.datetime

        return (('L', int(dt.timestamp())),)

class SetUTCCfm(KlfGwResponse):
    klf_command = commands.GW_SET_UTC_CFM

class RtcSetTimeZoneReq(KlfGwRequest):
    klf_command = commands.GW_RTC_SET_TIME_ZONE_REQ

    def __init__(self, timezone):
        raise NotImplemented

    def get_arguments(self):
        raise NotImplemented

class SetTimeZoneCfm(KlfSuccessOneMixin, KlfGwResponse):
    klf_command = commands.GW_RTC_SET_TIME_ZONE_CFM

class GetLocalTimeReq(KlfGwRequest):
    klf_command = commands.GW_GET_LOCAL_TIME_REQ

class GetLocalTimeCfm(KlfGwResponse):
    klf_command = commands.GW_GET_LOCAL_TIME_CFM
    arguments_format = 'LBBBBBHBHB'

    def fill_arguments(self):
        self.utc_time = datetime.utcfromtimestamp(self.raw_arguments[0])

class RtcSetTimeZoneCfm(KlfSuccessOneMixin, KlfGwResponse):
    klf_command = commands.GW_RTC_SET_TIME_ZONE_CFM

class RebootReq(KlfGwRequest):
    klf_command = commands.GW_REBOOT_REQ

class RebootCfm(KlfGwResponse):
    klf_command = commands.GW_REBOOT_CFM

class SetFactoryDefaultReq(KlfGwRequest):
    klf_command = commands.GW_SET_FACTORY_DEFAULT_REQ

class SetFactoryDefaultCfm(KlfGwResponse):
    klf_command = commands.GW_SET_FACTORY_DEFAULT_CFM

class GetNetworkSetupReq(KlfGwRequest):
    klf_command = commands.GW_GET_NETWORK_SETUP_REQ

class GetNetworkSetupCfm(KlfGwResponse):
    klf_command = commands.GW_GET_NETWORK_SETUP_CFM
    arguments_format = '4s4s4sB'

    def fill_arguments(self):
        self.ip_address = IPv4Address(self.raw_arguments[0])
        self.mask = IPv4Address(self.raw_arguments[1])
        self.default_gw = IPv4Address(self.raw_arguments[2])
        self.use_dhcp = self.raw_arguments[3] == 1

class SetNetworkSetupReq(KlfGwRequest):
    klf_command = commands.GW_SET_NETWORK_SETUP_REQ

    def __init__(self, ip_address, mask, default_gw, use_dhcp):
        self.ip_address = ip_address
        self.mask = mask
        self.default_gw = default_gw
        self.use_dhcp = use_dhcp

    def get_arguments(self):
        return (
            ('4s', self.ip_address.packed),
            ('4s', self.mask.packed),
            ('4s', self.default_gw.packed),
            ('B', int(self.use_dhcp)),
        )

class SetNetworkSetupCfm(KlfGwResponse):
    klf_command = commands.GW_SET_NETWORK_SETUP_CFM

class ErrorNtf(KlfGwResponse):
    klf_command = commands.GW_ERROR_NTF
    arguments_format = 'B'

    def fill_arguments(self):
        self.error_number = self.raw_arguments[0]

    _strerror_dict = {
        0: 'Generic error',
        1: 'Unknown command or command not accepted in this state',
        2: 'Error on frame structure',
        7: 'Busy, try again later',
        8: 'Bad system table index',
        12: 'Not authenticated',
    }
    @property
    def strerror(self):
        return self._strerror_dict.get(self.error_number,
            'Undocumented error')

    def __str__(self):
        return '{klass}: {strerror}'.format(
            klass=type(self).__name__,
            strerror=self.strerror)

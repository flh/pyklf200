# -*- coding: utf-8 -*-

import commands
from base import KlfGwResponse, KlfGwRequest, KlfSuccessOneMixin

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

# -*- coding: utf-8 -*-

import commands
from base import KlfGwResponse, KlfGwRequest, KlfSuccessZeroMixin

class PasswordEnterReq(KlfGwRequest):
    klf_command = commands.GW_PASSWORD_ENTER_REQ

    def __init__(self, password):
        self.password = password

    def get_arguments(self):
        return (('31sx', bytes(self.password)),)

class PasswordEnterCfm(KlfSuccessZeroMixin, KlfGwResponse):
    klf_command = commands.GW_PASSWORD_ENTER_CFM

    def __str__(self):
        if self.is_success:
            str_status = "authentication failure"
        else:
            str_status = "authentication success"

        return "{class_name}: {status}".format(
                class_name=type(self).__name__,
                status=str_status)

class PasswordChangeReq(KlfGwRequest):
    klf_command = commands.GW_PASSWORD_CHANGE_REQ

    def __init__(self, old_password, new_password):
        self.old_password = old_password
        self.new_password = new_password

    def get_arguments(self):
        return (
            ('31sx', bytes(self.old_password)),
            ('31sx', bytes(self.new_password)),
        )

class PasswordChangeCfm(KlfSuccessZeroMixin, KlfGwResponse):
    klf_command = commands.GW_PASSWORD_CHANGE_CFM

class PasswordChangeNtf(KlfGwResponse):
    klf_command = commands.GW_PASSWORD_CHANGE_NTF
    arguments_format = '31sx'

    def fill_arguments(self):
        self.new_password = self.raw_arguments[0]

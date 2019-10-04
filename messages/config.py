# -*- coding: utf-8 -*-

# pyKlf200 - Python client implementation of the Velux KLF200 protocol
# Copyright (c) 2019 Florian Hatat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from . import commands
from .base import KlfGwResponse, KlfGwRequest, KlfSuccessZeroMixin

class CsControllerCopyReq(KlfGwMessage):
    klf_command = commands.GW_CS_CONTROLLER_COPY_REQ

    COPY_MODE_TCM = 0
    COPY_MODE_RCM = 1

    def __init__(self, copy_mode):
        self.copy_mode = copy_mode

    def get_arguments(self):
        return (('B', self.copy_mode),)

class CsControllerCopyCfm(KlfGwResponse):
    klf_command = commands.GW_CS_CONTROLLER_COPY_CFM

class CsControllerCopyNtf(KlfGwResponse):
    klf_command = commands.GW_CS_CONTROLLER_COPY_NTF
    arguments_format = 'BB'

    COPY_OK = 0
    COPY_FAILED_NO_OTHER_CONTROLLER = 2
    COPY_FAILED_DTS_NOT_READY = 4
    COPY_FAILED_DTS_ERROR = 5
    COPY_FAILED_CS_NOT_READY = 9

    def fill_arguments(self):
        self.controller_copy_mode = self.raw_arguments[0]
        self.controller_copy_status = self.raw_arguments[1]

    @property
    def is_success(self):
        return self.controller_copy_mode == self.COPY_OK

class CsControllerCopyCancelNtf(KlfGwMessage):
    klf_command = commands.GW_CS_CONTROLLER_COPY_CANCEL_NTF

class VirginStateReq(KlfGwMessage):
    klf_command = commands.GW_CS_VIRGIN_STATE_REQ

    def get_arguments(self):
        return ()

class VirginStateCfm(KlfGwMessage):
    klf_command = commands.GW_CS_VIRGIN_STATE_CFM

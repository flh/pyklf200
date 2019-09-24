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

class GetAllNodesInformationReq(KlfGwRequest):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_REQ

    def get_arguments(self):
        return ()

class GetAllNodesInformationCfm(KlfSuccessZeroMixin, KlfGwResponse):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_CFM
    arguments_format = 'BB'

    def fill_arguments(self):
        super().fill_arguments()
        self.total_nodes = self.raw_arguments[1]

class GetAllNodesInformationNtf(KlfGwResponse):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_NTF
    arguments_format = 'BHB64sBHBBBBB8sBHHHHHHHLB5L'

    def fill_arguments(self):
        self.node_id = self.raw_arguments[0]
        self.order = self.raw_arguments[1]
        self.placement = self.raw_arguments[2]
        self.name = self.raw_arguments[3].decode('utf-8')
        self.velocity = self.raw_arguments[4]
        self.node_subtype = self.raw_arguments[5]
        self.product_type = self.raw_arguments[6]
        self.node_variation = self.raw_arguments[7]
        self.power_mode = self.raw_arguments[8]
        self.serial_number = self.raw_arguments[9]
        self.state = self.raw_arguments[10]
        self.current_position = self.raw_arguments[11]
        ...

    def __str__(self):
        return "ID {node_id}: {name} ({product_type}), position {pos}".format(
                node_id=self.node_id,
                name=self.name,
                product_type=self.product_type,
                pos=self.current_position)

class GetAllNodesInformationFinishedNtf(KlfGwResponse):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_FINISHED_NTF
    arguments_format = ''

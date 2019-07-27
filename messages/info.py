# -*- coding: utf-8 -*-

import commands
from base import KlfGwResponse, KlfGwRequest

class GetVersionReq(KlfGwRequest):
    klf_command = commands.GW_GET_VERSION_REQ
    arguments_format = ''

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

class GetAllNodesInformation(KlfGwRequest):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_REQ

    def get_arguments(self):
        return ()

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

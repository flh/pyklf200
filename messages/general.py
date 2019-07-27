# -*- coding: utf-8 -*-

import commands
from base import KlfGwResponse, KlfGwRequest

class GetStateReq(KlfGwRequest):
    klf_command = commands.GW_GET_STATE_REQ

    def get_arguments(self):
        return ()

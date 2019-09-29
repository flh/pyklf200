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
from .base import KlfGwResponse, KlfGwRequest, KlfSuccessOneMixin

"""
Commands from the "Command Handler" section of the API
"""

class NoSessionIDAvailable(Exception):
    """
    Exception raised when no fresh session identifier is available.
    """
    pass

class KlfSessionId:
    """
    Base class for request commands which need to create a unique
    session ID.

    This class maintains a registry of currently active session IDs and
    allocates a new one upon any object instantiation.

    Session IDs are released when one calls the class method
    free_session. This usually happens when we receive a
    SessionFinishedNtf response from the gateway.
    """
    _running_sessions = set()

    @classmethod
    def _allocate_session(cls):
        try:
            session_id = 1 + max(cls._running_sessions)
        except ValueError:
            session_id = 0

        if session_id >= 2 ** 16:
            for i in range(2 ** 16):
                if i not in cls._running_sessions:
                    session_id = i
                    break
            raise NoSessionIDAvailable
        cls._running_sessions.add(session_id)
        return session_id

    def __init__(self):
        self.session_id = KlfSessionId._allocate_session()

    @classmethod
    def free_session(cls, session_id):
        """
        Remove a session identifier from the registry.

        After this call, the session identifier may be allocated again
        for a new session.
        """
        cls._running_sessions.remove(session_id)

class CommandSendReq(KlfSessionId, KlfGwRequest):
    klf_command = commands.GW_COMMAND_SEND_REQ

    ORIGINATOR_USER = 1
    ORIGINATOR_RAIN = 2
    ORIGINATOR_TIMER = 3
    ORIGINATOR_UPS = 5
    ORIGINATOR_SAAC = 8
    ORIGINATOR_WIND = 9
    ORIGINATOR_LOAD_SHEDDING = 11
    ORIGINATOR_LOCAL_LIGHT = 12
    ORIGINATOR_ENVIRONMENT_SENSOR = 13
    ORIGINATOR_EMERGENCY = 255

    PRIORITY_PROTECTION_HUMAN = 0
    PRIORITY_PROTECTION_ENVIRONMENT = 1
    PRIORITY_USER_LEVEL1 = 2
    PRIORITY_USER_LEVEL2 = 3
    PRIORITY_COMFORT_LEVEL1 = 4
    PRIORITY_COMFORT_LEVEL2 = 5
    PRIORITY_COMFORT_LEVEL3 = 6
    PRIORITY_COMFORT_LEVEL4 = 7

    PLI_DISABLE = 0
    PLI_ENABLE = 1
    PLI_ENABLE_ALL = 2
    PLI_KEEP_CURRENT = 3

    def __init__(self, main_parameter,
            command_originator=ORIGINATOR_USER,
            priority_level=PRIORITY_USER_LEVEL2,
            parameter_active=0, functional_parameters=(), nodes=(),
            priority_level_lock=False, priority_levels=(), lock_time=0):

        super().__init__()
        self.main_parameter = main_parameter
        self.command_originator = command_originator
        self.priority_level = priority_level
        self.priority_level_lock = priority_level_lock
        self.parameter_active = parameter_active
        self.functional_parameters = functional_parameters
        self.nodes = nodes
        self.priority_levels = priority_levels
        self.lock_time = lock_time

    def get_arguments(self):
        fpi1 = 0
        fpi2 = 0
        fpvalues = [0 for i in range(16)]
        for fp_index, fp_value in enumerate(self.functional_parameters):
            if fp_index < 8:
                fpi1 |= 1 << fp_index
            else:
                fpi2 |= 1 << (fp_index - 8)

            fpvalues[fp_index] = fp_value

        nodes = list(self.nodes) + [0 for i in range(20 - len(self.nodes))]

        pli03 = 0
        pli47 = 0
        for pl_index, pl_value in enumerate(self.priority_levels):
            if pl_index < 4:
                pli03 |= pl_value << (2 * pl_index)
            else:
                pli47 |= pl_value << (2 * (pl_index - 4))

        return (
                ('H', self.session_id),
                ('B', self.command_originator),
                ('B', self.priority_level),
                ('B', self.parameter_active),
                ('B', fpi1),
                ('B', fpi2),
                (None, bytes(self.main_parameter)),
            ) + \
            tuple((None, bytes(fpvalues[i])) for i in range(16)) + \
            (
                ('B', 1 + len(self.nodes)),
            ) + \
            tuple(('B', nodes[i]) for i in range(20)) + \
            (
                ('B', int(self.priority_level_lock)),
                ('B', pli03),
                ('B', pli47),
                ('B', int(self.lock_time // 30)),
            )

class CommandSendCfm(KlfSuccessOneMixin, KlfGwResponse):
    klf_command = commands.GW_COMMAND_SEND_CFM
    arguments_format = 'HB'
    status_position = 1

    def fill_parameters(self):
        super().fill_parameters(self)
        self.session_id = self.raw_arguments[0]

class CommandRunStatusNtf(KlfGwResponse):
    klf_command = commands.GW_COMMAND_RUN_STATUS_NTF
    arguments_format = 'HBBBHBBL'

    def fill_parameters(self):
        self.session_id = self.raw_arguments[0]
        self.status_id = self.raw_arguments[1]
        self.index = self.raw_arguments[2]
        self.node_parameter = self.raw_arguments[3]
        self.parameter_value = self.raw_arguments[4]
        self.run_status = self.raw_arguments[5]
        self.status_reply = self.raw_arguments[6]
        self.information_code = self.raw_arguments[7]

class SessionFinishedNtf(KlfGwResponse):
    klf_command = commands.GW_SESSION_FINISHED_NTF
    arguments_format = 'H'

    def fill_parameters(self):
        self.session_id = self.raw_arguments[0]
        KlfSessionId.free_session(self.session_id)

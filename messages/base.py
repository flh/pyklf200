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

import struct
from functools import reduce
from operator import xor

class KlfGwMessage:
    """
    Base class representing any message, sent to the KLF200 gateway or
    received from it.
    """
    klf_command = None
    protocol_id = 0

class KlfGwRequest(KlfGwMessage):
    """
    Base class representing a request sent to the KLF200 gateway.
    """
    def get_arguments(self):
        pass

    def __bytes__(self):
        command_frame = struct.pack('>H', self.klf_command)
        command_frame += b''.join(map(lambda arg_line:
                struct.pack('>' + arg_line[0], arg_line[1])
                  if arg_line[0] is not None
                  else arg_line[1], self.get_arguments()))

        command_length_frame = struct.pack('>B', len(command_frame) +
                1) + command_frame

        protocol_frame = struct.pack('>B', self.protocol_id) + \
                command_length_frame

        checksum = struct.pack('>B', reduce(xor, protocol_frame))

        return protocol_frame + checksum

class KlfGwResponseMetaclass(type):
    """
    Metaclass which tracks classes handling gateway commands responses,
    given by their command number.
    """
    _klf_response_class = {}

    def __init__(cls, nom, bases, dict):
        super().__init__(nom, bases, dict)
        if cls.klf_command is not None:
            KlfGwResponseMetaclass._klf_response_class[cls.klf_command] = cls

class KlfError(Exception):
    """
    Base class for errors which can be raised when communicating with
    the gateway.
    """
    pass

class KlfWrongProtocolId(KlfError):
    """
    Exception raised when a frame received from the gateway bears an
    unhandled protocol identifier.
    """
    pass

class KlfWrongChecksum(KlfError):
    """
    Exception raised when a frame received from the gateway has an
    incorrect checksum.
    """
    pass

class KlfWrongLength(KlfError):
    """
    Exception raised when a frame received from the gateway has an
    incorrect frame length.
    """
    pass

class KlfGwResponse(KlfGwMessage, metaclass=KlfGwResponseMetaclass):
    """
    Base class for parsing gateway responses.

    Each subclass should define a klf_command attribute.
    """
    def get_arguments_format(self):
        try:
            return self.arguments_format
        except AttributeError:
            return None

    def expected_data_length(self):
        return struct.calcsize(self.get_arguments_format())

    def __new__(cls, frame):
        protocol_id = struct.unpack('>B', frame[0:1])[0]
        if protocol_id != 0:
            raise KlfWrongProtocolId()

        data_length = struct.unpack('>B', frame[1:2])[0]
        if data_length != len(frame) - 2:
            raise KlfWrongLength()

        klf_command = struct.unpack('>H', frame[2:4])[0]

        expected_checksum = reduce(xor, frame[:-1])
        checksum = struct.unpack('>B', frame[-1:])[0]
        if expected_checksum != checksum:
            raise KlfWrongChecksum()

        # Try to find in the registry a class handling the matching
        # klf_command
        klf_class = type(cls)._klf_response_class.get(klf_command, cls)
        klf_response = super().__new__(klf_class)
        return klf_response

    def __init__(self, frame):
        self.raw_frame = frame

        arguments_format = self.get_arguments_format()
        if arguments_format is not None:
            raw_data = struct.unpack('>BBH' + arguments_format + 'B',
                    frame)
        else:
            raw_data = struct.unpack('>BBH', frame[:4])

        self.protocol_id = raw_data[0]
        self.klf_command = raw_data[2]
        self.raw_arguments = raw_data[3:-1]

        self.fill_arguments()

    def fill_arguments(self):
        pass

class KlfStatusMixin:
    arguments_format = 'B'
    status_position = 0

    def fill_arguments(self):
        self.status = self.raw_arguments[self.status_position]

class KlfSuccessZeroMixin(KlfStatusMixin):
    arguments_format = 'B'

    def fill_arguments(self):
        super().fill_arguments()
        self.is_success = self.status == 0

class KlfSuccessOneMixin(KlfStatusMixin):
    arguments_format = 'B'

    def fill_arguments(self):
        super().fill_arguments()
        self.is_success = self.status == 1

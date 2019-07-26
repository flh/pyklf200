# -*- coding: utf-8 -*-

import socket
import ssl
import struct
from functools import reduce
from operator import xor
import logging

import commands

def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)

class KlfServer:
    INPUT_STATE_INIT = 0
    INPUT_STATE_FRAME = 1
    INPUT_STATE_ESC = 2

    # SLIP escape characters, see RFC1055
    SLIP_END     = b'\xC0'
    SLIP_ESC     = b'\xDB'
    SLIP_ESC_END = b'\xDC'
    SLIP_ESC_ESC = b'\xDD'

    def recvall(self):
        seen_frames = []
        while True:
            try:
                data = self.klf_socket.recv(4096)
            except (BlockingIOError, ssl.SSLWantReadError):
                logging.debug("No more data to receive from the socket gateway")
                # TODO
                break

            logging.debug("Parsing received data: {data}".format(
                data=toHex(data)))
            for c in data:
                if self.input_state == self.INPUT_STATE_INIT:
                    if c == self.SLIP_END:
                        self.input_state = self.INPUT_STATE_FRAME

                elif self.input_state == self.INPUT_STATE_FRAME:
                    if c == self.SLIP_END:
                        self.input_state = self.INPUT_STATE_INIT
                        seen_frames.append(KlfGwResponse(self.input_buffer))
                        self.input_buffer = b''
                    elif c == self.SLIP_ESC:
                        self.input_state = self.INPUT_STATE_ESC
                    else:
                        self.input_buffer += c

                elif self.input_state == self.INPUT_STATE_ESC:
                    self.input_state = self.INPUT_STATE_FRAME
                    if c == self.SLIP_ESC_END:
                        self.input_buffer += self.SLIP_END
                    elif c == self.SLIP_ESC_ESC:
                        self.input_buffer += self.SLIP_ESC

        return seen_frames

    @classmethod
    def slip_pack(cls, inputFrame):
        """
        Encode data in a SLIP (RFC1055) frame and return the packed
        bytes.
        """
        data = inputFrame
        data = data.replace(cls.SLIP_ESC, cls.SLIP_ESC + cls.SLIP_ESC_ESC)
        data = data.replace(cls.SLIP_END, cls.SLIP_ESC + cls.SLIP_ESC_END)
        return cls.SLIP_END + data + cls.SLIP_END

    def __init__(self, address, password, port=51200):
        self.klf_address = address
        self.klf_password = password
        self.klf_port = port
        self.klf_socket = None

        self.input_state = self.INPUT_STATE_INIT
        self.input_buffer = b''

    def fileno(self):
        """
        Return the file descriptor associated to the socket which
        communicates with the gateway.
        """
        return self.klf_socket.fileno()

    def connect(self):
        """
        Open a new socket to the gateway.
        """
        context = ssl.SSLContext()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.klf_socket = context.wrap_socket(sock,
                server_hostname=self.klf_address)
        self.klf_socket.connect((self.klf_address, self.klf_port))
        self.klf_socket.setblocking(False)

    def send_message(self, message):
        """
        Send a message to the gateway.
        """
        frame = self.slip_pack(bytes(message))
        len_sent = self.klf_socket.sendall(frame)
        logging.debug("Sent frame: {frame}".format(
            frame=toHex(frame)))

    def enter_password(self):
        logging.info("Sending authentication data to the gateway")
        self.send_message(PasswordEnterReq(self.klf_password))

    def ping(self):
        logging.info("Sending ping request to the gateway")
        self.send_message(GetStateReq())

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
        return self.arguments_format

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
        raw_data = struct.unpack('>BBH' + self.get_arguments_format() + 'B',
                frame)
        self.protocol_id = raw_data[0]
        self.klf_command = raw_data[1]
        self.raw_arguments = raw_data[3:-1]

class GetAllNodesInformationNtf(KlfGwResponse):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_NTF
    arguments_format = 'BHB64sBHBBBBB8sBHHHHHHHLB5L'

    def __init__(self, frame):
        super().__init__(frame)

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
        return "ID {node_id}: {name} (product_type)".format(
                node_id=self.node_id,
                name=self.name,
                product_type=self.product_type)

class PasswordEnterReq(KlfGwRequest):
    klf_command = commands.GW_PASSWORD_ENTER_REQ

    def __init__(self, password):
        self.password = password

    def get_arguments(self):
        return (('31sx', bytes(self.password)),)

class PasswordEnterCfm(KlfGwResponse):
    klf_command = commands.GW_PASSWORD_ENTER_CFM
    arguments_format = ''

class GetStateReq(KlfGwRequest):
    klf_command = commands.GW_GET_STATE_REQ

    def get_arguments(self):
        return ()

class GetAllNodesInformation(KlfGwRequest):
    klf_command = commands.GW_GET_ALL_NODES_INFORMATION_REQ

    def get_arguments(self):
        return ()


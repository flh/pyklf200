# -*- coding: utf-8 -*-

import socket
import ssl
import struct
import logging
import messages.auth
import messages.general
import asyncio
import inspect
import re

from messages.base import KlfGwResponse

def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)

class KlfConnection:
    """
    Low-level message handling from and to the KLF200 gateway, without
    managing any IO at all.
    """
    INPUT_STATE_INIT = 0
    INPUT_STATE_FRAME = 1
    INPUT_STATE_ESC = 2

    # SLIP escape characters, see RFC1055
    SLIP_END     = b'\xC0'
    SLIP_ESC     = b'\xDB'
    SLIP_ESC_END = b'\xDC'
    SLIP_ESC_ESC = b'\xDD'

    def __init__(self):
        self.frames = []
        self.input_buffer = b''
        self.input_state = self.INPUT_STATE_INIT

    def receive_data(self, data):
        """
        Read and decode frames received from the gateway.
        """
        # Detect when the socket has been closed on the remote side
        if data == '':
            logging.debug("Socket has been closed by the gateway")
            #TODO

        logging.debug("Parsing received data: {data}".format(
            data=toHex(data)))
        for c in data:
            logging.debug("Frame parser: handling byte {byte} in state {state}".format(
                byte=c, state=self.input_state))
            if self.input_state == self.INPUT_STATE_INIT:
                if c == self.SLIP_END[0]:
                    logging.debug("Frame parser: new frame start")
                    self.input_state = self.INPUT_STATE_FRAME

            elif self.input_state == self.INPUT_STATE_FRAME:
                if c == self.SLIP_END[0]:
                    logging.debug("Frame parser: frame end")
                    logging.debug("Frame parser: frame content: {}".format(
                        toHex(self.input_buffer)))
                    self.input_state = self.INPUT_STATE_INIT
                    self.frames.append(KlfGwResponse(self.input_buffer))
                    self.input_buffer = b''
                elif c == self.SLIP_ESC[0]:
                    logging.debug("Frame parser: escape sequence")
                    self.input_state = self.INPUT_STATE_ESC
                else:
                    logging.debug("Frame parser: regular byte")
                    self.input_buffer += bytes([c])

            elif self.input_state == self.INPUT_STATE_ESC:
                self.input_state = self.INPUT_STATE_FRAME
                if c == self.SLIP_ESC_END[0]:
                    self.input_buffer += self.SLIP_END
                elif c == self.SLIP_ESC_ESC[0]:
                    self.input_buffer += self.SLIP_ESC

    def next_event(self):
        try:
            return self.frames.pop(0)
        except IndexError:
            return None

    def iter_events(self):
        while True:
            event = self.next_event()
            if event is not None:
                yield event
            else:
                break

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

    def send(self, message):
        """
        Format a message so that it can be sent to the gateway.
        """
        logging.debug("Sent frame: {frame}".format(
            frame=toHex(bytes(message))))
        return self.slip_pack(bytes(message))

class KlfClient(asyncio.Protocol):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        self.heartbeat_handler = loop.call_later(10 * 60, self.ping)

    def connection_made(self, transport):
        self.transport = transport
        self.klf_connection = KlfConnection()
        self.futures = {}

    def data_received(self, data):
        self.klf_connection.receive_data(data)
        for event in self.klf_connection.iter_events():
            # TODO handle KlfErrorNtf
            if isinstance(event, KlfGwResponse):
                def iter_and_remove(list):
                    while True:
                        try:
                            yield list.pop(0)
                        except IndexError:
                            break
                for future in iter_and_remove(self.futures.get(type(event), [])):
                    future.set_result(event)

    def get_response(self, response_type):
        future = self.loop.create_future()
        self.futures.setdefault(response_type, []).append(future)
        return future

    @staticmethod
    def get_cfm_type(request):
        kls = type(request)
        return getattr(inspect.getmodule(kls), re.sub(r'Req$', 'Cfm', kls.__name__))

    def send(self, message):
        future = self.get_response(KlfClient.get_cfm_type(message))
        self.transport.write(self.klf_connection.send(message))
        return future

    def authenticate(self, password):
        """
        Send password to the gateway and return authentication status
        """
        return self.send(messages.auth.PasswordEnterReq(password))

    def ping(self):
        """
        Send a heartbeat frame to the gateway
        """
        return self.send(messages.general.GetStateReq())

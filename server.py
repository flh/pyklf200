# -*- coding: utf-8 -*-

import socket
import ssl
import struct
from functools import reduce
from operator import xor
import logging


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
                        seen_frames.append(KlfGwResponse(self.input_buffer))
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

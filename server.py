# -*- coding: utf-8 -*-

import socket
import ssl
import struct
from functools import reduce
from operator import xor
import logging


def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)

class KlfBlockingIOError(BlockingIOError):
    """
    Exception raised when received bytes from the gateway are
    insufficient to parse a full command frame.
    """
    pass

class KlfServer:
    INPUT_STATE_INIT = 0
    INPUT_STATE_FRAME = 1
    INPUT_STATE_ESC = 2

    # SLIP escape characters, see RFC1055
    SLIP_END     = b'\xC0'
    SLIP_ESC     = b'\xDB'
    SLIP_ESC_END = b'\xDC'
    SLIP_ESC_ESC = b'\xDD'

    def recv(self):
        """
        Read and decode frames received from the gateway.

        This method returns a list of KlfGwResponse instances, which
        represent frames received from the gateway.

        When the network socket operates in non-blocking mode, this
        method may still raise a KlfBlockingIOError even if it was
        called after a select. This happens when we receive an
        insufficient amount of bytes to parse a single full frame. In
        such cases, the caller should catch the exception and retry
        after another select on the socket.
        """
        seen_frames = []
        try:
            # The length of a KLF200 frame is at most 255 bytes. Since
            # it is encoded using SLIP, the whole SLIP frame length is
            # at most:
            # 512 bytes = 1 (initial SLIP END)
            #             + 255 * 2 (characters all SLIP escaped)
            #             + 1 (final SLIP END)
            data = self.klf_socket.recv(4096)
        except (BlockingIOError, ssl.SSLWantReadError):
            logging.info("No more data to receive from the gateway socket")
            raise KlfBlockingIOError()

        # Detect when the socket has been closed on the remote side
        if data == '':
            logging.debug("Socket has been closed by the gateway")
            return []

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

        # If we received less than a single full frame, we raise an
        # exception to tell that more bytes are needed.
        if seen_frames == []:
            raise KlfBlockingIOError()

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

    def setblocking(self, blocking):
        self.klf_socket.setblocking(blocking)

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

# -*- coding: utf-8 -*-

from server import KlfServer
import selectors
import logging

def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)

def main():
    logging.basicConfig(format='%(asctime)s %(message)s',
            level=logging.DEBUG)
    logging.debug("Here we go!")
    klf_server = KlfServer('klf_ip', b'klf_password')
    klf_server.connect()
    klf_server.enter_password()

    logging.debug("Starting select loop")
    selector = selectors.DefaultSelector()
    selector.register(klf_server, selectors.EVENT_READ)
    while True:
        logging.debug("Waiting for something to happen")
        events = selector.select(timeout=42)

        # Timeout: ping the gateway to keep the connection open
        if not events:
            logging.debug("Sending heartbeat packet to the gateway")
            klf_server.ping()

        for key, mask in events:
            if key == klf_server:
                logging.debug("Handling data from the gateway")
                responses = klf_server.recvall()
                logging.debug("Got {} frames from the gateway".format(len(responses)))
                for resp in responses:
                    print(toHex(resp))

if __name__ == '__main__':
    main()

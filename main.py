# -*- coding: utf-8 -*-

from server import KlfServer, KlfBlockingIOError
import selectors
import logging
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class RestServer(HTTPServer):
    pass

def connect_klf_server(address, password):
    klf_server = KlfServer('klf_ip', b'klf_password')
    klf_server.connect()

    # Authentication on the KLF200 gateway
    klf_server.enter_password()
    auth_response = klf_server.recv()
    if auth_response.status:
        logging.info("Successfully authenticated on the gateway")
    else:
        logging.critical("Cannot authenticate on the gateway: invalid credentials")
        sys.exit(1)

    # Now, go in non-blocking mode
    klf_server.setblocking(False)

    return klf_server

def connect_rest_server():
    rest_server = RestServer(('', '51280'), RestHandler)
    return rest_server

def main():
    logging.basicConfig(format='%(asctime)s %(message)s',
            level=logging.DEBUG)
    logging.debug("Here we go!")

    klf_server = connect_klf_server('klf_ip', b'klf_password')
    rest_server = connect_rest_server()

    logging.debug("Starting select loop")
    selector = selectors.DefaultSelector()
    selector.register(klf_server, selectors.EVENT_READ)
    selector.register(rest_server, selectors.EVENT_READ)

    klf_gateway = KlfGateway()

    while True:
        logging.debug("Waiting for something to happen")
        events = selector.select(timeout=42)

        # Timeout: ping the gateway to keep the connection open
        if not events:
            logging.debug("Sending heartbeat packet to the gateway")
            klf_server.ping()

        for key, mask in events:
            logging.debug("Selector got an event from key {key}".format(key=key))
            if key.fileobj == klf_server:
                logging.debug("Handling data from the gateway")
                responses = klf_server.recvall()
                logging.debug("Got {} frames from the gateway".format(len(responses)))
                for resp in responses:
                    klf_server.handle_response(resp)

            elif key.fileobj == rest_server:
                request, client_address = rest_server.get_request()
                rest_server.process_request(request, client_address)
                pass

if __name__ == '__main__':
    main()

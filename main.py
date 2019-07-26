# -*- coding: utf-8 -*-

from server import KlfServer
import selectors

def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)

def main():
    klf_server = KlfServer('klf_ip', 'klf_password')
    klf_server.connect()
    klf_server.send_password()

    selector = selectors.DefaultSelector()
    selector.register(klf_server, selectors.EVENT_READ)
    while True:
        events = selector.select(timeout=42)

        # Timeout: ping the gateway to keep the connection open
        if not events:
            klf_server.ping()

        for key, mask in events:
            if key == klf_server:
                responses = klf_server.recvall()
                for resp in responses:
                    print(toHex(resp))

if __name__ == '__main__':
    main()

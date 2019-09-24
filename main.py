#!env python3
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

from client import KlfClient
from rest_server import RestClientConnection
import logging
import sys
import asyncio
import ssl

async def connect_klf_client(address, password):
    loop = asyncio.get_running_loop()
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.check_hostname = False
    # The gateway certificate is self-signed.
    ssl_context.verify_mode = ssl.CERT_NONE

    (klf_transport, klf_client) = await loop.create_connection(
            lambda: KlfClient(loop),
            host=address, port=51200, ssl=ssl_context)
    if await klf_client.authenticate(password):
        logging.info("Successfully authenticated on the gateway")
    else:
        logging.critical("Cannot authenticate on the gateway: invalid credentials")
        sys.exit(1)

    return klf_client

async def connect_rest_server(klf_client):
    logging.info("Starting REST server")
    rest_server = await asyncio.start_server(lambda reader, writer:
            RestClientConnection(reader, writer, klf_client).run(),
            '', 52280)
    logging.info("REST server waiting for incoming connections")
    return rest_server

async def main():
    logging.basicConfig(format='%(asctime)s %(message)s',
            level=logging.DEBUG)
    logging.debug("Here we go!")

    klf_client = await connect_klf_client('klf_ip', b'klf_password')
    rest_server = await connect_rest_server(klf_client)

    async with rest_server:
        await rest_server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())

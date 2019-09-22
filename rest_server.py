# -*- coding: utf-8 -*-

import json
import re
import h11
import asyncio
import logging
import messages.info

class RestClientConnection(asyncio.Protocol):
    """
    Client connection handling. One should instance a new object for
    each client connection then call the run coroutine which will handle
    client requests.
    """
    def __init__(self, reader, writer, klf_client):
        logging.info("Client connected to the REST server")
        self.reader = reader
        self.writer = writer
        self.klf_client = klf_client
        self.connection = h11.Connection(h11.SERVER)

    async def run(self):
        """
        Receive client requests, forward them to the KLF gateway client
        and build responses.
        """
        while True:
            self.connection.receive_data(await self.reader.read(100))

            while True:
                event = self.connection.next_event()

                if isinstance(event, h11.Request):
                    if event.method == b'GET':
                        await self.handle_GET(event)
                    elif event.method == b'POST':
                        await self.handle_POST(event)
                    else:
                        # Method not allowed
                        await self.method_not_allowed()

                elif isinstance(event, h11.ConnectionClosed) \
                        or event is h11.NEED_DATA \
                        or event is h11.PAUSED:
                    break

            if self.connection.our_state is h11.MUST_CLOSE:
                self.writer.close()
                await self.writer.wait_closed()
            # TODO when should we exit the main loop?

    async def write_simple_response(self, status_code=200, reason=b'OK',
            headers=(), body={}):
        data = h11.Data(json.dumps(body).encode('utf-8'))
        response = h11.Response(status_code=status_code,
                headers=headers + (
                    ('Content-type', 'application/json; encoding=utf-8'),
                    ('Content-length', len(data)),
                ), reason=reason)
        self.writer.write(self.connection.send(response) + self.connection.send(data) +
                self.connection.send(h11.EndOfMessage()))
        await self.writer.drain()

    async def method_not_allowed(self):
        await self.write_simple_response(
                status_code=405,
                reason=b'Method not allowed',
                headers=(('Allow', 'GET, POST'),),
                body={'status': 'error', 'reason': 'HTTP method not allowed'})

    async def handle_GET(self, request):
        actuator_match = re.match(b'/actuator/(?:(?P<node_id>\d+)/)?$',
                request.target)
        if actuator_match is not None:
            await self.actuator_GET(node_id=actuator_match.group('node_id'))

    async def handle_POST(self, request):
        actuator_match = re.match(b'/actuator/(?:(?P<node_id>\d+)/)?$',
                request.path)
        if actuator_match is not None:
            await self.actuator_POST(node_id=actuator_match.group('node_id'))

    async def actuator_GET(self, node_id=None):
        """
        Request for actuator information. When node_id is None, the full
        list of actuators is returned.
        """
        logging.info("Asking all nodes information to the KLF gateway")
        information_ntf = self.klf_client.get_response(messages.info.GetAllNodesInformationNtf)
        finished_ntf = self.klf_client.get_response(messages.info.GetAllNodesInformationFinishedNtf)
        await self.klf_client.send(messages.info.GetAllNodesInformationReq())

        event = None
        klf_nodes = []
        logging.info("Waiting for all nodes information")
        while event != finished_ntf:
            event, _ = await asyncio.wait((information_ntf, finished_ntf),
                    return_when=asyncio.FIRST_COMPLETED)
            if event == information_ntf:
                logging.info("Got one frame in response to all nodes information")
                information_ntf = self.klf_client.get_response(messages.info.GetAllNodesInformationNtf)
                node_info = event.result()
                klf_nodes.append({
                    'id': node_info.node_id,
                    'name': node_info.name,
                    })
            elif event == finished_ntf:
                logging.info("Got final frame in response to all nodes information")
                information_ntf.cancel()

        # Response to the HTTP request
        await self.write_simple_response(body=klf_nodes)

    async def actuator_POST(request, node_id=None):
        pass

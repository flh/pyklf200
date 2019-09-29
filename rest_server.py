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

import json
import re
import h11
import asyncio
import logging
import messages.info
import messages.general

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
            event = None
            current_request = None

            while not (isinstance(event, h11.ConnectionClosed)
                    or event is h11.NEED_DATA
                    or event is h11.PAUSED):

                event = self.connection.next_event()

                if isinstance(event, h11.Request):
                    if event.method == b'GET':
                        await self.handle_GET(event)
                    elif event.method == b'POST':
                        current_request = event
                        current_request.body = b''
                    else:
                        # Method not allowed
                        await self.method_not_allowed()

                elif isinstance(event, h11.Data):
                    current_request.body += event.data

                elif isinstance(event, h11.EndOfMessage) and \
                        isinstance(current_request, h11.Request) and \
                        current_request.method == b'POST':
                    await self.handle_POST(current_request)
                    current_request = None

            if self.connection.our_state is h11.MUST_CLOSE:
                self.writer.close()
                await self.writer.wait_closed()
                return

    async def write_simple_response(self, status_code=200, reason=b'OK',
            headers=(), body={}):
        data = h11.Data(data=json.dumps(body).encode('utf-8'))
        response = h11.Response(status_code=status_code,
                headers=headers + (
                    ('Content-type', 'application/json; encoding=utf-8'),
                    ('Content-length', str(len(data.data))),
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

    @staticmethod
    def find_handler(url_patterns, request):
        for url_pattern, url_handler in url_patterns:
            url_match = re.fullmatch(url_pattern, request.target)
            if url_match is not None:
                return url_handler(request, **url_match.groupdict())
        return None

    async def internal_error(self, request):
        await self.write_simple_response(status_code=500,
                reason='Internal server error',
                body={'status': 'error'})

    async def handle_not_found(self, request):
        await self.write_simple_response(status_code=404,
            reason=b'Not found',
            body={'status': 'error'})

    async def handle_GET(self, request):
        try:
            url_handler = self.find_handler((
                (b'/actuator/(?:(?P<node_id>\d+)/)?$', self.GET_actuator),
                (b'/version/?', self.GET_gateway_version),
                (b'/network_setup/?', self.GET_network_setup),
                (b'/clock/?', self.GET_clock),
            ), request)
            if url_handler is not None:
                await url_handler
            else:
                await self.handle_not_found(request)
        except:
            await self.internal_error(request)

    async def handle_POST(self, request):
        try:
            url_handler = self.find_handler((
                (b'/actuator/(?:(?P<node_id>\d+)/)?$', self.POST_actuator),
                (b'/config/controller_copy/?', self.POST_controller_copy),
                (b'/clock/?', self.POST_clock),
            ), request)
            if url_handler is not None:
                await url_handler
            else:
                await self.handle_not_found(request)
        except:
            await self.internal_error(request)

    async def GET_actuator(self, request, node_id=None):
        """
        Request for actuator information. When node_id is None, the full
        list of actuators is returned.
        """
        logging.info("Asking all nodes information to the KLF gateway")
        information_ntf = self.klf_client.get_response(messages.info.GetAllNodesInformationNtf)
        finished_ntf = self.klf_client.get_response(messages.info.GetAllNodesInformationFinishedNtf)
        await self.klf_client.send(messages.info.GetAllNodesInformationReq())

        finished_event = None
        klf_nodes = []
        logging.info("Waiting for all nodes information")
        while finished_event != finished_ntf:
            events, _ = await asyncio.wait((information_ntf, finished_ntf),
                    return_when=asyncio.FIRST_COMPLETED)
            for event in events:
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
                    finished_event = finished_ntf

        # Response to the HTTP request
        await self.write_simple_response(body=klf_nodes)

    async def POST_actuator(self, request, node_id=None):
        pass

    async def POST_controller_copy(self, request):
        body_json = json.loads(request.body)
        copy_mode = body.json.get('copy_mode')
        if copy_mode == 'rcm':
            message_copy_mode = messages.config.CsControllerCopyReq.COPY_MODE_RCM
        elif copy_mode == 'tcm':
            message_copy_mode = messages.config.CsControllerCopyReq.COPY_MODE_TCM
        else:
            await self.write_simple_response(body={
                    'error': "Unhandled value for copy_mode"},
                status_code=400)

        copy_ntf = self.klf_client.get_response(messages.config.CsControllerCopyNtf)
        await self.klf_client.send(messages.config.CsControllerCopyReq(message_copy_mode))
        copy_status = await copy_ntf
        await self.write_simple_response(body={
            'copy_mode': copy_status.controller_copy_mode,
            'copy_status': copy_status.controller_copy_status,
        })

    async def GET_gateway_version(self, request):
        firmware_version_info = await self.klf_client.send(messages.general.GetVersionReq())
        protocol_version_info = await self.klf_client.send(messages.general.GetProtocolVersionReq())
        await self.write_simple_response(body={
            'software_version': list(firmware_version_info.software_version),
            'hardware_version': firmware_version_info.hardware_version,
            'product_group': firmware_version_info.product_group,
            'product_type': firmware_version_info.product_type,
            'protocol_major_version': protocol_version_info.major_version,
            'protocol_minor_version': protocol_version_info.minor_version,
        })

    async def GET_network_setup(self, request):
        network_info = await self.klf_client.send(messages.general.GetNetworkSetupReq())
        await self.write_simple_response(body={
            'ip_address': str(network_info.ip_address),
            'mask': str(network_info.mask),
            'default_gw': str(network_info.default_gw),
            'use_dhcp': network_info.use_dhcp
        })

    async def GET_clock(self, request):
        clock_info = await self.klf_client.send(messages.general.GetLocalTimeReq())
        await self.write_simple_response(body={
            'time': clock_info.utc_time.isoformat(),
            'localtime': clock_info.local_time.isoformat(),
            'dst_flag': clock_info.dst_flag,
        })

    async def POST_clock(self, request):
        json_body = json.loads(request.body)
        clock_cfm = await self.klf_client.send(messages.general.SetUTCReq())
        timezone = json_body.get('timezone')
        if timezone is not None:
            tz_cfm = await self.klf_client.send(messages.general.RtcSetTimeZoneReq(timezone.encode('utf-8')))
            if tz_cfm.is_success:
                await self.write_simple_response(body={
                    'status': 'done',
                })
            else:
                await self.write_simple_response(status_code=500, body={
                    'status': 'fail',
                })
            return

        await self.write_simple_response(body={
                'status': 'done',
            })

#!/usr/bin/env python

"""
Copyright (c) 2013, Luke Fitzgerald
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project."""

import asyncio
import logging
import socket
import struct


HELLO_STR = "hello-000"

HEADER_STRUCT = struct.Struct("<B21s21sBBH")

COMMAND_MAP = {
    "NULL": 0,
    "SET": 1,
    "GET": 2,
    "IO": 3,
    "KEEPALIVE": 4,
    "RSS": 5,
    "RCU": 6,
}

SOCKET_TIMEOUT = 1


class DXPCommand(object):
    COMMAND = None
    DESCRIPTOR_MAP = None
    DESCRIPTOR = None
    PAYLOAD_STRUCT = None

    def __init__(self, interface):
        self.interface = interface

    def _build_header(self):
        if not self.COMMAND:
            raise Exception("'COMMAND' type not specified for class")

        if not self.DESCRIPTOR_MAP:
            raise Exception("'DESCRIPTOR_MAP' not specified for class")

        if not self.DESCRIPTOR:
            raise Exception("'DESCRIPTOR' type not specified for class")

        return HEADER_STRUCT.pack(
            COMMAND_MAP[self.COMMAND],
            bytes(self.interface.username, "utf-8"),
            bytes(self.interface.password, "utf-8"),
            self.DESCRIPTOR_MAP[self.DESCRIPTOR],
            0,
            self.interface.get_seq_num(),
        )

    def _build_payload(self, *pack_args):
        if not self.PAYLOAD_STRUCT:
            raise Exception("'PAYLOAD_STRUCT' not specified for class")

        return self.PAYLOAD_STRUCT.pack(*pack_args)

    async def _get_response(self, socket):
        """
        Parse the response from the request
        """
        raise Exception("get_response method not implemented")

    async def _get_boolean_response(self):
        # response = self.interface.socket.recv(1)
        response = await self.interface.loop.sock_recv(self.interface.socket, 1)
        if not response:
            return False

        self.interface.increment_seq_num()
        return self._parse_bool(response)

    def _parse_bool(self, string):
        return not struct.unpack("?", string)[0]

    async def do_request(self):
        header = self._build_header()
        payload = self._build_payload()
        request = header + payload
        # self.interface.socket.sendall(request)
        # self.interface.socket.sendall(bytes(request, 'utf-8'))
        await self.interface.loop.sock_sendall(self.interface.socket, request)

        return await self._get_response()

    async def _do_payloadless_request(self):
        request = self._build_header()
        # self.interface.socket.sendall(request)
        # self.interface.socket.sendall(bytes(request, 'utf-8'))
        await self.interface.loop.sock_sendall(self.interface.socket, request)
        return await self._get_response()


class IOCommand(DXPCommand):
    COMMAND = "IO"
    DESCRIPTOR_MAP = {
        "NULL": 0,
        "CHANGE_RELAY": 1,
        "CHANGE_RELAYS": 2,
        "GET_RELAY": 3,
        "GET_RELAYS": 4,
        "GET_INPUT": 5,
        "GET_INPUTS": 6,
        "PULSE_RELAY": 7,
    }


class RelayCommand(IOCommand):
    STATE_MAP = {True: 1, False: 0, "NO_CHANGE": 2}

    async def _get_response(self):
        return await self._get_boolean_response()


class ChangeRelayCommand(RelayCommand):
    DESCRIPTOR = "CHANGE_RELAY"
    PAYLOAD_STRUCT = struct.Struct("<BB")

    def __init__(self, interface, relay, state):
        super(ChangeRelayCommand, self).__init__(interface)
        self.relay = relay
        self.state = state

    def _build_payload(self):
        return super(ChangeRelayCommand, self)._build_payload(
            self.relay, self.STATE_MAP[self.state]
        )


class ChangeRelaysCommand(RelayCommand):
    DESCRIPTOR = "CHANGE_RELAYS"
    PAYLOAD_STRUCT = struct.Struct("<" + ("B" * 32))  # 32 unsigned chars

    def __init__(self, interface, relay_state_dict):
        super(ChangeRelaysCommand, self).__init__(interface)
        self.relay_state_dict = relay_state_dict

    def _build_payload(self):
        state_list = []

        self.interface.logger.debug(self.relay_state_dict)

        for relay in range(32):
            if (relay + 1) not in self.relay_state_dict:
                state_list.append(self.STATE_MAP["NO_CHANGE"])
            else:
                state_list.append(self.STATE_MAP[self.relay_state_dict[relay + 1]])

        self.interface.logger.debug(state_list)

        return super(ChangeRelaysCommand, self)._build_payload(*state_list)


class GetRelaysRequest(IOCommand):
    DESCRIPTOR = "GET_RELAYS"

    async def do_request(self):
        return await self._do_payloadless_request()

    async def _get_response(self):
        # response = self.interface.socket.recv(self.interface.num_relays)
        response = await self.interface.loop.sock_recv(
            self.interface.socket, self.interface.num_relays
        )
        if not response:
            return None

        self.interface.increment_seq_num()
        # return [True if ord(str(relay_status)) == 1 else False
        return [True if relay_status == 1 else False for relay_status in response]


class PulseRelayRequest(RelayCommand):
    DESCRIPTOR = "PULSE_RELAY"
    PAYLOAD_STRUCT = struct.Struct("<BBH")

    def __init__(self, interface, relay, state, width):
        super(PulseRelayRequest, self).__init__(interface)
        self.relay = relay
        self.state = state
        self.width = width

    def _build_payload(self):
        return super(PulseRelayRequest, self)._build_payload(
            self.relay, self.STATE_MAP[self.state], self.width
        )


class iBootInterface(object):
    def __init__(self, ip, username, password, num_relays=3, log=None, port=9100):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.num_relays = num_relays
        self.seq_num = None
        self.socket = None
        if log:
            self.logger = log
        else:
            logging.basicConfig()
            self.logger = logging.getLogger("iBootInterface")
            self.logger.setLevel(logging.DEBUG)
        self.loop = asyncio.get_event_loop()

    def get_seq_num(self):
        seq_num = self.seq_num
        self.seq_num += 1
        return seq_num

    def increment_seq_num(self):
        self.seq_num += 1

    async def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(SOCKET_TIMEOUT)

        try:
            # self.socket.connect((self.ip, self.port))
            await self.loop.sock_connect(self.socket, (self.ip, self.port))
        except socket.error:
            self.logger.error("Socket failed to connect")
            return False

        try:
            # self.socket.sendall(bytes(HELLO_STR, 'utf-8'))
            await self.loop.sock_sendall(self.socket, bytes(HELLO_STR, "utf-8"))
            return await self._get_initial_seq_num()
        except socket.error:
            self.logger.error("Socket error")
            return False

        return True

    async def _get_initial_seq_num(self):
        # response = self.socket.recv(2)
        response = await self.loop.sock_recv(self.socket, 2)

        if not response:
            return False

        self.seq_num = struct.unpack("H", response)[0] + 1
        return True

    def disconnect(self):
        try:
            self.socket.close()
        except socket.error:
            pass

    async def switch(self, relay, on):
        """Switch the given relay on or off"""
        await self.connect()
        request = ChangeRelayCommand(self, relay, on)

        try:
            return await request.do_request()
        except socket.error:
            return False
        finally:
            self.disconnect()

    async def switch_multiple(self, relay_state_dict):
        """
        Change the state of multiple relays at once

        State dictionary should be of the form:
            {1: True}
        where the key is the relay and the value is the new state
        """
        await self.connect()

        for relay, new_state in list(relay_state_dict.items()):
            request = ChangeRelayCommand(self, relay, new_state)

            try:
                result = await request.do_request()

                if not result:
                    return False
            except socket.error:
                self.disconnect()
                return False

        self.disconnect()
        return True

    async def get_relays(self):
        await self.connect()
        request = GetRelaysRequest(self)

        try:
            return await request.do_request()
        except socket.error:
            return False
        finally:
            self.disconnect()

    async def pulse_relay(self, relay, on, length):
        await self.connect()
        request = PulseRelayRequest(self, relay, on, length)

        try:
            return await request.do_request()
        except socket.error:
            return False
        finally:
            self.disconnect()


if __name__ == "__main__":
    interface = iBootInterface("192.168.0.105", "admin", "admin")
    print(str(interface.get_relays()))
    print(str(interface.switch(1, False)))

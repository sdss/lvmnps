import asyncio
import logging
import sys

import pytest
#from asynctest import CoroutineMock

from clu import REPLY, AMQPActor, CluError, CommandError
from clu.client import AMQPReply
from clu.model import Model


#pytestmark = [pytest.mark.asyncio]

#@pytest.fixture(scope="session")
#def event_loop():
    #return asyncio.get_event_loop()


#@pytest.fixture
#def message_maker(mocker):
    #def _make_message(headers=None, body=None):

        #headers = headers or {"command_id": 1, "message_code": "i", "sender": "me"}

        #message = mocker.MagicMock()
        #message.correlation_id = headers["command_id"]
        #message.info.return_value = {"headers": headers}
        #message.body = b"{}"

        #return message

    #yield _make_message


#def test_actor(amqp_actor):

    #assert amqp_actor.name == "amqp_actor"


#async def test_client_send_command(amqp_client, amqp_actor):

    #cmd = await amqp_client.send_command("amqp_actor", "ping")
    #await cmd

    #assert len(cmd.replies) == 2
    #assert cmd.replies[-1].message_code == ":"
    #assert cmd.replies[-1].body["text"] == "Pong."


#async def test_client_send_command_args(amqp_client, amqp_actor):

    #cmd = await amqp_client.send_command("amqp_actor", "ping", "--help")
    #await cmd

    #assert len(cmd.replies) == 2
    #assert cmd.replies[-1].message_code == ":"
    #assert "help" in cmd.replies[-1].body


#async def test_get_version(amqp_client, amqp_actor):

    #cmd = await amqp_client.send_command("amqp_actor", "version")
    #await cmd

    #assert len(cmd.replies) == 2
    #assert cmd.replies[-1].message_code == ":"
    #assert cmd.replies[-1].body["version"] == "?"

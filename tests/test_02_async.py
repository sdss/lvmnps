import asyncio
import os

import pytest
from clu import JSONActor
from clu.testing import setup_test_actor

from lvmnps.actor.actor import lvmnps as NpsActor
from sdsstools.logger import get_logger

from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory



@pytest.mark.asyncio
async def test_actor(actor: NpsActor):


    # status check of nps_dummy_1 port1
    assert actor
    
    command = await actor.invoke_mock_command("status slow 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["slow"]["slow"]["state"] == -1
    
    command = await actor.invoke_mock_command("status fast 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["fast"]["fast"]["state"] == -1

    task = []
    task.append(asyncio.create_task(actor.invoke_mock_command("on slow 1")))
    task.append(asyncio.create_task(actor.invoke_mock_command("on fast 1")))

    status = await asyncio.gather(*task)
    
    status_task = []
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status slow 1")))
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status fast 1")))
    
    status_before = await asyncio.gather(*status_task)
    assert status_before[0].replies[-2].message["status"]["slow"]["slow"]["state"] == -1
    assert status_before[1].replies[-2].message["status"]["fast"]["fast"]["state"] == 1

    await asyncio.sleep(2)
    
    status_task = []
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status slow 1")))
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status fast 1")))
    
    status_after = await asyncio.gather(*status_task)
    assert status_after[0].replies[-2].message["status"]["slow"]["slow"]["state"] == 1
    assert status_after[1].replies[-2].message["status"]["fast"]["fast"]["state"] == 1
    
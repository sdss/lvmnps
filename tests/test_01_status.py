import os

import pytest
from clu.testing import setup_test_actor

from sdsstools.logger import get_logger

from lvmnps.actor.actor import lvmnps as NpsActor
from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory

@pytest.mark.asyncio
async def test_actor(actor: NpsActor):

    # status check of nps_dummy_1 port1
    assert actor
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == -1
    
    # switch on nps_dummy_1 port1
    command = await actor.invoke_mock_command("on nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 1
    
    # switch off nps_dummy_1 port1
    command = await actor.invoke_mock_command("off nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0

    # switch status
    command = await actor.invoke_mock_command("status skye.nps")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    
    print(command.replies[-2].message)
    assert command.replies[-2].message["status"]["skye.nps"]["skye.pwi"]["state"] == -1
    
    # switch on skye.nps port1
    command = await actor.invoke_mock_command("on skye.nps 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["skye.nps"]["skye.pwi"]["state"] == 1
    
     # switch off skye.nps port1
    command = await actor.invoke_mock_command("off skye.nps 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["skye.nps"]["skye.pwi"]["state"] == 0   
    
    # switch status
    command = await actor.invoke_mock_command("status nps_dummy_1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0
    assert command.replies[-2].message["status"]["nps_dummy_1"]["skye.what.ever"]["state"] == -1
    assert command.replies[-2].message["status"]["nps_dummy_1"]["skyw.what.ever"]["state"] == -1

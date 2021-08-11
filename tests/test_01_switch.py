import os

import pytest
from clu import JSONActor
from clu.testing import setup_test_actor

from sdsstools.logger import get_logger

from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory


@pytest.fixture
def switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "test_01_switch.yml")
    default_config = JSONActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, config) in default_config["switches"].items():
        print(f"Switch {name}: {config}")
        try:
            switches.append(powerSwitchFactory(name, config, get_logger("test")))

        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


async def send_command(actor, command_string):
    command = actor.invoke_mock_command(command_string)
    await command
    assert command.status.is_done
    assert actor.mock_replies[-1]["text"] == "done"

    status_reply = actor.mock_replies[-2]
    return status_reply["STATUS"]


@pytest.mark.asyncio
async def test_actor(switches):

    test_actor = await setup_test_actor(JSONActor("lvmnp", host="localhost", port=9999))

    test_actor.parser = nps_command_parser
    test_actor.parser_args = [switches]

    status = await send_command(test_actor, "status what nps_dummy_1.port1")
    assert len(status) == 1
    assert status["nps_dummy_1.port1"]["STATE"] == -1

    # switch nps_dummy_1 port1 'on'
    status = await send_command(test_actor, "on nps_dummy_1.port1")
    assert status["nps_dummy_1.port1"]["STATE"] == 1


"""
    # switch all ports on  nps_dummy_1 on
    status = await send_command(test_actor, "on nps_dummy_1")
    assert status["nps_dummy_1.port1"]["STATE"] == 1
    assert status["skye.what.ever"]["STATE"] == 1
    assert status["skyw.what.ever"]["STATE"] == 1

    # switch off port 4 on nps_dummy_1
    status = await send_command(test_actor, "off nps_dummy_1 4")

    status = await send_command(test_actor, "status")
    assert status["nps_dummy_1.port1"]["STATE"] == 1
    assert status["skye.what.ever"]["STATE"] == 1
    assert status["skyw.what.ever"]["STATE"] == 0
    assert status["skye.pwi"]["STATE"] == -1
    assert status["skyw.pwi"]["STATE"] == -1

    # switch off everything - same as command offall
    status = await send_command(test_actor, "off")
    assert status["nps_dummy_1.port1"]["STATE"] == 0
    assert status["skye.what.ever"]["STATE"] == 0
    assert status["skyw.what.ever"]["STATE"] == 0
    assert status["skye.pwi"]["STATE"] == 0
    assert status["skyw.pwi"]["STATE"] == 0
"""

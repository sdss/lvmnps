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
    # assert command.status.is_done

    switch_num = len(actor.parser_args[0])
    status_all_reply = []
    # assert actor.mock_replies[-1]["text"] == "done"
    status_reply = actor.mock_replies[-2]

    if command_string == "status":
        length = len(actor.mock_replies)
        print(
            actor.mock_replies[
                length - 2 : length - switch_num * 2 - 1 : -2  # noqa: E203
            ]
        )
        status_all_reply = actor.mock_replies[
            length - 2 : length - switch_num * 2 - 1 : -2  # noqa: E203
        ]
        status_all_reply.reverse()
        return status_all_reply
    else:
        return status_reply["status"]


@pytest.mark.asyncio
async def test_actor(amqp_actor, switches):

    test_actor = await setup_test_actor(JSONActor("lvmnps", host="localhost", port=9999))

    test_actor.parser = nps_command_parser
    test_actor.parser_args = [switches]

    # status what port unit
    status = await send_command(test_actor, "status nps_dummy_1 1")
    assert len(status) == 1
    assert status["nps_dummy_1"]["port1"]["state"] == -1

    # switch on nps_dummy_1 port1
    status = await send_command(test_actor, "on nps_dummy_1 1")
    assert status["nps_dummy_1"]["port1"]["state"] == 1

    # switch off nps_dummy_1 port1
    status = await send_command(test_actor, "off nps_dummy_1 1")
    assert status["nps_dummy_1"]["port1"]["state"] == 0

    # switch skye.nps skye.pwi 'on'
    status = await send_command(test_actor, "on skye.pwi")
    assert status["skye.nps"]["skye.pwi"]["state"] == 1

    # switch off skye.nps skye.pwi
    status = await send_command(test_actor, "off skye.pwi")
    assert status["skye.nps"]["skye.pwi"]["state"] == 0

    # switch status
    status = await send_command(test_actor, "status skye.nps 1")
    assert status["skye.nps"]["skye.pwi"]["state"] == 0

    # status what switch unit
    status = await send_command(test_actor, "status nps_dummy_3")
    assert status["nps_dummy_3"]["skyw.pwi"]["state"] == -1

    # switch status
    status = await send_command(test_actor, "status")
    print(f"status is {status[2]}")
    assert status[2]["status"]["nps_dummy_1"]["port1"]["state"] == 0
    assert status[2]["status"]["nps_dummy_1"]["skye.what.ever"]["state"] == -1
    assert status[2]["status"]["nps_dummy_1"]["skyw.what.ever"]["state"] == -1
    assert status[2]["status"]["skye.nps"]["skye.pwi"]["state"] == 0
    assert status[0]["status"]["nps_dummy_3"]["skyw.pwi"]["state"] == -1

    # switch all ports on  nps_dummy_1 on
    # status = await send_command(test_actor, "on nps_dummy_1")
    # assert status["nps_dummy_1.port1"]["state"] == 1
    # assert status["skye.what.ever"]["state"] == 1
    # assert status["skyw.what.ever"]["state"] == 1

    # switch off everything - same as command offall
    # status = await send_command(test_actor, "off")
    # assert status["nps_dummy_1.port1"]["state"] == 0
    # assert status["skye.what.ever"]["state"] == 0
    # assert status["skyw.what.ever"]["state"] == 0
    # assert status["skye.pwi"]["state"] == 0
    # assert status["skyw.pwi"]["state"] == 0

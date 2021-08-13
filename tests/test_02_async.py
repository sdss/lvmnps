import asyncio
import os

import pytest
from clu import JSONActor
from clu.testing import setup_test_actor

from sdsstools.logger import get_logger

from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory


@pytest.fixture
def switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "test_02_async.yml")
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

    # print("number of swithces are ",len(actor.parser_args[0]))
    switch_num = len(actor.parser_args[0])
    status_all_reply = []
    assert actor.mock_replies[-1]["text"] == "done"
    status_reply = actor.mock_replies[-2]
    # print(status_reply)
    if command_string == "status all":
        length = len(actor.mock_replies)
        print(
            actor.mock_replies[length - 2 : length - switch_num * 2 - 1 : -2]  # noqa: E203
        )  # noqa: E203
        status_all_reply = actor.mock_replies[
            length - 2 : length - switch_num * 2 - 1 : -2  # noqa: E203
        ]
        status_all_reply.reverse()
        return status_all_reply
    else:
        return status_reply["STATUS"]


@pytest.mark.asyncio
async def test_actor(switches):

    test_actor = await setup_test_actor(
        JSONActor("lvmnps", host="localhost", port=9999)
    )

    test_actor.parser = nps_command_parser
    test_actor.parser_args = [switches]

    task = []
    task.append(asyncio.create_task(send_command(test_actor, "on slow")))
    task.append(asyncio.create_task(send_command(test_actor, "on fast")))

    await asyncio.sleep(0.2)

    status_task = []
    status_task.append(asyncio.create_task(send_command(test_actor, "status all")))

    status = await asyncio.gather(*status_task)
    # print(status)
    # assert status[0][0]["STATE"] == -1
    # assert status[0]["fast"]["fast"]["STATE"] == -1

    status_after = await asyncio.gather(*task)
    assert status_after[0]["slow"]["slow"]["STATE"] == 1
    assert status_after[1]["fast"]["fast"]["STATE"] == 1

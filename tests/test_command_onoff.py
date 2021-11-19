import pytest


# from lvmnps.actor.actor import lvmnps as NpsActor


pytestmark = [pytest.mark.asyncio]

"""
async def test_on(actor: NpsActor):
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    print(command.replies[2].message)

    # assert len(command.replies) == 1

    command = await actor.invoke_mock_command("on nps_dummy_1 1")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    print(command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"])
    assert command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"] == 1


async def test_off(actor: NpsActor):
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    print(command.replies[2].message)

    # assert len(command.replies) == 1

    command = await actor.invoke_mock_command("on nps_dummy_1 1")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    print(command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"])
    assert command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"] == 1

    command = await actor.invoke_mock_command("off nps_dummy_1 1")
    await command
    assert command.status.did_succeed

    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    print(command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"])
    assert command.replies[2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0
"""

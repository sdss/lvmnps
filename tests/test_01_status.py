import pytest

from lvmnps.actor.actor import lvmnps as NpsActor


@pytest.mark.asyncio
async def test_status(switches, actor: NpsActor):

    # status check of nps_dummy_1 port1
    assert actor
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == -1

    assert switches[0].name == "nps_dummy_1"
    assert switches[0].outlets[0].name == "port1"
    assert switches[0].outlets[0].state == -1
    switches[0].outlets[0].state = 0
    assert switches[0].outlets[0].state == 0

    # status check of nps_dummy_1 port1
    assert actor
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4
    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0

    # switch status
    command = await actor.invoke_mock_command("status nps_dummy_1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 4

    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0
    assert (
        command.replies[-2].message["status"]["nps_dummy_1"]["skye.what.ever"]["state"]
        == -1  # noqa: W503
    )
    assert (
        command.replies[-2].message["status"]["nps_dummy_1"]["skyw.what.ever"]["state"]
        == -1  # noqa: W503
    )

    # status of all available switches
    command = await actor.invoke_mock_command("status")
    await command
    assert command.status.did_succeed

    assert command.replies[-2].message["status"]["nps_dummy_1"]["port1"]["state"] == 0
    assert (
        command.replies[-2].message["status"]["nps_dummy_1"]["skye.what.ever"]["state"]
        == -1  # noqa: W503
    )
    assert (
        command.replies[-2].message["status"]["nps_dummy_1"]["skyw.what.ever"]["state"]
        == -1  # noqa: W503
    )

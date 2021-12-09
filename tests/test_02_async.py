import asyncio

import pytest

from lvmnps.actor.actor import lvmnps as NpsActor


@pytest.mark.asyncio
async def test_async_onoff(switches, actor: NpsActor):

    # status check of nps_dummy_1 port1
    assert actor

    assert switches[3].name == "slow"
    assert switches[3].outlets[0].name == "slow"
    assert switches[3].outlets[0].state == -1
    switches[3].outlets[0].state = 0
    assert switches[3].outlets[0].state == 0

    assert switches[4].name == "fast"
    assert switches[4].outlets[0].name == "fast"
    assert switches[4].outlets[0].state == -1
    switches[4].outlets[0].state = 0
    assert switches[4].outlets[0].state == 0

    task = []
    task.append(asyncio.create_task(actor.invoke_mock_command("on slow 1")))
    task.append(asyncio.create_task(actor.invoke_mock_command("on fast 1")))

    await asyncio.gather(*task)

    status_task = []
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status slow 1")))
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status fast 1")))

    status_before = await asyncio.gather(*status_task)
    assert status_before[0].replies[-2].message["status"]["slow"]["slow"]["state"] == 0
    assert status_before[1].replies[-2].message["status"]["fast"]["fast"]["state"] == 1

    await asyncio.sleep(2)

    status_task = []
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status slow 1")))
    status_task.append(asyncio.create_task(actor.invoke_mock_command("status fast 1")))

    status_after = await asyncio.gather(*status_task)
    assert status_after[0].replies[-2].message["status"]["slow"]["slow"]["state"] == 1
    assert status_after[1].replies[-2].message["status"]["fast"]["fast"]["state"] == 1

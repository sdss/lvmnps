#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from lvmnps.actor.actor import NPSActor


async def test_status(switches, actor: NPSActor):

    # status check of nps_dummy_1 port1
    assert actor
    command = await actor.invoke_mock_command("status nps_dummy_1 1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 2
    assert command.replies[-1].message["status"]["nps_dummy_1"]["port1"]["state"] == -1

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
    assert len(command.replies) == 2
    assert command.replies[-1].message["status"]["nps_dummy_1"]["port1"]["state"] == 0

    # switch status
    command = await actor.invoke_mock_command("status nps_dummy_1")
    await command
    assert command.status.did_succeed
    assert len(command.replies) == 2

    status = command.replies[-1].message["status"]
    assert status["nps_dummy_1"]["port1"]["state"] == 0
    assert status["nps_dummy_1"]["skye.what.ever"]["state"] == -1
    assert status["nps_dummy_1"]["skyw.what.ever"]["state"] == -1

    # status of all available switches
    command = await actor.invoke_mock_command("status")
    await command
    assert command.status.did_succeed
    status = command.replies[-1].message["status"]

    assert status["nps_dummy_1"]["port1"]["state"] == 0
    assert status["nps_dummy_1"]["skye.what.ever"]["state"] == -1
    assert status["nps_dummy_1"]["skyw.what.ever"]["state"] == -1

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from lvmnps.actor.actor import lvmnps as NpsActor


async def test_actor(actor: NpsActor):

    assert actor


async def test_reachable(actor: NpsActor):

    # check the reachable switches command
    command = await actor.invoke_mock_command("reachable switches")
    await command

    assert command.status.did_succeed
    assert command.replies[-2].message["switches"][0] == "nps_dummy_1"
    assert command.replies[-2].message["switches"][1] == "skye.nps"
    assert command.replies[-2].message["switches"][2] == "nps_dummy_3"
    assert command.replies[-2].message["switches"][3] == "slow"
    assert command.replies[-2].message["switches"][4] == "fast"

    # check the reachable outlets command
    command = await actor.invoke_mock_command("reachable outlets nps_dummy_1")
    await command
    assert command.status.did_succeed
    assert command.replies[-2].message["outlets"][0] == "port1"

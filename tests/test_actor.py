#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import pytest

from lvmnps.actor.actor import AMQPActor, NPSActor


async def test_actor(actor: NPSActor):

    assert actor


async def test_ping(actor: NPSActor):

    command = await actor.invoke_mock_command("ping")
    await command

    assert command.status.did_succeed
    assert len(command.replies) == 2
    assert command.replies[1].message["text"] == "Pong."


async def test_actor_no_config():

    with pytest.raises(RuntimeError):
        NPSActor.from_config(None)


async def test_actor_start(switches, test_config: dict, mocker):

    actor = NPSActor.from_config(test_config)
    mocker.patch.object(AMQPActor, "start")

    actor.parser_args = [{switch.name: switch for switch in switches}]

    for switch in switches:
        mocker.patch.object(switch, "start")

    await actor.start()

    assert len(actor.parser_args[0].keys()) == len(switches)

    await actor.stop()


async def test_actor_start_one_fails(switches, test_config: dict, mocker):

    actor = NPSActor.from_config(test_config)
    mocker.patch.object(AMQPActor, "start")

    actor.parser_args = [{switch.name: switch for switch in switches}]

    for ii, switch in enumerate(switches):
        mocker.patch.object(
            switch,
            "start",
            side_effect=None if ii != 1 else RuntimeError,
        )

    await actor.start()

    assert len(actor.parser_args[0].keys()) == len(switches) - 1

    await actor.stop()

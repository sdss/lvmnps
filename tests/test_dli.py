#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

from lvmnps.actor.actor import lvmnps as NpsActor


# TODO: this need to be rewritten.


async def test_status(dli_switches, actor: NpsActor):

    assert actor

    command = await actor.invoke_mock_command("status DLI-01")
    await command
    assert command.status.did_succeed
    assert command.replies[-2].message["status"] == {}

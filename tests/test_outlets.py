#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-05-22
# @Filename: test_outlets.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from lvmnps.actor import NPSActor


async def test_command_outlets(actor: NPSActor):
    cmd = await (await actor.invoke_mock_command("outlets"))
    assert cmd.status.did_succeed

    assert len(cmd.replies) == 2
    assert cmd.replies.get("outlets") == [
        "port1",
        "skye.what.ever",
        "skyw.what.ever",
        "skye.pwi",
        "skyw.pwi",
        "slow",
        "fast",
    ]


async def test_command_outlets_switchname(actor: NPSActor):
    cmd = await (await actor.invoke_mock_command("outlets nps_dummy_1"))
    assert cmd.status.did_succeed

    assert len(cmd.replies) == 2
    assert cmd.replies.get("outlets") == ["port1", "skye.what.ever", "skyw.what.ever"]


async def test_command_outlets_switchname_unknown(actor: NPSActor):
    cmd = await (await actor.invoke_mock_command("outlets blah"))
    assert cmd.status.did_fail

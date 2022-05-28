#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-05-22
# @Filename: test_switches.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from lvmnps.actor import NPSActor


async def test_command_switches(actor: NPSActor):

    cmd = await (await actor.invoke_mock_command("switches"))
    assert cmd.status.did_succeed

    assert len(cmd.replies) == 2
    assert cmd.replies.get("switches") == [
        "nps_dummy_1",
        "skye.nps",
        "nps_dummy_3",
        "slow",
        "fast",
    ]

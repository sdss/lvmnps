#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: test_actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pytest_mock import MockerFixture

from lvmnps.actor.actor import NPSActor
from lvmnps.nps.implementations.netio import NetIOClient


if TYPE_CHECKING:
    from sdsstools import Configuration


async def test_actor(nps_actor: NPSActor):
    assert isinstance(nps_actor, NPSActor)

    await nps_actor.stop()


@pytest.mark.parametrize("nps_type", [None, "bad_name"])
async def test_actor_invalid_type(nps_type: str | None, lvmnps_config: Configuration):
    lvmnps_config["nps"]["type"] = nps_type

    with pytest.raises(ValueError):
        NPSActor.from_config(lvmnps_config)


async def test_actor_config_missing(lvmnps_config: Configuration):
    del lvmnps_config["nps"]

    with pytest.raises(ValueError):
        NPSActor.from_config(lvmnps_config)


async def test_actor_netio_nps(lvmnps_config: Configuration):
    lvmnps_config["nps"]["type"] = "netio"

    actor = NPSActor.from_config(lvmnps_config)
    assert isinstance(actor.nps, NetIOClient)


async def test_command_status(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("status")
    await cmd

    assert cmd.status.did_succeed
    assert len(cmd.replies) == 5
    assert cmd.replies[-2].body == {
        "outlets": [
            {
                "critical": False,
                "cycle_delay": None,
                "id": 1,
                "index": 0,
                "locked": False,
                "name": "outlet_1",
                "normalised_name": "outlet_1",
                "physical_state": False,
                "state": False,
                "transient_state": False,
            }
        ]
    }


async def test_command_status_outlet(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("status outlet_1")
    await cmd

    assert cmd.status.did_succeed
    assert len(cmd.replies) == 2
    assert cmd.replies[-1].body == {
        "outlet_info": {
            "critical": False,
            "cycle_delay": None,
            "id": 1,
            "index": 0,
            "locked": False,
            "name": "outlet_1",
            "normalised_name": "outlet_1",
            "physical_state": False,
            "state": False,
            "transient_state": False,
        }
    }


async def test_command_status_invalid_outlet(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("status outlet_5")
    await cmd

    assert cmd.status.did_fail


async def test_command_refresh(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("refresh")
    await cmd

    assert cmd.status.did_succeed


@pytest.mark.parametrize("on", [True, False])
@pytest.mark.parametrize("outlet", [1, "outlet_1"])
async def test_command_onoff(nps_actor: NPSActor, outlet: str | int, on: bool):
    cmd = await nps_actor.invoke_mock_command(f"on {outlet}" if on else f"off {outlet}")
    await cmd

    assert cmd.status.did_succeed
    assert nps_actor.nps.outlets["outlet_1"].state is on


async def test_command_cycle(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("cycle 1")
    await cmd

    assert cmd.status.did_succeed


async def test_command_script_list(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("scripts list")
    await cmd

    assert cmd.status.did_succeed


async def test_command_script_list_invalid(nps_actor: NPSActor):
    nps_actor.nps.implementations = {"scripting": False}

    cmd = await nps_actor.invoke_mock_command("scripts list")
    await cmd

    assert cmd.status.did_fail


async def test_command_script_run(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("scripts run user_function1")
    await cmd

    assert cmd.status.did_succeed


async def test_command_script_run_not_enough_args(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("scripts run")
    await cmd

    assert cmd.status.did_fail


async def test_command_script_run_invalid(nps_actor: NPSActor):
    nps_actor.nps.implementations = {"scripting": False}

    cmd = await nps_actor.invoke_mock_command("scripts run user_function1")
    await cmd

    assert cmd.status.did_fail


async def test_command_script_run_fails(nps_actor: NPSActor, mocker: MockerFixture):
    nps_actor.nps.run_script = mocker.AsyncMock(side_effect=RuntimeError)

    cmd = await nps_actor.invoke_mock_command("scripts run user_function1")
    await cmd

    assert cmd.status.did_fail


async def test_command_script_stop(nps_actor: NPSActor):
    cmd = await nps_actor.invoke_mock_command("scripts stop")
    await cmd

    assert cmd.status.did_succeed


async def test_command_script_stop_invalid(nps_actor: NPSActor):
    nps_actor.nps.implementations = {"scripting": False}

    cmd = await nps_actor.invoke_mock_command("scripts stop")
    await cmd

    assert cmd.status.did_fail


async def test_command_script_stop_fails(nps_actor: NPSActor, mocker: MockerFixture):
    nps_actor.nps.stop_script = mocker.AsyncMock(side_effect=RuntimeError)

    cmd = await nps_actor.invoke_mock_command("scripts stop")
    await cmd

    assert cmd.status.did_fail

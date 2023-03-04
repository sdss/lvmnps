#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import os

import pytest

from sdsstools import read_yaml_file

from lvmnps.switch.dli.powerswitch import DLIPowerSwitch


@pytest.fixture
async def dli_switches(mocker):
    root = os.path.dirname(__file__)
    config = read_yaml_file(os.path.join(root, "test_dli_switch.yml"))

    switches = []
    for switch_name in config["switches"]:
        switch = DLIPowerSwitch(switch_name, config["switches"][switch_name])

        # Fake the client reply to a get(/relay/outlets)
        get_mock = mocker.MagicMock(status_code=200)

        # Build a fake reply with two outlets defined and six empty ones
        get_mock.json.return_value = [
            {"state": False, "name": "Outlet 1"},
            {"state": True, "name": "Outlet 2"},
        ]
        get_mock.json.return_value += 6 * [{"state": False, "name": ""}]

        # Patch the client to use the mocked get method.
        mocker.patch.object(
            switch.dli.client,
            "get",
            return_value=get_mock,
        )

        # Also mock PUT
        mocker.patch.object(
            switch.dli.client,
            "put",
            return_value=mocker.MagicMock(status_code=204),
        )

        await switch.start()

        switches.append(switch)

    yield switches

    for switch in switches:
        await switch.stop()


async def test_dli_power_switch(dli_switches: list[DLIPowerSwitch]):
    switch = dli_switches[0]

    assert switch.name == "DLI-01"
    assert len(switch.outlets) == 8
    assert switch.outlets[1].inuse is False


async def test_dli_power_switch_handle_undefined(dli_switches: list[DLIPowerSwitch]):
    switch = dli_switches[0]
    switch.onlyusedones = False

    await switch.start()

    assert switch.name == "DLI-01"
    assert len(switch.outlets) == 8

    assert switch.outlets[1].name == "Outlet 2"
    assert switch.outlets[1].inuse is True
    assert (await switch.isReachable()) is True


async def test_dli_on(dli_switches: list[DLIPowerSwitch]):
    switch = dli_switches[0]

    assert switch.outlets[0].state == 0

    await switch.switch(True, [switch.outlets[0]])


async def test_dli_off(dli_switches: list[DLIPowerSwitch]):
    switch = dli_switches[0]

    await switch.switch(False, [switch.outlets[0]])


async def test_dli_verify_fails(dli_switches: list[DLIPowerSwitch], mocker):
    switch = dli_switches[0]
    mocker.patch.object(switch.dli, "verify", side_effect=ValueError)

    with pytest.raises(RuntimeError):
        await switch.start()


def test_dli_missing_credentials():
    with pytest.raises(ValueError):
        DLIPowerSwitch("test", {})


async def test_dli_switch_fails(dli_switches: list[DLIPowerSwitch], mocker):
    switch = dli_switches[0]
    mocker.patch.object(switch.dli, "on", side_effect=ValueError)

    with pytest.raises(RuntimeError):
        await switch.switch(True, [switch.outlets[0]])


async def test_dli_update_fails(dli_switches: list[DLIPowerSwitch], mocker):
    switch = dli_switches[0]
    mocker.patch.object(switch.dli, "status", side_effect=ValueError)

    with pytest.raises(RuntimeError):
        await switch.update([switch.outlets[0]])

    assert switch.outlets[0].state == -1


async def test_dli_update_unreachable(dli_switches: list[DLIPowerSwitch], mocker):
    switch = dli_switches[0]
    switch.reachable = False

    await switch.update([switch.outlets[0]])

    assert switch.outlets[0].state == -1

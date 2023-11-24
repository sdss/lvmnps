#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: test_nps.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pytest
from pytest_mock import MockerFixture

from lvmnps.nps.core import NPSClient, OutletModel


async def test_npsclient(nps_test_client: NPSClient):
    await nps_test_client.stop()

    assert nps_test_client is not None
    assert len(nps_test_client.outlets) == 1


@pytest.mark.parametrize("outlets", [1, "test_1", "Test_1", [1], ["test_1"]])
async def test_set_state(nps_test_client: NPSClient, outlets):
    assert nps_test_client is not None

    await nps_test_client.set_state(outlets, on=True)

    outlet = nps_test_client.outlets["test_1"]
    assert outlet.state is True


async def test_set_state_outlet_model(nps_test_client: NPSClient):
    assert nps_test_client is not None

    outlet = nps_test_client.outlets["test_1"]
    await nps_test_client.set_state([outlet], on=True)

    assert outlet.state is True


@pytest.mark.parametrize("client", [True, False])
async def test_outlet_on_off(nps_test_client: NPSClient, client: bool):
    assert nps_test_client is not None

    outlet = nps_test_client.outlets["test_1"]

    if client:
        await outlet.on()
        assert outlet.state is True

        await outlet.off()
        assert outlet.state is False

    else:
        outlet._client = None

        with pytest.raises(RuntimeError):
            await outlet.off()

        with pytest.raises(RuntimeError):
            await outlet.on()


async def test_outlet_cycle(nps_test_client: NPSClient):
    assert nps_test_client is not None

    outlet = nps_test_client.outlets["test_1"]
    await nps_test_client.cycle(outlet, delay=0.1)

    assert outlet.state is True


@pytest.mark.parametrize("outlet", [1, "test_1"])
async def test_client_get(nps_test_client: NPSClient, outlet: str | int):
    assert isinstance(nps_test_client.get(outlet), OutletModel)


async def test_client_get_invalid_type(nps_test_client: NPSClient):
    with pytest.raises(TypeError):
        nps_test_client.get(None)  # type: ignore


async def test_all_off(nps_test_client: NPSClient, mocker: MockerFixture):
    assert nps_test_client is not None

    nps_test_client._set_state_internal = mocker.AsyncMock()

    await nps_test_client.all_off()

    outlets = list(nps_test_client.outlets.values())
    nps_test_client._set_state_internal.assert_called_once_with(outlets, on=False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: conftest.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pathlib

from typing import TYPE_CHECKING

import pytest
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from clu.testing import setup_test_actor
from sdsstools import read_yaml_file

from lvmnps.actor.actor import NPSActor
from lvmnps.nps import DLIClient
from lvmnps.nps.core import NPSClient, OutletModel
from lvmnps.nps.implementations.dli import DLIOutletModel
from lvmnps.nps.implementations.netio import NetIOClient


if TYPE_CHECKING:
    from sdsstools import Configuration


class NPSTestClient(NPSClient):
    """Test NPS client."""

    nps_type = "test"

    async def setup(self):
        await self.refresh()

    async def refresh(self):
        if "test_1" in self.outlets:
            return

        self.outlets = {"test_1": OutletModel(id=1, name="test_1", state=False)}
        self.outlets["test_1"].set_client(self)

    async def verify(self):
        pass

    async def _set_state_internal(self, outlets: list[OutletModel], on: bool = False):
        for outlet in outlets:
            outlet.state = on


@pytest.fixture
async def nps_test_client():
    _client = NPSTestClient()
    await _client.setup()

    yield _client


dli_default_outlets = [
    {
        "critical": False,
        "transient_state": False,
        "state": False,
        "physical_state": False,
        "name": "Argon",
        "locked": False,
        "cycle_delay": None,
    },
    {
        "critical": False,
        "transient_state": True,
        "state": True,
        "physical_state": True,
        "name": "Neon",
        "locked": False,
        "cycle_delay": None,
    },
]


@pytest.fixture
def lvmnps_config():
    yield read_yaml_file(pathlib.Path(__file__).parent / "./config.yaml")


@pytest.fixture
async def dli_client(httpx_mock: HTTPXMock, lvmnps_config: Configuration):
    init_parameters = lvmnps_config["nps.init_parameters"]

    client = DLIClient(**init_parameters)

    _base_url = f"http://{init_parameters['host']}:{init_parameters['port']}/restapi"

    httpx_mock.add_response(
        method="GET",
        url=f"{_base_url}/",
        status_code=206,
    )

    httpx_mock.add_response(
        method="PUT",
        url=f"{_base_url}/relay/sequence_delay/",
        status_code=204,
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{_base_url}/relay/outlets/",
        json=dli_default_outlets,
        status_code=200,
    )

    yield client


netio_default_outlets = {
    "Agent": {
        "Model": "4PS",
        "DeviceName": "PowerPDU SkyW",
        "MAC": "24:A4:2C:39:9D:27",
        "SerialNumber": "24A42C399D27",
        "JSONVer": "2.3",
        "Time": "1970-01-02T04:24:59+01:00",
        "Uptime": 55499,
        "Version": "3.0.1",
        "OemID": 100,
        "VendorID": 0,
        "NumOutputs": 4,
        "NumInputs": 0,
    },
    "Outputs": [
        {"ID": 1, "Name": "PW Mount", "State": 1, "Action": 6, "Delay": 5000},
        {"ID": 2, "Name": "PW MiniPC", "State": 1, "Action": 6, "Delay": 5000},
        {"ID": 3, "Name": "Power output 3", "State": 0, "Action": 6, "Delay": 5000},
        {"ID": 4, "Name": "Power output 4", "State": 0, "Action": 6, "Delay": 5000},
    ],
}


@pytest.fixture
async def netio_client(httpx_mock: HTTPXMock):
    client = NetIOClient(host="127.0.0.1")

    _base_url = "http://127.0.0.1:80"

    httpx_mock.add_response(
        method="GET",
        url=f"{_base_url}/netio.json",
        json=netio_default_outlets,
        status_code=200,
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{_base_url}/netio.json",
        json=netio_default_outlets,
        status_code=200,
    )

    yield client


@pytest.fixture
async def nps_actor(mocker: MockerFixture, lvmnps_config: Configuration):
    actor = NPSActor.from_config(lvmnps_config)

    actor.nps = mocker.MagicMock(spec=DLIClient)
    actor.nps.nps_type = "dli"
    actor.nps.outlets = {"outlet_1": DLIOutletModel(id=1, name="outlet_1")}

    async def _set_state_mock(outlets: list[int | str], on: bool = False):
        for outlet in actor.nps.outlets.values():
            outlet.state = on

        return list(actor.nps.outlets.values())

    actor.nps.set_state = mocker.MagicMock(side_effect=_set_state_mock)

    await setup_test_actor(actor)  # type: ignore

    yield actor

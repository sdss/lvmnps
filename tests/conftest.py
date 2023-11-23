#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: conftest.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pathlib

import pytest
from pytest_httpx import HTTPXMock

from sdsstools import read_yaml_file

from lvmnps.nps import DLIClient
from lvmnps.nps.core import NPSClient, OutletModel


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
async def dli_client(httpx_mock: HTTPXMock):
    config = read_yaml_file(pathlib.Path(__file__).parent / "./config.yaml")
    init_parameters = config["nps.init_parameters"]

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

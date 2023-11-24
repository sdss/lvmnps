#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: test_nps.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import re

from typing import TYPE_CHECKING

import httpx
import pytest
from pytest_httpx import HTTPXMock

from lvmnps.exceptions import NPSWarning, VerificationError

from .conftest import netio_default_outlets


if TYPE_CHECKING:
    from lvmnps.nps import NetIOClient


async def test_netio(netio_client: NetIOClient):
    await netio_client.setup()

    assert len(netio_client.outlets) == 4


async def test_netio_verification_fails(
    netio_client: NetIOClient,
    httpx_mock: HTTPXMock,
):
    httpx_mock.reset(False)
    httpx_mock.add_response(url=re.compile(r"http://.+?/netio.json"), status_code=500)

    with pytest.warns(NPSWarning):
        await netio_client.setup()

    assert len(netio_client.outlets) == 0


async def test_netio_verification_connection_error(
    netio_client: NetIOClient,
    httpx_mock: HTTPXMock,
):
    httpx_mock.reset(False)
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    with pytest.raises(VerificationError):
        await netio_client.verify()


async def test_netio_set_state(netio_client: NetIOClient, httpx_mock: HTTPXMock):
    await netio_client.setup()

    httpx_mock.add_response(
        method="POST",
        url=re.compile(r"http://.+?/netio.json"),
        status_code=200,
    )

    response_json = netio_default_outlets.copy()
    response_json["Outputs"][2]["State"] = True

    httpx_mock.add_response(
        method="GET",
        url=re.compile(r"http://.+?/netio.json"),
        status_code=200,
        json=response_json,
    )

    await netio_client.set_state(3, on=True)

    assert netio_client.get(3).state is True

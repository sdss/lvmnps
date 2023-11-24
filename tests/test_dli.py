#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: test_dli.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import re

from typing import TYPE_CHECKING

import httpx
import pytest
from pytest_httpx import HTTPXMock

from lvmnps.exceptions import NPSWarning, ResponseError, VerificationError

from .conftest import dli_default_outlets


if TYPE_CHECKING:
    from lvmnps.nps import DLIClient


async def test_dli(dli_client: DLIClient):
    await dli_client.setup()

    assert len(dli_client.outlets) == 2


async def test_dli_verification_fails(dli_client: DLIClient, httpx_mock: HTTPXMock):
    httpx_mock.reset(False)
    httpx_mock.add_response(url=re.compile(r"http://.+?/restapi/"), status_code=500)

    with pytest.warns(NPSWarning):
        await dli_client.setup()

    assert len(dli_client.outlets) == 0


async def test_dli_verification_connection_error(
    dli_client: DLIClient,
    httpx_mock: HTTPXMock,
):
    httpx_mock.reset(False)
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    with pytest.raises(VerificationError):
        await dli_client.verify()


async def test_dli_set_state(dli_client: DLIClient, httpx_mock: HTTPXMock):
    await dli_client.setup()

    httpx_mock.add_response(
        method="PUT",
        url=re.compile(r"http://.+?/restapi/relay/outlets/=0/state/"),
        status_code=207,
    )

    response_json = dli_default_outlets.copy()
    response_json[0]["state"] = True

    httpx_mock.add_response(
        method="GET",
        url=re.compile(r"http://.+?/restapi/relay/outlets/"),
        status_code=200,
        json=response_json,
    )

    await dli_client.set_state("argon", on=True)

    assert dli_client.outlets["argon"].state is True


async def test_dli_list_scripts(dli_client: DLIClient, httpx_mock: HTTPXMock):
    await dli_client.setup()

    httpx_mock.add_response(
        method="GET",
        url=re.compile(r"http://.+?/restapi/script/user_functions/"),
        status_code=200,
        json={"user_function1": {}, "user_function2": {}},
    )

    user_functions = await dli_client.list_scripts()
    assert len(user_functions) == 2


async def test_dli_list_running_scripts(dli_client: DLIClient, httpx_mock: HTTPXMock):
    await dli_client.setup()

    httpx_mock.add_response(
        method="GET",
        url=re.compile(r"http://.+?/restapi/script/threads/"),
        status_code=200,
        json={"1": {"label": "user_function1 (blah)"}},
    )

    running_threads = await dli_client.list_running_scripts()
    assert running_threads == {1: "user_function1"}


@pytest.mark.parametrize("check_exists", [True, False])
@pytest.mark.parametrize("function_args", [[1, 2], []])
async def test_dli_run_script(
    dli_client: DLIClient,
    httpx_mock: HTTPXMock,
    check_exists: bool,
    function_args: list,
):
    await dli_client.setup()

    if check_exists:
        httpx_mock.add_response(
            method="GET",
            url=re.compile(r"http://.+?/restapi/script/user_functions/"),
            status_code=200,
            json={"user_function1": {}, "user_function2": {}},
        )

    httpx_mock.add_response(
        method="POST",
        url=re.compile(r"http://.+?/restapi/script/start/"),
        status_code=200,
        json="1",
    )

    await dli_client.run_script(
        "user_function1",
        *function_args,
        check_exists=check_exists,
    )


async def test_dli_run_script_does_not_exist(
    dli_client: DLIClient,
    httpx_mock: HTTPXMock,
):
    await dli_client.setup()

    httpx_mock.add_response(
        method="GET",
        url=re.compile(r"http://.+?/restapi/script/user_functions/"),
        status_code=200,
        json={"user_function3": {}},
    )

    with pytest.raises(ValueError):
        await dli_client.run_script("user_function1")


async def test_dli_run_script_invalid(dli_client: DLIClient, httpx_mock: HTTPXMock):
    await dli_client.setup()

    httpx_mock.add_response(
        method="POST",
        url=re.compile(r"http://.+?/restapi/script/start/"),
        status_code=409,
        json="1",
    )

    with pytest.raises(ResponseError):
        await dli_client.run_script("user_function1", check_exists=False)


@pytest.mark.parametrize("thread_num", [None, 1])
async def test_dli_stop_script(
    dli_client: DLIClient,
    httpx_mock: HTTPXMock,
    thread_num: int | None,
):
    await dli_client.setup()

    httpx_mock.add_response(
        method="POST",
        url=re.compile(r"http://.+?/restapi/script/stop/"),
        status_code=200,
    )

    await dli_client.stop_script(thread_num)

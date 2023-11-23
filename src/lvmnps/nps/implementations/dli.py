#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: dli.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import warnings

import httpx
from pydantic import ConfigDict, SecretStr
from pydantic.dataclasses import dataclass

from lvmnps import log
from lvmnps.exceptions import ResponseError, VerificationError
from lvmnps.nps.core import NPSClient, OutletModel


__all__ = ["DLIClient", "DLIOutletModel"]


class DLIOutletModel(OutletModel):
    """A model for a DLI outlet status."""

    index: int = 0
    physical_state: bool = False
    transient_state: bool = False
    critical: bool = False
    locked: bool = False
    cycle_delay: float | None = None


@dataclass
class APIClient:
    """A wrapper around ``httpx.AsyncClient`` to yield a new client."""

    base_url: str
    user: str
    password: SecretStr

    def __post_init__(self):
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Yields a new client."""

        log.debug(f"Creating async client to {self.base_url!r} with digest.")

        auth = httpx.DigestAuth(self.user, self.password.get_secret_value())
        self.client = httpx.AsyncClient(
            auth=auth,
            base_url=self.base_url,
            headers={},
        )

        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        """Closes the client."""

        if self.client and not self.client.is_closed:
            log.debug("Closing async client.")
            await self.client.aclose()


@dataclass(config=ConfigDict(extra="forbid"))
class DLIClient(NPSClient):
    """An NPS client for a Digital Loggers switch."""

    host: str
    port: int = 80
    user: str = "admin"
    password: SecretStr = SecretStr("admin")
    api_route: str = "restapi/"

    def __post_init__(self):
        super().__init__()

        self.base_url = f"http://{self.host}:{self.port}/{self.api_route}"
        self.api_client = APIClient(self.base_url, self.user, self.password)

        self.outlet: dict[str, DLIOutletModel] = {}

        self.nps_type = "dli"

    async def setup(self):
        """Sets up the power supply, setting any required configuration options."""

        try:
            await self.verify()
        except VerificationError as err:
            warnings.warn(
                "Cannot setup DLI. Power switch "
                f"verification failed with error: {err}"
            )
            return

        async with self.api_client as client:
            # Change in-rush delay to 1 second.
            log.debug("Setting sequence delay to 1 second.")
            response = await client.put(
                url="/relay/sequence_delay/",
                data={"value": 1},
                headers={"X-CSRF": "x"},
            )
            self._validate_response(response, 204)

        await self.refresh()

    def _validate_response(self, response: httpx.Response, expected_code: int = 200):
        """Validates an HTTP response."""

        if response.status_code != expected_code:
            raise VerificationError(
                f"Request returned response with status code {response.status_code}."
            )

    async def verify(self):
        """Checks that the NPS is connected and responding."""

        async with self.api_client as client:
            try:
                response = await client.get(url="/", headers={"Range": "dli-depth=1"})
            except httpx.ConnectError as err:
                raise VerificationError(f"Failed to connect to DLI: {err}")

        # 206 because we have asked for the API to only do depth=1
        self._validate_response(response, 206)

    async def refresh(self):
        """Refreshes the list of outlets."""

        log.debug("Refreshing list of outlets.")

        url = "/relay/outlets/"
        async with self.api_client as client:
            response = await client.get(url=url)

        self._validate_response(response)

        data = response.json()
        log.debug(f"Found {len(data)} outlets.")

        self.outlets = {}

        for outlet_id in range(1, len(data) + 1):
            outlet_data = data[outlet_id - 1]
            outlet_data["id"] = outlet_id
            outlet_data["index"] = outlet_id - 1

            outlet = DLIOutletModel(**outlet_data)
            outlet.client = self
            self.outlets[outlet.normalised_name] = outlet

    async def _set_state_internal(
        self,
        outlets: list[DLIOutletModel],
        on: bool = False,
    ):
        """Sets the state of a list of outlets."""

        outlet_indices = [outlet.index for outlet in outlets]

        # Use a matrix URI to set all the states at once.
        outlet_path = "=" + ",".join(map(str, outlet_indices))

        async with self.api_client as client:
            response = await client.put(
                url=f"/relay/outlets/{outlet_path}/state/",
                data={"value": on},
                headers={"X-CSRF": "x"},
            )
            self._validate_response(response, 207)

        return

    async def list_scripts(self):
        "Retrieves the list of user scripts." ""

        async with self.api_client as client:
            response = await client.get(url="/script/user_functions/")
            self._validate_response(response, 200)

        return list(response.json())

    async def run_script(self, name: str, *args, check_exists: bool = True) -> int:
        """Runs a user script.

        Parameters
        ----------
        name
            The script name.
        args
            Arguments with which to call the script function.
        check_exists
            If ``True``, checks that the script exists in the DLI before
            executing it.

        Returns
        -------
        thread_num
            The thread identifier for the running script.

        """

        if check_exists:
            scripts = await self.list_scripts()
            if name not in scripts:
                raise ValueError(f"Unknown user function {name!r}.")

        data = {"user_function": name}
        if len(args) > 0:
            args_comma = ", ".join(map(str, args))
            data["source"] = f"{name}({args_comma})"

        async with self.api_client as client:
            response = await client.post(
                url="/script/start/",
                json=[data],
                headers={"X-CSRF": "x"},
            )

            if response.status_code == 409:
                raise ResponseError("Invalid function name or argument")

            self._validate_response(response, 200)

        thread_num = int(response.json())

        log.info(f"Script {name!r} is running as thread {thread_num}")

        return thread_num

    async def stop_script(self, thread_num: int | None = None):
        """Stops a running script.

        Parameters
        ----------
        thread_num
            The thread to stop. If not specified, stops all threads.

        """

        if thread_num is None:
            log.info("Stopping all script threads.")
        else:
            log.info(f"Stopping script thread {thread_num}.")

        async with self.api_client as client:
            response = await client.post(
                url="/script/stop/",
                json=["all" if thread_num is None else str(thread_num)],
                headers={"X-CSRF": "x"},
            )

            self._validate_response(response, 200)
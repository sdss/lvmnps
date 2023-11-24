#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: netio.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import warnings

from typing import Any

import httpx
from pydantic import ConfigDict, SecretStr
from pydantic.dataclasses import dataclass

from lvmnps import log
from lvmnps.exceptions import NPSWarning, VerificationError
from lvmnps.nps.core import NPSClient, OutletModel
from lvmnps.tools import APIClient


class NetIOOutLetModel(OutletModel):
    """Outlet model for NetIO switches."""

    pass


@dataclass(config=ConfigDict(extra="forbid"))
class NetIOClient(NPSClient):
    """An NPS client for a NetIO switch.

    This implementation uses the JSON API, see
    https://www.netio-products.com/files/NETIO-M2M-API-Protocol-JSON.pdf

    """

    host: str
    port: int = 80
    user: str = "admin"
    password: SecretStr = SecretStr("admin")

    def __post_init__(self):
        super().__init__()

        self.base_url = f"http://{self.host}:{self.port}"
        self.api_client = APIClient(
            self.base_url,
            self.user,
            self.password,
            auth_method="basic",
        )

        self.outlets: dict[str, NetIOOutLetModel] = {}

        self.nps_type = "netio"
        self.implementations = {"scripting": False}

    async def setup(self):
        """Sets up the power supply, setting any required configuration options."""

        log.info("Setting up NetIO switch.")

        try:
            await self.verify()
        except VerificationError as err:
            warnings.warn(
                "Cannot setup NetIO. Power switch "
                f"verification failed with error: {err}",
                NPSWarning,
            )
            return

        await self.refresh()

        log.info("Set up complete.")

    async def verify(self):
        """Checks that the NPS is connected and responding."""

        async with self.api_client as client:
            try:
                response = await client.get(url="/netio.json")
            except httpx.ConnectError as err:
                raise VerificationError(f"Failed to connect to NetIO: {err}")

        self._validate_response(response, 200)

    async def refresh(self):
        """Refreshes the list of outlets."""

        log.debug("Refreshing list of outlets.")

        async with self.api_client as client:
            response = await client.get(url="/netio.json")

        self._validate_response(response)

        data = response.json()
        outlet_json = data["Outputs"]

        log.debug(f"Found {len(outlet_json)} outlets.")

        self.outlets = {}

        for data in outlet_json:
            outlet = NetIOOutLetModel(
                id=data["ID"],
                name=data["Name"],
                state=data["State"],
            )
            outlet.set_client(self)
            self.outlets[outlet.normalised_name] = outlet

    async def _set_state_internal(
        self,
        outlets: list[NetIOOutLetModel],
        on: bool = False,
        off_after: float | None = None,
    ):
        """Sets the state of a list of outlets."""

        outputs: list[dict[str, Any]] = []

        for outlet in outlets:
            outlet_action: dict[str, Any] = {"ID": outlet.id, "Action": int(on)}
            if on is True and off_after is not None:
                outlet_action["Action"] = 3
                outlet_action["Delay"] = off_after * 1000
            outputs.append(outlet_action)

        async with self.api_client as client:
            response = await client.post(
                url="/netio.json",
                json={"Outputs": outputs},
            )

        self._validate_response(response)

        return

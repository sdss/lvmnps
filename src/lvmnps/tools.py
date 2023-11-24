#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: tools.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING

import httpx
from pydantic import SecretStr
from pydantic.dataclasses import dataclass
from typing_extensions import Literal

from lvmnps import log


if TYPE_CHECKING:
    from lvmnps.nps.core import OutletModel


__all__ = [
    "APIClient",
    "normalise_outlet_name",
    "get_outlet_by_name",
    "get_outlet_by_id",
]


@dataclass
class APIClient:
    """A wrapper around ``httpx.AsyncClient`` to yield a new client."""

    base_url: str
    user: str
    password: SecretStr

    auth_method: Literal["digest", "basic"] = "digest"

    def __post_init__(self):
        self.client: httpx.AsyncClient | None = None
        self.lock = asyncio.Lock()

    async def __aenter__(self):
        """Yields a new client."""

        await self.lock.acquire()

        log.debug(f"Creating async client to {self.base_url!r} with digest.")

        if self.auth_method == "digest":
            auth = httpx.DigestAuth(self.user, self.password.get_secret_value())
        elif self.auth_method == "basic":
            auth = (self.user, self.password.get_secret_value())
        else:
            raise ValueError(f"Invalud authentication method {self.auth_method!r}.")

        self.client = httpx.AsyncClient(
            auth=auth,
            base_url=self.base_url,
            headers={},
        )

        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        """Closes the client."""

        self.lock.release()

        if self.client and not self.client.is_closed:
            log.debug("Closing async client.")
            await self.client.aclose()


def normalise_outlet_name(name: str):
    """Returns a normalised name for an outlet."""

    return name.lower().replace(" ", "_")


def get_outlet_by_name(outlet_data: dict[str, OutletModel], name: str):
    """Gets an outlet from a list of outlets.

    Parameters
    ----------
    outlet_data
        The mapping of outlet name to outlet model data.
    name
        The name of the outlet to retrieve.

    Returns
    -------
    outlet
        The outlet matching the input name.

    Raises
    ------
    ValueError
        If the outlet cannot be found.

    """

    normalised_name = normalise_outlet_name(name)

    if normalised_name in outlet_data:
        return outlet_data[normalised_name]

    raise ValueError(f"Cannot find outlet with name {name!r}.")


def get_outlet_by_id(outlet_data: dict[str, OutletModel], id: int):
    """Gets an outlet by id.

    Parameters
    ----------
    outlet_data
        The mapping of outlet name to outlet model data.
    id
        The id of the outlet to retrieve.

    Returns
    -------
    outlet
        The outlet matching the id.

    Raises
    ------
    ValueError
        If the outlet cannot be found.

    """

    for outlet in outlet_data.values():
        if outlet.id == id:
            return outlet

    raise ValueError(f"Cannot find outlet with id {id!r}.")

# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr), Changgon Kim (changgonkim@khu.ac.kr)
# @Date: 2021-08-24
# @Update: 2021-10-09
# @Filename: lvmnps/switch/dli/dli.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

import httpx


if TYPE_CHECKING:
    from sdsstools.logger import SDSSLogger

    from ..outlet import Outlet


class DLI(object):
    """Powerswitch class to manage the DLI power switch.

    Parameters
    ----------
    hostname
        The hostname from the configuration (the IP address for connection).
    user
        The username from the configuration (the id for login).
    password
        The password from the configuration (the password for login).
    name
        The name of the DLI Controller.
    log
        The logger for logging.
    onoff_timeout
        The timeout, in seconds, before failing an on/off command.

    """

    def __init__(
        self,
        hostname: str,
        user: str,
        password: str,
        name: str | None = None,
        log: SDSSLogger | None = None,
        onoff_timeout=3,
    ):

        self.user = user
        self.hostname = hostname
        self.name = name or hostname

        self.log = log or logging.getLogger(f"{self.__class__.__name__}_{self.name}")

        self.onoff_timeout = onoff_timeout

        self.client: httpx.AsyncClient
        self.add_client(password)

    def add_client(self, password: str):
        """Add the `httpx.AsyncClient` to the DLI object."""

        try:
            auth = httpx.DigestAuth(self.user, password)
            self.client = httpx.AsyncClient(
                auth=auth,
                base_url=f"http://{self.hostname}/restapi",
                headers={},
            )
        except Exception as ex:
            self.log.error(f"{type(ex)}: couldn't access client {self.hostname}: {ex}")

    async def verify(self, outlets: list[Outlet]):
        """Verifies if we can reach the switch by the "get" method.

        Also compares the outlet lists with the configuration, and returns true
        if it's identical.

        Parameters
        ----------
        outlets
            The list of `.Outlet` instance to check.

        """

        result = False

        async with self.client as client:
            r = await client.get("relay/outlets/")
            if r.status_code != 200:
                raise RuntimeError(f"GET returned code {r.status_code}.")
            else:
                result = self.compare(r.json(), outlets)

        return result

    def compare(self, json: dict, outlets: list[Outlet]):
        """Compares the names of the outlets with the response JSON object.

        Parameters
        ----------
        json
            The json list from the restful API. The current status of the power
            switch is contained here.
        outlets
            List of `.Outlet` objects to compare.

        """

        same = True

        for outlet in outlets:
            portnum = outlet.portnum
            if json[portnum - 1]["name"] != outlet.name:
                same = False
                break

        return same

    async def on(self, outlet: int = 0):
        """Turn on the power to the outlet.

        Set the value of the outlet state by using a PUT request. Note that the
        outlets in the RESTful API are zero-indexed.

        Parameters
        ----------
        outlet
            The number indicating the outlet (1-indexed).

        """

        outlet = outlet - 1

        async with self.client as client:
            r = await asyncio.wait_for(
                client.put(
                    f"relay/outlets/{outlet}/state/",
                    data={"value": True},
                    headers={"X-CSRF": "x"},
                ),
                self.onoff_timeout,
            )
            if r.status_code != 204:
                raise RuntimeError(f"PUT returned code {r.status_code}.")

    async def off(self, outlet=0):
        """Turn off the power to the outlet.

        Set the value of the outlet state by using a PUT request. Note that the
        outlets in the RESTful API are zero-indexed.

        Parameters
        ----------
        outlet
            The number indicating the outlet (1-indexed).

        """

        outlet = outlet - 1

        async with self.client as client:
            r = await asyncio.wait_for(
                client.put(
                    f"relay/outlets/{outlet}/state/",
                    data={"value": False},
                    headers={"X-CSRF": "x"},
                ),
                self.onoff_timeout,
            )
            if r.status_code != 204:
                raise RuntimeError(f"PUT returned code {r.status_code}.")

    async def get_outlets_response(self):
        """Returns the raw response to a ``relay/outlets`` GET request.."""

        async with self.client as client:
            r = await client.get("relay/outlets/")
            if r.status_code != 200:
                raise RuntimeError(f"GET returned code {r.status_code}.")

        return r.json()

    async def status(self):
        """Returns the status as a dictionary.

        Receives the data from the switch by the GET method as a JSON. Note that
        this method returns the status of all the outlets (ports 1-8).

        """

        async with self.client as client:
            r = await client.get("relay/outlets/")
            if r.status_code != 200:
                raise RuntimeError(f"GET returned code {r.status_code}.")

        outlets_dict = {}

        data = r.json()
        for n in range(0, 8):
            outlets_dict[n + 1] = data[n]["state"]

        return outlets_dict

# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de),
# Mingyeong Yang (mingyeong@khu.ac.kr),
# Changgon Kim (changgonkim@khu.ac.kr)
# @Date: 2021-06-24
# @Update: 2021-10-09
# @Filename: lvmnps/switch/dli/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

from lvmnps.switch.dli.dli import DLI
from lvmnps.switch.powerswitchbase import PowerSwitchBase


if TYPE_CHECKING:
    from sdsstools.logger import SDSSLogger

    from ..outlet import Outlet


__all__ = ["DLIPowerSwitch"]


class DLIPowerSwitch(PowerSwitchBase):
    """A DLI power switch.

    Parameters
    ----------
    name
        A name identifying the power switch.
    config
        The configuration defined on the .yaml file under ``/etc/lvmnps_dli.yml``.
    log
        The logger for logging.

    """

    def __init__(self, name: str, config: dict, log: SDSSLogger | None = None):

        super().__init__(name, config, log)

        hostname = self.config_get("hostname")
        user = self.config_get("user")
        password = self.config_get("password")

        onoff_timeout = self.config_get("onoff_timeout", 3)

        if hostname is None or user is None or password is None:
            raise ValueError(
                "Hostname or credentials are missing. "
                "Cannot create new DLI instance."
            )

        self.name = name

        self.dli = DLI(
            hostname,
            user,
            password,
            log=self.log,
            name=self.name,
            onoff_timeout=onoff_timeout,
        )

        self.reachable = False

    async def start(self):
        """Adds the client controlling the DLI Power Switch.

        Checks if the Power switch is reachable.
        If the Power switch is reachable, updates the data of Outlet objects.

        """

        # Instead of sending several requests, which makes it a bit slower,
        # get all the information form the outlets and manually update states.

        outlet_data = await self.dli.get_outlets_response()

        for i in range(len(outlet_data)):
            outlet = self.collectOutletsByNameAndPort(portnum=i + 1)
            if len(outlet) == 0 or len(outlet) > 1:
                continue

            outlet[0].setState(outlet_data[i]["state"])

            if self.onlyusedones is False:
                if outlet[0].inuse:
                    continue

                if outlet_data[i]["name"] == "":
                    continue

                outlet[0].name = outlet_data[i]["name"]
                outlet[0].description = outlet_data[i]["name"]
                outlet[0].inuse = True

        try:
            inuse = [outlet for outlet in self.outlets if outlet.inuse]
            self.reachable = await self.dli.verify(inuse)
        except Exception as ex:
            raise RuntimeError(f"Unexpected exception is {type(ex)}: {ex}")

    async def stop(self):
        """Closes the connection to the client."""

        pass

    async def isReachable(self):
        """Check if the power switch is reachable."""

        return self.reachable

    async def update(self, outlets: list[Outlet] | None = None):
        """Updates the data based on the received status dictionary from the DLI class.

        Parameters
        ----------
        outlets
            List of `.Outlet` objects. If `None`, updates the status of all outlets.

        """

        outlets = outlets or self.outlets

        try:
            if self.reachable:
                # set the status to the real state
                status = await self.dli.status()
                for o in outlets:
                    o.setState(status[o.portnum])
            else:
                for o in outlets:
                    o.setState(-1)
        except Exception as ex:
            for o in outlets:
                o.setState(-1)
            raise RuntimeError(f"Unexpected exception for {type(ex)}: {ex}")

    async def switch(self, state: bool, outlets: list[Outlet]):
        """Controls the switch (turning on or off).

        Parameters
        ----------
        state
            The state to which to switch the outlet(s).
        outlets
            List of outlets to command.

        """

        state = bool(state)

        try:
            if self.reachable:
                for o in outlets:
                    await (self.dli.on(o.portnum) if state else self.dli.off(o.portnum))
            await self.update(outlets)
        except Exception as ex:
            raise RuntimeError(f"Unexpected exception to {type(ex)}: {ex}")

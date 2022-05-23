# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/powerswitchbase.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from abc import abstractmethod

from sdsstools.logger import SDSSLogger

from lvmnps.switch.outlet import Outlet


__all__ = ["PowerSwitchBase"]


class PowerSwitchBase(object):
    """PowerSwitchBase class for multiple power switches from different manufacturers.

    The Powerswitch classes will inherit from the `.PowerSwitchBase` class.

    Parameters
    ----------
    name
        A name identifying the power switch.
    config
        The configuration defined on the .yaml file under ``/etc/lvmnps.yml``.
    log
        The logger for logging.

    """

    def __init__(self, name: str, config: dict, log: SDSSLogger | None = None):

        self.name = name
        self.log = log or SDSSLogger(f"powerswitchbase.{name}")
        self.config = config

        numports = self.config_get("ports.number_of_ports", 8)
        if numports is None:
            raise ValueError(f"{name}: unknown number of ports.")
        self.numports: int = numports

        self.outlets = [
            Outlet(
                self,
                self.config_get(f"ports.{portnum}.name"),
                portnum,
                self.config_get(f"ports.{portnum}.desc"),
                -1,
            )
            for portnum in range(1, self.numports + 1)
        ]

        self.onlyusedones = self.config_get("ouo", True)
        self.log.debug(f"Only used ones: {self.onlyusedones}")

    def config_get(self, key, default=None):
        """Read the configuration and extract the data as a structure that we want.

        Notice: DOESN'T work for keys with dots !!!

        Parameters
        ----------
        key
            The tree structure as a string to extract the data.
            For example, if the configuration structure is ::

                ports:
                  1:
                      desc: "Hg-Ar spectral callibration lamp"

            You can input the key as
            ``ports.1.desc`` to take the information "Hg-Ar spectral callibration lamp".

        """

        def g(config, key, d=None):
            """Internal function for parsing the key from the configuration.

            Parameters
            ----------
            config
                config from the class member, which is saved from the class instance
            key
                The tree structure as a string to extract the data.
                For example, if the configuration structure is ::

                ports:
                  num:1
                    1:
                      desc: "Hg-Ar spectral callibration lamp"

                You can input the key as "ports.1.desc" to take the information
                "Hg-Ar spectral callibration lamp"

            """

            k = key.split(".", maxsplit=1)
            c = config.get(
                k[0] if not k[0].isnumeric() else int(k[0])
            )  # keys can be numeric

            return (
                d
                if c is None
                else c
                if len(k) < 2
                else g(c, k[1], d)
                if type(c) is dict
                else d
            )

        return g(self.config, key, default)

    def findOutletByName(self, name: str):
        """Find the outlet by the name, comparing with the name from the Outlet object.

        Parameters
        ----------
        name
            The string to compare with the name in Outlet instance.
        """
        for o in self.outlets:
            if o.name.lower() == name.lower():
                return o

    def collectOutletsByNameAndPort(
        self,
        name: str | None = None,
        portnum: int | None = None,
    ):
        """Collects the outlet by the name and ports,
        comparing with the name and ports from the Outlet object.

        Parameters
        ----------
        name
            The string to compare with the name in Outlet instance.
        portnum
            The integer for indicating each Outlet instances. If zero or `None`,
            identifies the outlet only by name.

        Returns
        -------
        outlets
            A list of `.Outlet` that match the name and port number. If ``name=None``,
            the outlet matching the port number is returned. If both ``name`` and
            ``portnum`` are `None`, a list with all the outlets connected to this
            switch is returned.

        """

        if not name or name == self.name:
            if portnum:
                if portnum > self.numports:
                    return []
                return [self.outlets[portnum - 1]]
            else:
                outlets = []

                for o in self.outlets:
                    if o.inuse or not self.onlyusedones:
                        outlets.append(o)

                return outlets
        else:
            o = self.findOutletByName(name)
            if o:
                return [o]

        return []

    async def setState(
        self,
        state: bool | int,
        name: str | None = None,
        portnum: int | None = None,
    ):
        """Set the state of the Outlet instance to On/Off. (On = 1, Off = 0).

        Note that dependending on the values passed to ``name`` and ``portnum``,
        multiple outlets may be commanded.

        Parameters
        ----------
        state
            The boolean value (True, False) to set the state inside the Outlet object.
        name
            The string to compare with the name in Outlet instance.
        portnum
            The integer for indicating each Outlet instances.

        """

        state_int = Outlet.parse(state)
        if state_int == -1:
            raise ValueError(f"{self.name}: cannot parse state {state!r}.")

        return await self.switch(
            state_int,
            self.collectOutletsByNameAndPort(name, portnum),
        )

    async def statusAsDict(self, name: str | None = None, portnum: int | None = None):
        """Get the status of the `.Outlets` as a dictionary.

        Parameters
        ----------
        name
            The string to compare with the name in Outlet instance.
            ``name`` can be a switch or an outlet name.
        portnum
            The integer for indicating each Outlet instances.

        """

        outlets = self.collectOutletsByNameAndPort(name, portnum)

        await self.update(outlets)

        status = {}
        for o in outlets:
            status[f"{o.name}"] = o.toDict()

        return status

    @abstractmethod
    async def start(self):
        """Starts the switch instance, potentially connecting to the device server."""
        pass

    @abstractmethod
    async def stop(self):
        """Stops the connection to the switch server."""
        pass

    @abstractmethod
    async def isReachable(self):
        """Verify we can reach the switch. Returns `True` if ok."""
        pass

    @abstractmethod
    async def update(self, outlets: list[Outlet] | None):
        """Retrieves the status of a list of outlets and updates the internal mapping.

        Parameters
        ----------
        outlets
            A list of `.Outlets` to update. If `None`, all outlets are updated.

        """
        pass

    @abstractmethod
    async def switch(self, state: int, outlets: list[Outlet]):
        """Changes the state of an outlet.

        Parameters
        ----------
        state
            The final state for the outlets. 0: off, 1: on.
        outlets
            A list of `.Outlets` which status will be updated.

        """
        pass

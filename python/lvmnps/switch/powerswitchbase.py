# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/powerswitchbase.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from abc import abstractmethod

from sdsstools.logger import SDSSLogger

from lvmnps.switch.outlet import Outlet


__all__ = ["PowerSwitchBase"]


class PowerSwitchBase(object):
    """PowerswitchBase class for multiple power switches from different manufacturers
    The Powerswitch classes will inherit the PowerSwitchBase class.

    Parameters
    ----------
    name
        A name identifying the power switch.
        'DLI Controller' for Dli switch
    config
        The configuration defined on the .yaml file under /etc/lvmnps.yml
    log
        The logger for logging
    """

    def __init__(self, name: str, config: [], log: SDSSLogger):
        self.name = name
        self.log = log
        self.config = config

        self.numports = self.config_get("ports.num", 8)
        self.outlets = [
            Outlet(
                name,
                self.config_get(f"ports.{portnum}.name"),
                portnum,
                self.config_get(f"ports.{portnum}.desc"),
                -1,
            )
            for portnum in range(1, self.numports + 1)
        ]
        self.log.debug(f"{self.outlets}")
        self.onlyusedones = self.config_get("ouo", True)
        self.log.debug(f"Only used ones: {self.onlyusedones}")

    def config_get(self, key, default=None):
        """Read the configuration and extract the data as a structure that we want.
        Notice: DOESNT work for keys with dots !!!

        Parameters
        ----------
        key
            The tree structure as a string to extract the data.
            For example, if the configuration structure is

            ports:
                num:1
                1:
                    desc: "Hg-Ar spectral callibration lamp"

            You can input the key as
            "ports.1.desc" to take the information "Hg-Ar spectral callibration lamp"
        """

        def g(config, key, d=None):
            """Internal function for parsing the key from the configuration.

            Parameters
            ----------
            config
                config from the class member, which is saved from the class instance
            key
                The tree structure as a string to extract the data.
                For example, if the configuration structure is

                ports:
                    num:1
                    1:
                        desc: "Hg-Ar spectral callibration lamp"

                You can input the key as
                "ports.1.desc" to take the information "Hg-Ar spectral callibration lamp"
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
            if o.name == name:
                return o

    def collectOutletsByNameAndPort(self, name: str, portnum: int = 0):
        """Collects the outlet by the name and ports,
        comparing with the name and ports from the Outlet object.

        Parameters
        ----------
        name
            The string to compare with the name in Outlet instance.
        portnum
            The integer for indicating each Outlet instances
        """
        if not name or name == self.name:
            if portnum:
                if portnum > self.numports:
                    return []
                return [self.outlets[portnum - 1]]
            else:
                outlets = []
                self.log.debug(str(self.onlyusedones))

                for o in self.outlets:
                    if o.inuse or not self.onlyusedones:
                        outlets.append(o)

                return outlets
        else:
            o = self.findOutletByName(name)
            if o:
                return [o]
        return []

    async def setState(self, state, name: str = "", portnum: int = 0):
        """Set the state of the Outlet instance to On/Off. (On = 1, Off = 0)

        Parameters
        ----------
        state
            The boolian value (True, False) to set the state inside the Outlet object.
        name
            The string to compare with the name in Outlet instance.
        portnum
            The integer for indicating each Outlet instances
        """
        if portnum > self.numports:
            return []

        return await self.switch(
            Outlet.parse(state), self.collectOutletsByNameAndPort(name, portnum)
        )

    async def statusAsDict(self, name: str = "", portnum: int = 0):
        """Get the status of the Outlets by dictionary.

        Parameters
        ----------
        name
            The string to compare with the name in Outlet instance.
            'name' can be a switch or an outlet name.
        portnum
            The integer for indicating each Outlet instances
        """

        outlets = self.collectOutletsByNameAndPort(name, portnum)

        await self.update(outlets)

        status = {}
        for o in outlets:
            status[f"{o.name}"] = o.toDict()

        return status

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def isReachable(self):
        """Verify we can reach the switch, returns true if ok"""
        pass

    @abstractmethod
    async def update(self, outlets):
        pass

    @abstractmethod
    async def switch(self, state, outlets):
        pass

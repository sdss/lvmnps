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
    """Powerswitch class to manage the Digital Loggers Web power switch"""

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
        """DOESNT work for keys with dots !!!"""

        def g(config, key, d=None):
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
        for o in self.outlets:
            if o.name == name:
                return o

    def collectOutletsByNameAndPort(self, name: str, portnum: int = 0):

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
        if portnum > self.numports:
            return []

        return await self.switch(
            Outlet.parse(state), self.collectOutletsByNameAndPort(name, portnum)
        )

    async def statusAsJson(self, name: str = "", portnum: int = 0):
        # name: can be a switch or an outlet name

        outlets = self.collectOutletsByNameAndPort(name, portnum)

        await self.update(outlets)

        status = {}
        for o in outlets:
            status[f"{o.name}"] = o.toJson()

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

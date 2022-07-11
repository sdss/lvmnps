# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/dummy/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

from sdsstools.logger import SDSSLogger

from lvmnps.switch.powerswitchbase import PowerSwitchBase

from lvmnps.switch.netio.Netio import Netio


__all__ = ["PowerSwitch"]


class PowerSwitch(PowerSwitchBase):
    """Powerswitch class to manage the Digital Loggers Web power switch"""

    def __init__(self, name: str, config: dict, log: SDSSLogger):
        super().__init__(name, config, log)

        for o in self.outlets:
            o.setState(0)
        hostname = self.config_get("hostname")
        username = self.config_get("username", "netio")
        password = self.config_get("password", "netio")

        self.con_url = f"http://{hostname}/netio.json"
        self.con_args = {"auth_rw": (username, password), "verify": True}
        self.portsnum = int(self.config_get("ports.num", "4"))
        
        print(self.outlets)

    async def start(self):
        if not await self.isReachable():
            self.log.warning(f"{self.name} not reachable on start up")

        await self.update(self.outlets)

    async def stop(self):
        self.log.debug(
            "For a moment, nothing happened. Then, after a second or so, "
            "nothing continued to happen ..."
        )

    async def isReachable(self):
        return Netio(self.con_url, **self.con_args)

    async def update(self, outlets):

        if switch := await self.isReachable():
            relays = switch.get_outputs()
            for o in outlets:
                o.setState(relays[o.portnum - 1].State if o.portnum <= len(relays) else -1)
        else:
            for o in outlets:
                o.setState(-1)

    async def switch(self, state, outlets):
        if switch := await self.isReachable():
            switch.set_outputs({o.portnum: Netio.ACTION.ON if state else Netio.ACTION.OFF for o in outlets})

            self.log.debug(f"{self.name} {outlets}")
            for o in outlets:
                o.setState(state)
            
        else:
            for o in outlets:
                o.setState(-1)

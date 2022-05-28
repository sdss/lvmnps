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


__all__ = ["PowerSwitch"]


class PowerSwitch(PowerSwitchBase):
    """Powerswitch class to manage the Digital Loggers Web power switch"""

    def __init__(self, name: str, config: dict, log: SDSSLogger):
        super().__init__(name, config, log)
        self.delay = self.config_get("delay", 0.0)

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
        return True

    async def update(self, outlets):
        pass

    async def switch(self, state, outlets):
        for o in outlets:
            self.log.debug(f"{self.name} set")
            await asyncio.sleep(self.delay)
            self.log.debug(f"{self.name} {outlets}")
            o.setState(state)

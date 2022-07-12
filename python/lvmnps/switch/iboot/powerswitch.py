# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/iboot/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools.logger import SDSSLogger

from lvmnps.switch.iboot.iboot import iBootInterface
from lvmnps.switch.powerswitchbase import PowerSwitchBase


__all__ = ["PowerSwitch"]


class PowerSwitch(PowerSwitchBase):
    """Powerswitch class to manage the iboot power switch"""

    def __init__(self, name: str, config: [], log: SDSSLogger):
        super().__init__(name, config, log)

        self.hostname = self.config_get("hostname")
        self.username = self.config_get("username", "admin")
        self.password = self.config_get("password", "admin")
        self.portsnum = int(self.config_get("ports.num", "1"))

        self.iboot = iBootInterface(
            self.hostname, self.username, self.password, self.portsnum, self.log
        )

    async def start(self):
        if not await self.isReachable():
            self.log.warning(f"{self.name} not reachable on start up")
        await self.update(self.outlets)

    async def stop(self):
        try:
            return self.iboot.disconnect()

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False
        self.log.debug("So Long, and Thanks for All the Fish ...")

    async def isReachable(self):
        try:
            return self.iboot.connect()

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False

    async def update(self, outlets):
        try:
            if await self.isReachable():
                relays = self.iboot.get_relays()
                for o in len(relays):
                    o.setState(relays[o.portnum - 1])
            else:
                for o in outlets:
                    o.setState(-1)

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")

    async def switch(self, state, outlets):
        self.log.debug(str(state))
        try:
            if await self.isReachable():
                for o in outlets:
                    self.iboot.switch(o.portnum, state)
            await self.update(outlets)

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")

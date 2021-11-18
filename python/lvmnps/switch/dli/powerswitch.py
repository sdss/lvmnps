# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de),
# Mingyeong Yang (mingyeong@khu.ac.kr),
# Changgon Kim (changgonkim@khu.ac.kr)
# @Date: 2021-06-24
# @Update: 2021-10-09
# @Filename: lvmnps/switch/dli/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools.logger import SDSSLogger

from lvmnps.switch.dli.dli import Dli as DliPowerSwitch
from lvmnps.switch.powerswitchbase import PowerSwitchBase


__all__ = ["PowerSwitch"]


class PowerSwitch(PowerSwitchBase):
    """Powerswitch class inherited from the PowerSwitchBase class,
    the middle library to parse commands from the actor to the Dli class.

    Parameters
    ----------
    name
        A name identifying the power switch.
        'DLI Controller' for Dli switch
    config
        The configuration defined on the .yaml file under /etc/lvmnps_dli.yml
    log
        The logger for logging
    """

    def __init__(self, name: str, config: [], log: SDSSLogger):
        super().__init__(name, config, log)

        self.hostname = self.config_get("hostname")
        self.username = self.config_get("user", "admin")
        self.password = self.config_get("password", "admin")
        self.onoff_timeout = self.config_get("onoff_timeout")

        self.dli = DliPowerSwitch(
            log=self.log,
            name=self.name,
            userid=self.username,
            password=self.password,
            hostname=self.hostname,
            onoff_timeout=self.onoff_timeout,
        )
        self.reachable = False

    async def start(self):
        """Adds the client controlling the DLI Power Switch.
        Checks if the Power switch is reachable.
        If the Power switch is reachable, updates the data of Outlet objects.

        """
        await self.dli.add_client()
        if not await self.isReachable():
            self.log.warning(f"{self.name} not reachable on start up")
        await self.update(self.outlets)

    async def stop(self):
        """Closes the connection with the httpx client."""
        try:
            await self.dli.close()

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False

        self.log.debug("So Long, and Thanks for All the Fish ...")

    async def isReachable(self):
        """Check if the Power switch is reachable by the verify
        method which is the member of Dli class."""
        try:
            self.reachable = await self.dli.verify(self.outlets)

        except Exception as ex:
            self.log.error(f"Unexpected exception is {type(ex)}: {ex}")
            self.dli = None
        return self.reachable

    async def update(self, outlets):
        """Updates the data based on the received status dictionary from the Dli class.

        Parameters
        ----------
        outlets
            list of Outlet objects defined on /switch/outlet.py
            each Oulet object indicates one of eight outlets of the dli power switch
        """
        # outlets contains all targeted ports
        self.log.debug(f"{outlets}")
        try:
            if self.reachable:
                # set the status to the real state
                await self.dli.statusdictionary()
                for o in outlets:
                    o.setState(self.dli.outlets_dict[o.portnum])
            else:
                for o in outlets:
                    o.setState(-1)
        except Exception as ex:
            self.log.error(f"Unexpected exception for {type(ex)}: {ex}")

    async def switch(self, state, outlets):
        """Controls the switch (Turning on or off)

        Parameters
        ----------
        state
            the destination of the state that each outlet will be changed.
            the type is bool. (True/False)
        outlets
            list of Outlet objects defined on /switch/outlet.py
            each Oulet object indicates one of eight outlets of the dli power switch
        """
        # outlets contains all targeted ports
        self.log.debug(f"{outlets} = {state}")
        try:
            if self.reachable:
                # either loop over the outlets or pass the outlet list.
                for o in outlets:
                    await self.dli.on(o.portnum) if state else await self.dli.off(
                        o.portnum
                    )
            await self.update(outlets)

        except Exception as ex:
            self.log.error(f"Unexpected exception to {type(ex)}: {ex}")

    async def scripting(self):
        result = await self.dli.script()
        return result

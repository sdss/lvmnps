# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/iboot/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools.logger import SDSSLogger
import datetime

from lvmnps.switch.dli.lvmpower import PowerSwitch as DliPowerSwitch
from lvmnps.switch.powerswitchbase import PowerSwitchBase


# Todo: Dont inherit clu.Device in lvmnps.switch.dli.dlipower.PowerSwitch if you are not using it.


__all__ = ['PowerSwitch']


class PowerSwitch(PowerSwitchBase):
    """ Powerswitch class to manage the iboot power switch """

    def __init__(self, name: str, config: [], log: SDSSLogger):
        super().__init__(name, config, log)

        self.hostname = self.config_get('hostname')
        self.username = self.config_get('user', 'admin')
        self.password = self.config_get('password', 'admin')
        self.use_https = self.config_get('use_https', False)

        self.dli = None

    async def start(self):
        if not await self.isReachable():
            self.log.warning(f"{self.name} not reachable on start up")

        await self.update(self.outlets)

    async def stop(self):
        try:
            pass

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False

        self.log.debug("So Long, and Thanks for All the Fish ...")


    async def isReachable(self):
        try:
            if not self.dli:
                self.dli = DliPowerSwitch(name=self.name, userid=self.username, password=self.password,
                                          hostname=self.hostname, use_https=self.use_https)
#                reachable = self.statuslist()
                reachable = await self.dli.verify()

                if not reachable:
                    self.dli = None
            return reachable

        except Exception as ex:
            self.log.error(f"Unexpected exception is {type(ex)}: {ex}")        #help me please.... to ck
            self.dli = None
            return False

    async def update(self, outlets):
        # outlets contains all targeted ports
        self.log.debug(f"{outlets}")
        #flag = await self.isReachable()
        try:
            if await self.isReachable():
                # get a list [] of port states, use outlets for a subset.
                #print("is inside reachable")
                current_time = datetime.datetime.now()
                print(f"after isReachable  :  {current_time}")

                currentstatus = await self.dli.statusdictionary()
                #print(currentstatus)
                for o in outlets:
                    o.setState(currentstatus[o.portnum])
                
                current_time = datetime.datetime.now()
                print(f"after setState  :  {current_time}")
            else:
                for o in outlets:
                    o.setState(-1)

        except Exception as ex:
            self.log.error(f"Unexpected exception for {type(ex)}: {ex}")


    async def switch(self, state, outlets):
        # outlets contains all targeted ports
        self.log.debug(f"{outlets} = {state}")
        try:
            if await self.isReachable():
                # either loop over the outlets or pass the outlet list.
                for o in outlets:
                    await self.dli.on(o.portnum) if state else await self.dli.off(o.portnum)

            await self.update(outlets)

        except Exception as ex:
            self.log.error(f"Unexpected exception to {type(ex)}: {ex}")

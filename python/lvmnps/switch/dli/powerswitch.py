# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-24
# @Filename: lvmnps/switch/iboot/powerswitch.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools.logger import SDSSLogger

from lvmnps.switch.exceptions import *
from lvmnps.switch.outlet import Outlet
from lvmnps.switch.powerswitchbase import PowerSwitchBase

from lvmnps.switch.dli.dlipower import PowerSwitch as DliPowerSwitch

# Todo: Dont inherit clu.Device in lvmnps.switch.dli.dlipower.PowerSwitch if you are not using it.


__all__ = ['PowerSwitch']

class PowerSwitch(PowerSwitchBase):
     """ Powerswitch class to manage the iboot power switch """

     def __init__(self, name: str, config: [], log: SDSSLogger):
        super().__init__(name, config, log)
        
        self.hostname = self.config_get('hostname')
        self.port = self.config_get('port', 80)
        self.username = self.config_get('user', 'admin')
        self.password = self.config_get('password', 'admin')
        
        self.dli = DliPowerSwitch(name=self.name, hostname=self.hostname, port=self.port, userid=self.username, password=self.password)
    

     async def start(self):
        if not await self.isReachable():
            self.log.warning(f"{self.name} not reachable on start up")

        await self.update(self.outlets)
    

     async def stop(self):
        try:
            # await self.dli.stop()
            pass
 
        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False

        self.log.debug("So Long, and Thanks for All the Fish ...")
    

     async def isReachable(self):
        try:
            # return self.dli.is_connected()
            return self.dli.login()

        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
            return False
 

     async def update(self, outlets):
        # outlets contains all targeted ports 
        self.log.debug(f"{outlets}")
        try:
            if await self.isReachable():
               # get a list [] of port states, use outlets for a subset. 
               # relays = self.iboot.get_relays()
               for o in outlets:
                  # set the states into internal store.
                  # o.setState(relays[o.portnum-1])
                  pass
            else:
              for o in outlets:
                 o.setState(-1)
                
        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")

 
     async def switch(self, state, outlets):
        # outlets contains all targeted ports 
        self.log.debug(f"{outlets} = {state}")
        try:
            if await self.isReachable():
                # either loop over the outlets or pass the outlet list.
                for o in outlets:
                    # self.iboot.switch(o.portnum, state)
                    pass
                
            await self.update(outlets)
            
        except Exception as ex:
            self.log.error(f"Unexpected exception {type(ex)}: {ex}")
 
        

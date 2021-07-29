#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: test.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.switch.exceptions import PowerException

from lvmnps.switch.dli.powerswitch import PowerSwitch
#from lvmnps.switch.dli.lvmpower import PowerSwitch as DliPowerSwitch


@parser.command()
async def test(command: Command, switches: PowerSwitch):
    """print the status of the NPS."""

    for switch in switches:
        try:
            #command.info(host=switch.hostname)
            #command.info(user=switch.username)
            #command.info(password=switch.password)
            command.info(Reachable=await switch.isReachable())
            #command.info(start=await switch.start())
        
        except PowerException as ex:
            return command.fail(error=str(ex))
    
    #switches.start()

    return command.finish("done")

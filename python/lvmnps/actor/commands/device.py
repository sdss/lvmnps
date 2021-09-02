#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang(mingyeong@khu.ac.kr)
# @Date: 2021-08-30
# @Filename: device.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.switch.dli.powerswitch import PowerSwitch
from lvmnps.switch.exceptions import PowerException
from lvmnps.exceptions import NpsActorError

@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def device(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """return the list of devices connected with switch"""
    
    if name:    
        command.info(info=f"Individual Control of {name}...")
        
        for switch in switches:
            current_status = await switch.statusAsJson(name, portnum)

            if current_status:
                the_switch = switch
                break
            
        try:
            outlets = []
            status = {}
            
            status = await the_switch.statusAsJson(name, portnum)
            outlets = list(status.keys())
            command.info(IndividualControl=outlets)
            
        except NpsActorError as err:
            return {str(err)}
        
        return command.finish()
    
    else:
        return command.fail(text="write the name of NPS you want to know")
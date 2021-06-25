#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.exceptions import NpsActorError

from lvmnps.actor.commands import parser

from lvmnps.switch.dli.powerswitch import PowerSwitch



async def switch_control(switches: [], on: bool, name: str, portnum: int):
    status = {}
    
    for switch in switches:
        try:
             await switch.setState(on, name, portnum)
             status |= await switch.statusAsJson(name, portnum)
           
        except NpsActorError as err:
             pass

    return status
    

@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def on(command:Command, switches: [], name: str, portnum: int):
    """Turn on the Outlet"""

    command.info( STATUS = await switch_control(switches, True, name, portnum) )

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command:Command, switches : [], name: str, portnum: int):
    """Turn off the Outlet"""

    command.info( STATUS = await switch_control(switches, False, name, portnum) )
    
    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
async def onall(command:Command, switches : [], name: str):
    """Turn on all Outlet"""

    command.info( STATUS = await switch_control(switches, True,  0, name) )

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
async def offall(command:Command, switches : [], name: str):
    """Turn off all Outlet"""

    command.info( STATUS = await switch_control(switches, False,  0, name) )
    
    return command.finish(text="done")


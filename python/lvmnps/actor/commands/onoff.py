#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-07-28
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import datetime
#from lvmnps.python.lvmnps.actor.commands.status import status

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.dli.powerswitch import PowerSwitch

async def switch_control(switches: PowerSwitch, on: bool, name: str, portnum: int):
    current_time = datetime.datetime.now()
    print(f"starting switch_control  :  {current_time}")

    status = {}

    try:
        tasks = []
        for switch in switches:
            tasks.append(asyncio.create_task(switch.setState(on, name, portnum)))
            current_time = datetime.datetime.now()
            print(f"after setState  :  {current_time}")

        await asyncio.gather(*tasks)
        current_time = datetime.datetime.now()
        print(f"after gather  :  {current_time}")

        status = dict(list(status.items()) + 
                  list((await switch.statusAsJson(name, portnum)).items()))

    except NpsActorError as err:
        return {str(err)}

    return status


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def on(command: Command, switches: [], name: str, portnum: int):
    """Turn on the Outlet"""

    command.info(STATUS=await switch_control(switches, True, name, portnum))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command: Command, switches: [], name: str, portnum: int):
    """Turn off the Outlet"""

    command.info(STATUS=await switch_control(switches, False, name, portnum))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
async def onall(command: Command, switches: [], name: str):
    """Turn on all Outlet"""

    command.info(STATUS=await switch_control(switches, True, 0, name))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def cycle(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """cycle power to an Outlet"""

    status = {}
    for switch in switches:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
        current_status = await switch.statusAsJson(name, portnum)

        command.info(text=f"cycle {name}")

        #off
        if current_status[name]['STATE'] == 1:
            await switch_control(switches, False, name, portnum)
        elif current_status[name]['STATE'] == 0:
            command.fail(text=f"The Outlet {name} is already ON")
        else:
            command.fail(text=f"The Outlet {name} returns wrong value")

        #wait
        command.info(text="WAIT...")
        await asyncio.sleep(1)

        #on
        await switch_control(switches, True, name, portnum)
        status = dict(list(status.items()) +
                          list((current_status.items())))

    command.info(STATUS=status)

    return command.finish(text="done")

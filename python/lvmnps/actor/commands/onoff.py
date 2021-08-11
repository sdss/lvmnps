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

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.exceptions import PowerException
from lvmnps.switch.dli.powerswitch import PowerSwitch


async def switch_control(switches: PowerSwitch, on: bool, name: str, portnum: int):

    current_time = datetime.datetime.now()
    print(f"starting switch_control  :  {current_time}")

    for switch in switches:
        try:
            await switch.setState(on, name, portnum)

        except NpsActorError as err:
            return {str(err)}


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def on(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn on the Outlet"""

    try:
        for switch in switches:
            command.info(text=f"Turning on port {name} in {switch.name}")
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            current_status = await switch.statusAsJson(name, portnum)

            if current_status:
                if current_status[name]["STATE"] == 0:
                    await switch_control(switches, True, name, portnum)
                elif current_status[name]["STATE"] == 1:
                    return command.fail(text=f"The Outlet {name} is already ON")
                else:
                    return command.fail(text=f"The Outlet {name} returns wrong value")
            else:
                command.info(text=f"looking for {name}")
                continue

        current_status = await switch.statusAsJson(name, portnum)

        command.info(STATUS=current_status)

    except PowerException as ex:
        return command.fail(error=str(ex))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn off the Outlet"""

    try:
        for switch in switches:
            command.info(text=f"Turning off port {name} in {switch.name}")
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            current_status = await switch.statusAsJson(name, portnum)

            if current_status:
                if current_status[name]["STATE"] == 1:
                    await switch_control(switches, False, name, portnum)
                elif current_status[name]["STATE"] == 0:
                    return command.fail(text=f"The Outlet {name} is already OFF")
                else:
                    return command.fail(text=f"The Outlet {name} returns wrong value")
            else:
                command.info(text=f"looking for {name}")
                continue

        current_status = await switch.statusAsJson(name, portnum)

        command.info(STATUS=current_status)

    except PowerException as ex:
        return command.fail(error=str(ex))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
async def onall(command: Command, switches: PowerSwitch, name: str):
    """Turn on all Outlet"""

    status = {}
    for switch in switches:
        # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
        await switch_control(switch, True, 0, name)

        current_status = await switch.statusAsJson(name)
        status = dict(list(status.items()) + list((current_status.items())))

    command.info(STATUS=status)

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def cycle(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """cycle power to an Outlet"""

    for switch in switches:
        # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
        current_status = await switch.statusAsJson(name, portnum)

        command.info(text=f"cycle {name} in {switch.name}")

        if current_status:
            # off
            if current_status[name]["STATE"] == 1:
                await switch_control(switches, False, name, portnum)
            elif current_status[name]["STATE"] == 0:
                return command.fail(text=f"The Outlet {name} is already OFF")
            else:
                return command.fail(text=f"The Outlet {name} returns wrong value")

            # wait
            command.info(text="WAIT...")
            await asyncio.sleep(1)

            # on
            await switch_control(switches, True, name, portnum)

        else:
            continue

        # result
        current_status = await switch.statusAsJson(name, portnum)

    command.info(STATUS=current_status)

    return command.finish(text="done")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio

import click

from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.switch.powerswitchbase import PowerSwitchBase as PowerSwitch


async def switch_control(command, switch, on: bool, name: str, portnum: int):
    """The function for parsing the actor command to the switch library."""
    status = {}
    if command == "on" or command == "off":
        await switch.setState(on, name, portnum)
        # status |= await switch.statusAsDict(name, portnum) works only with python 3.9
        status[switch.name] = dict(
            list(status.items())
            + list((await switch.statusAsDict(name, portnum)).items())  # noqa: W503
        )
    return status


@parser.command()
@click.argument("NAME", type=str, required=False)
@click.argument("PORTNUM", type=int, required=False, default=0)
@click.argument("OFFAFTER", type=int, default=0)
async def on(
    command: Command, switches: PowerSwitch, name: str, portnum: int, offafter: int
):
    """Turn on the outlet."""

    if portnum:
        command.info(text=f"Turning on {name} port {portnum}...")
    else:
        command.info(text=f"Turning on Outlet {name}...")
    for switch in switches:

        current_status = await switch.statusAsDict(name, portnum)
        if current_status:
            the_switch = switch
            break
    outletname_list = list(current_status.keys())
    outletname = outletname_list[0]

    if current_status[outletname]["state"] == 0:
        current_status = await switch_control("on", the_switch, True, name, portnum)
    elif current_status[outletname]["state"] == 1:
        return command.fail(text=f"The Outlet {outletname} is already ON")
    else:
        return command.fail(text=f"The Outlet {outletname} returns wrong value")

    command.info(status=current_status)
    if offafter > 0:
        command.info(f"The switch will be turned off after {offafter} seconds.")
        await asyncio.sleep(offafter - 1)
        current_status = await switch_control("off", the_switch, False, name, portnum)
        command.info(status=current_status)
    return command.finish()


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn off the outlet."""
    if portnum:
        command.info(text=f"Turning off {name} port {portnum}...")
    else:
        command.info(text=f"Turning off Outlet {name}...")

    for switch in switches:
        current_status = await switch.statusAsDict(name, portnum)

        if current_status:
            the_switch = switch
            break
    outletname_list = list(current_status.keys())
    outletname = outletname_list[0]

    if current_status[outletname]["state"] == 1:
        current_status = await switch_control("off", the_switch, False, name, portnum)
    elif current_status[outletname]["state"] == 0:
        return command.fail(text=f"The Outlet {outletname} is already OFF")
    else:
        return command.fail(text=f"The Outlet {outletname} returns wrong value")

    command.info(status=current_status)
    return command.finish()

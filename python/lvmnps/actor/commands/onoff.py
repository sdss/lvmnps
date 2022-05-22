#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import click

from lvmnps.actor.commands import parser


if TYPE_CHECKING:
    from lvmnps.actor.actor import NPSCommand
    from lvmnps.switch.powerswitchbase import PowerSwitchBase


async def switch_control(
    command: str,
    switch: PowerSwitchBase,
    on: bool,
    name: str,
    portnum: int,
):
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
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    name: str,
    portnum: int,
    offafter: int,
):
    """Turn on the outlet."""

    if portnum:
        command.info(text=f"Turning on {name} port {portnum}...")
    else:
        command.info(text=f"Turning on Outlet {name}...")

    # TODO: this could fail if multiple switches have outlets with the same name.

    the_switch: PowerSwitchBase | None = None
    current_status: dict | None = None
    for switch in switches.values():
        current_status = await switch.statusAsDict(name, portnum)
        if current_status:
            the_switch = switch
            break

    if current_status is None or the_switch is None:
        return command.fail(f"Could not find a match for {name}:{portnum}.")

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
async def off(
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    name: str,
    portnum: int,
):
    """Turn off the outlet."""

    if portnum:
        command.info(text=f"Turning off {name} port {portnum}...")
    else:
        command.info(text=f"Turning off Outlet {name}...")

    the_switch: PowerSwitchBase | None = None
    current_status: dict | None = None
    for switch in switches.values():
        current_status = await switch.statusAsDict(name, portnum)
        if current_status:
            the_switch = switch
            break

    if current_status is None or the_switch is None:
        return command.fail(f"Could not find a match for {name}:{portnum}.")

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

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
    portnum: int | None,
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
@click.argument("OUTLET", type=str)
@click.argument("PORTNUM", type=int, required=False)
@click.option(
    "--switch",
    type=str,
    help="Address this switch specifically. Otherwise the first switch "
    "with an outlet that matches NAME will be commanded.",
)
@click.option("--off-after", type=float, help="Turn off after X seconds.")
async def on(
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    outlet: str,
    portnum: int | None = None,
    switch: str | None = None,
    off_after: float | None = None,
):
    """Turn on the outlet."""

    if portnum:
        command.info(text=f"Turning on {outlet} port {portnum} ...")
    else:
        command.info(text=f"Turning on outlet {outlet} ...")

    the_switch: PowerSwitchBase | None = None
    current_status: dict | None = None
    for sw in switches.values():
        if switch and sw.name != switch:
            continue

        current_status = await sw.statusAsDict(outlet, portnum)
        if current_status:
            the_switch = sw
            break

    if current_status is None or the_switch is None:
        return command.fail(f"Could not find a match for {outlet}:{portnum}.")

    outletname_list = list(current_status.keys())
    outletname = outletname_list[0]

    if current_status[outletname]["state"] == 0:
        current_status = await switch_control("on", the_switch, True, outlet, portnum)
    elif current_status[outletname]["state"] == 1:
        return command.finish(text=f"The outlet {outletname} is already ON")
    else:
        return command.fail(text=f"The outlet {outletname} returns wrong value")

    command.info(status=current_status)

    if off_after is not None:
        command.info(f"The switch will be turned off after {off_after} seconds.")
        await asyncio.sleep(off_after - 1)
        current_status = await switch_control("off", the_switch, False, outlet, portnum)
        command.info(status=current_status)

    return command.finish()


@parser.command()
@click.argument("OUTLET", type=str)
@click.argument("PORTNUM", type=int, required=False)
@click.option(
    "--switch",
    type=str,
    help="Address this switch specifically. Otherwise the first switch "
    "with an outlet that matches NAME will be commanded.",
)
async def off(
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    outlet: str,
    portnum: int | None = None,
    switch: str | None = None,
):
    """Turn off the outlet."""

    if portnum:
        command.info(text=f"Turning off {outlet} port {portnum} ...")
    else:
        command.info(text=f"Turning off outlet {outlet} ...")

    the_switch: PowerSwitchBase | None = None
    current_status: dict | None = None
    for sw in switches.values():
        if switch and sw.name != switch:
            continue

        current_status = await sw.statusAsDict(outlet, portnum)
        if current_status:
            the_switch = sw
            break

    if current_status is None or the_switch is None:
        return command.fail(f"Could not find a match for {outlet}:{portnum}.")

    outletname_list = list(current_status.keys())
    outletname = outletname_list[0]

    if current_status[outletname]["state"] == 1:
        current_status = await switch_control("off", the_switch, False, outlet, portnum)
    elif current_status[outletname]["state"] == 0:
        return command.finish(text=f"The outlet {outletname} is already OFF")
    else:
        return command.fail(text=f"The outlet {outletname} returns wrong value")

    command.info(status=current_status)

    return command.finish()

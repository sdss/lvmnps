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
from lvmnps.switch.powerswitchbase import PowerSwitchBase as PowerSwitch


@parser.group()
def reachable():
    """Returns the list of reachable objects."""

    pass


@reachable.command()
@click.argument("SWITCHNAME", type=str)
@click.argument("PORTNUM", type=int, default=0)
async def outlets(
    command: Command, switches: PowerSwitch, switchname: str, portnum: int
):
    """Returns the list of names for each outlet on a specific power switch."""

    if switchname:
        command.info(text=f"Individual Control of {switchname}...")

        for switch in switches:
            current_status = await switch.statusAsDict(switchname, portnum)

            if current_status:
                the_switch = switch
                break

        outlets = []
        status = {}

        status = await the_switch.statusAsDict(switchname, portnum)
        outlets = list(status.keys())
        command.info(outlets=outlets)

        return command.finish()

    else:
        return command.fail(error="write the name of NPS you want to know")


@reachable.command()
async def switches(
    command: Command,
    switches: PowerSwitch,
):
    """Returns the list of switches which is reachable."""

    command.info(text="the list of switches")

    names = []

    for switch in switches:
        names.append(switch.name)

    command.info(switches=names)

    return command.finish()

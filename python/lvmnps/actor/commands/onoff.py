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

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.actor.commands import parser

#from lvmnps.switch.dli.dlipower import PowerSwitch
from lvmnps.switch.lvmpower import LVMPowerSwitch as PowerSwitch


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("OUTLET", type=int, default=0)
async def on(command: Command, switches: dict[str, PowerSwitch], name: str, outlet: int):
    """Turn on the Outlet"""

    command.info(text="Turn on the outlet %d" % (outlet))

    for switch in switches:
        try:
            await switches[switch].on(name, outlet)
        except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn on the outlet %d done!" % (outlet))


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("OUTLET", type=int, default=0)
async def off(command: Command, switches: dict[str, PowerSwitch], name: str, outlet: int):
    """Turn on the Outlet"""

    command.info(text="Turn off the outlet %d" % (outlet))

    for switch in switches:
        try:
            await switches[switch].off(name, outlet)
        except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn off the outlet %d done!" % (outlet))


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
<<<<<<< HEAD
from lvmnps.switch.dli.dlipower import PowerSwitch
=======
from lvmnps.switch.lvmpower import PowerSwitch
>>>>>>> 6fb77e8498290755cbe8025a8dc5681b3e4ef294


@parser.command()
@click.argument("OUTLET", type=float)
async def on(command:Command, switches: dict[str, PowerSwitch], outlet):
    """Turn on the Outlet"""

    command.info(text="Turn on the outlet %d" % (outlet))

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                await switches[switch].on(outlet)
            except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn on the outlet %d done!" % (outlet))

@parser.command()
@click.argument("OUTLET", type=float)
async def off(command:Command, switches : dict[str, PowerSwitch], outlet):
    """Turn off the Outlet"""

    command.info(text="Turn off the outlet %d" % (outlet))

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                await switches[switch].off(outlet)
            except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn off the outlet %d done!" % (outlet))

@parser.command()
async def onall(command:Command, switches : dict[str, PowerSwitch]):
    """Turn on all Outlet"""

    command.info(text="Turn on all of the outlet")

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                for outlet in switches[switch]:
                    await outlet.on()
            except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn on all of the outlet done!")

@parser.command()
async def offall(command:Command, switches : PowerSwitch):
    """Turn off all Outlet"""

    command.info(text="Turn off all of the outlet")

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                for outlet in switches[switch]:
                    await outlet.off()
            except NpsActorError as err:
                return command.fail(error=str(err))
    
    return command.finish(text="Turn off all of the outlet done!")


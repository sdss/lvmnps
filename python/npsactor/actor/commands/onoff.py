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

from npsactor.exceptions import NpsActorError

from npsactor.actor.commands import parser
from npsactor.switch.dlipower import PowerSwitch


@parser.command()
@click.argument("OUTLET", type=float)
async def on(command:Command, switches: dict[str, PowerSwitch], outlet):
    """Turn on the Outlet"""

    command.info(text="Turn on the outlet %d" % (outlet))

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                switches[switch].on(outlet)
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
                switches[switch].off(outlet)
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
                    outlet.on()
            except NpsActorError as err:
                return command.fail(error=str(err))

    return command.finish(text="Turn on all of the outlet done!")

@parser.command()
async def offall(command:Command, switch : PowerSwitch):
    """Turn off all Outlet"""

    command.info(text="Turn off all of the outlet")

    for switch in switches:
        if switches[switch].name == 'nps1':
            try:
                for outlet in switches[switch]:
                    outlet.off()
            except NpsActorError as err:
                return command.fail(error=str(err))
    
    return command.finish(text="Turn off all of the outlet done!")


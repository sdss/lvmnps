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

#from npsactor.controller.controller import NpsController
from npsactor.exceptions import NpsActorError

#from ..tools import check_controller, error_controller, parallel_controllers
from npsactor.actor.commands import parser

import dlipower

switch = dlipower.PowerSwitch(hostname="10.7.45.22",userid="admin",password='rLXR3KxUqiCPGvA')

@parser.command()
@click.argument("OUTLET", type=float)
async def on(command:Command, outlet):
    """Turn on the Outlet"""

    command.info(text="Turn on the outlet %d" % (outlet))

    switch.on(outlet)

    return command.finish(text="Turn on the outlet %d done!" % (outlet))

@parser.command()
@click.argument("OUTLET", type=float)
async def off(command:Command, outlet):
    """Turn off the Outlet"""

    command.info(text="Turn off the outlet %d" % (outlet))

    switch.off(outlet)

    return command.finish(text="Turn off the outlet %d done!" % (outlet))

@parser.command()
async def onall(command:Command):
    """Turn on all Outlet"""

    command.info(text="Turn on all of the outlet")

    for outlet in switch:
        outlet.on()
    return command.finish(text="Turn on all of the outlet done!")

@parser.command()
async def offall(command:Command):
    """Turn off all Outlet"""

    command.info(text="Turn off all of the outlet")

    for outlet in switch:
        outlet.off()
    return command.finish(text="Turn off all of the outlet done!")


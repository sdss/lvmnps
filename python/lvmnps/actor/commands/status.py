#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.switch.dli.powerswitch import PowerSwitch
from lvmnps.switch.exceptions import PowerException


@parser.group()
def status(*args):
    """print the status of the NPS."""
    pass


@status.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def what(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Returns the status of the outlets."""

    command.info(
        text=f"Printing the current status of port {name}"
        )
    
    try:
        for switch in switches:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            current_status = await switch.statusAsJson(name, portnum)
            
            if current_status:
                return command.finish(STATUS=current_status)
            else:
                return command.fail(text=f"The Outlet {name} don't exist")

    except PowerException as ex:
        return command.fail(error=str(ex))


@status.command()
async def all(command: Command, switches: PowerSwitch):
    """Returns the status of ALL outlets in the NPS."""
    
    status = {}
    
    try:
        for switch in switches:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            command.info(text=f"Printing the current status of switch {switch.name}")

            current_status = await switch.statusAsJson()
            status = dict(list(status.items()) + list((current_status.items())))
            
            return command.finish(STATUS=status)

        except PowerException as ex:
            return command.fail(error=str(ex))


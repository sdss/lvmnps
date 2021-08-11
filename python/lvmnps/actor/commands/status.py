#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-07-28
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

    try:
        for switch in switches:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            command.info(
                text=f"Printing the current status of port {name} in {switch.name}"
            )
            # print(f"before switch getting status  :  {current_time}")

            current_status = await switch.statusAsJson(name, portnum)
            # print(f"after switch getting status  :  {current_time}")

            # print(current_status)
            # command.info(STATUS=current_status)

            if current_status:
                break
            else:
                command.info(text=f"{name} is not here!")

        if current_status:
            command.info(STATUS=current_status)
        else:
            return command.fail(text="The switch returns wrong value")

    except PowerException as ex:
        return command.fail(error=str(ex))

    return command.finish("done")


@status.command()
async def all(command: Command, switches: PowerSwitch):
    """Returns the status of ALL outlets in the NPS."""

    status = {}

    for switch in switches:
        try:

            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            command.info(text=f"Printing the current status of switch {switch.name}")

            current_status = await switch.statusAsJson()
            status = dict(list(status.items()) + list((current_status.items())))
            command.info(STATUS=status)

        except PowerException as ex:
            return command.fail(error=str(ex))

    return command.finish("done")

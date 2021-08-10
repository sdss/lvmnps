#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-07-28
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations
import asyncio

import click
from clu.command import Command
import datetime

from lvmnps.actor.commands import parser
from lvmnps.switch.exceptions import PowerException
from lvmnps.switch.dli.powerswitch import PowerSwitch

@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def status(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """print the status of the NPS."""

    status = {}

    for switch in switches:
        try:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            command.info(text=f"Printing the current status of switch {name}")
            current_time = datetime.datetime.now()
            print(f"before switch getting status  :  {current_time}")

            current_status = await switch.statusAsJson(name, portnum)
            current_time = datetime.datetime.now()
            print(f"after switch getting status  :  {current_time}")

            if current_status[name]:
                status = dict(list(status.items()) +
                          list((current_status.items())))
            else:
                return command.fail(text="The switch returns wrong value")

        except PowerException as ex:
            return command.fail(error=str(ex))

    command.info(
        STATUS=status
    )

    return command.finish("done")


@parser.command()
async def statusall(command: Command, switches: PowerSwitch):
    """print the status of ALL outlets in the NPS."""

    status = {}

    for switch in switches:
        try:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            command.info(text="Printing the current status of switch")

            current_status = await switch.statusAsJson()
            
            status = dict(list(status.items()) +
                          list((current_status.items())))

        except PowerException as ex:
            return command.fail(error=str(ex))

    command.info(
        STATUS=status
    )

    return command.finish("done")
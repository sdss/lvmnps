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
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.powerswitchbase import PowerSwitchBase as PowerSwitch


@parser.command()
@click.argument("SWITCHNAME", type=str, required=False)
@click.argument("PORTNUM", type=int, default=0)
async def status(
    command: Command, switches: PowerSwitch, switchname: str, portnum: int
):
    """Returns the dictionary of a specific outlet."""

    if switchname is None:
        command.info(text="Printing the current status of all outlets")
    elif switchname:
        if portnum:
            command.info(
                text=f"Printing the current status of switch {switchname}, port {portnum}"
            )
        else:
            command.info(text=f"Printing the current status of switch {switchname}")

    try:
        status = {}
        if switchname is None:
            for switch in switches:
                current_status = await switch.statusAsDict()
                if current_status:
                    status[switch.name] = current_status
        elif switchname:
            for switch in switches:
                # status |= await switch.statusAsDict(name, portnum) works only with python 3.9
                if switchname == switch.name:
                    if portnum:
                        current_status = await switch.statusAsDict(switchname, portnum)
                    else:
                        current_status = await switch.statusAsDict(switchname)
                    if current_status:
                        status[switch.name] = current_status
                        break

    except NpsActorError as ex:
        return command.fail(error=str(ex))

    command.info(status=status)
    return command.finish()

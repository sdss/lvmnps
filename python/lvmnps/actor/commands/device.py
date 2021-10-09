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
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.dli.powerswitch import PowerSwitch


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def device(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Returns the list of names for each outlet on a specific power switch."""

    if name:
        command.info(info=f"Individual Control of {name}...")

        for switch in switches:
            current_status = await switch.statusAsDict(name, portnum)

            if current_status:
                the_switch = switch
                break

        try:
            outlets = []
            status = {}

            status = await the_switch.statusAsDict(name, portnum)
            outlets = list(status.keys())
            command.info(IndividualControl=outlets)

        except NpsActorError as err:
            return command.error(str(err))
        return command.finish()

    else:
        return command.fail(text="write the name of NPS you want to know")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.dli.powerswitch import PowerSwitch


async def switch_control(command, switch, on: bool, name: str, portnum: int):
    """The function for parsing the actor command to the switch library."""
    status = {}
    try:
        if command == "on" or command == "off":
            await switch.setState(on, name, portnum)
            # status |= await switch.statusAsDict(name, portnum) works only with python 3.9
            status[switch.name] = dict(
                list(status.items())
                + list((await switch.statusAsDict(name, portnum)).items())  # noqa: W503
            )
    except NpsActorError as err:
        return {str(err)}

    return status


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def on(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn on the outlet."""

    command.info(info=f"Turning on port {name}...")

    for switch in switches:
        current_status = await switch.statusAsDict(name, portnum)

        if current_status:
            the_switch = switch
            break

    try:
        if current_status[name]["STATE"] == 0:
            current_status = await switch_control("on", the_switch, True, name, portnum)
            print(current_status)
        elif current_status[name]["STATE"] == -1:
            current_status = await switch_control("on", the_switch, True, name, portnum)
        elif current_status[name]["STATE"] == 1:
            return command.fail(text=f"The Outlet {name} is already ON")
        else:
            return command.fail(text=f"The Outlet {name} returns wrong value")

    except NpsActorError as ex:
        return command.fail(error=str(ex))

    command.info(STATUS=current_status)
    return command.finish()


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn off the outlet."""

    command.info(info=f"Turning off port {name}...")

    for switch in switches:
        current_status = await switch.statusAsDict(name, portnum)

        if current_status:
            the_switch = switch
            break

    try:
        if current_status[name]["STATE"] == 1:
            current_status = await switch_control(
                "off", the_switch, False, name, portnum
            )
        elif current_status[name]["STATE"] == -1:
            current_status = await switch_control(
                "off", the_switch, False, name, portnum
            )
        elif current_status[name]["STATE"] == 0:
            return command.fail(text=f"The Outlet {name} is already OFF")
        else:
            return command.fail(text=f"The Outlet {name} returns wrong value")

    except NpsActorError as ex:
        return command.fail(error=str(ex))

    command.info(STATUS=current_status)
    return command.finish()

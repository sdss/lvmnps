#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-07-28
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.dli.powerswitch import PowerSwitch
from lvmnps.switch.exceptions import PowerException


async def switch_control(
    command, switches: PowerSwitch, on: bool, name: str, portnum: int
):

    status = {}

    for switch in switches:
        try:
            if command == "on" or command == "off":
                await switch.setState(on, name, portnum)
                # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
                status = dict(
                    list(status.items())
                    + list(  # noqa: W503
                        (await switch.statusAsJson(name, portnum)).items()
                    )
                )
            elif command == "cycle":
                await switch.cycle(name, portnum)
                status = dict(
                    list(status.items())
                    + list(  # noqa: W503
                        (await switch.statusAsJson(name, portnum)).items()
                    )
                )
        except NpsActorError as err:
            return {str(err)}

    return status


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def on(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn on the Outlet"""
    for switch in switches:
        current_status = await switch.statusAsJson(name, portnum)
        if current_status:
            break

    print(current_status)

    try:
        if current_status:
            if current_status[name]["STATE"] == 0:
                current_status = await switch_control(
                    "on", switches, True, name, portnum
                )
            elif current_status[name]["STATE"] == -1:
                current_status = await switch_control(
                    "on", switches, True, name, portnum
                )
            elif current_status[name]["STATE"] == 1:
                return command.fail(text=f"The Outlet {name} is already ON")
            else:
                return command.fail(text=f"The Outlet {name} returns wrong value")
        command.info(STATUS=current_status)
    except PowerException as ex:
        return command.fail(error=str(ex))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def off(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """Turn off the Outlet"""

    for switch in switches:
        current_status = await switch.statusAsJson(name, portnum)

    print(current_status)

    current_status = await switch.statusAsJson(name, portnum)

    try:
        if current_status:
            if current_status[name]["STATE"] == 1:
                current_status = await switch_control(
                    "off", switch, True, name, portnum
                )
            elif current_status[name]["STATE"] == -1:
                current_status = await switch_control(
                    "off", switch, True, name, portnum
                )
            elif current_status[name]["STATE"] == 0:
                return command.fail(text=f"The Outlet {name} is already OFF")
            else:
                return command.fail(text=f"The Outlet {name} returns wrong value")
        command.info(STATUS=current_status)
    except PowerException as ex:
        return command.fail(error=str(ex))

    return command.finish(text="done")


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def cycle(command: Command, switches: PowerSwitch, name: str, portnum: int):
    """cycle power to an Outlet"""
    for switch in switches:
        current_status = await switch.statusAsJson(name, portnum)

    print(current_status)

    # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
    current_status = await switch.statusAsJson(name, portnum)

    if current_status:
        # off
        if current_status[name]["STATE"] == 1:
            current_status = await switch_control(
                "cycle", switches, False, name, portnum
            )
        elif current_status[name]["STATE"] == 0:
            return command.fail(text=f"The Outlet {name} is OFF")
        else:
            return command.fail(text=f"The Outlet {name} returns wrong value")
    command.info(STATUS=current_status)
    return command.finish(text="done")


"""
@parser.command()
@click.argument("NAME", type=str, default="")
async def onall(command: Command, switches: PowerSwitch, name: str):

    status = {}
    for switch in switches:
        # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
        await switch_control(switch, True, 0, name)

        current_status = await switch.statusAsJson(name)
        status = dict(list(status.items()) + list((current_status.items())))

    command.info(STATUS=status)

    return command.finish(text="done")
"""

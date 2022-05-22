#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from lvmnps.actor.commands import parser


if TYPE_CHECKING:
    from lvmnps.actor.actor import NPSCommand
    from lvmnps.switch.powerswitchbase import PowerSwitchBase


@parser.command()
@click.argument("SWITCHNAME", type=str, required=False)
@click.argument("PORTNUM", type=int, required=False)
@click.option(
    "-o",
    "--outlet",
    type=str,
    help="Print only the information for this outlet.",
)
async def status(
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    switchname: str | None = None,
    portnum: int | None = None,
    outlet: str | None = None,
):
    """Returns the dictionary of a specific outlet."""

    if switchname and switchname not in switches:
        return command.fail(f"Unknown switch {switchname}.")

    status = {}
    if switchname is None:
        for switch in switches.values():
            if not await switch.isReachable():
                continue
            current_status = await switch.statusAsDict(outlet, portnum)
            if current_status:
                status[switch.name] = current_status
    else:
        switch = switches[switchname]
        if await switch.isReachable():
            current_status = await switch.statusAsDict(outlet, portnum)
            if current_status:
                status[switch.name] = current_status

    if status == {}:
        return command.fail("Unable to find matching outlets.")

    return command.finish(message={"status": status})

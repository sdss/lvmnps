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
from lvmnps.switch.powerswitchbase import PowerSwitchBase as PowerSwitch


@parser.command()
@click.argument("SWITCH", type=str, required=False)
@click.argument("PORT", type=int, required=False)
@click.option("--outlet", type=str, help="Print only the information for this outlet.")
async def status(
    command: Command,
    switches: dict[str, PowerSwitch],
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
            current_status = await switch.statusAsDict(outlet, portnum)
            if current_status:
                status[switch.name] = current_status
    else:
        switch = switches[switchname]

        current_status = await switch.statusAsDict(switchname, portnum)
        if current_status:
            status[switch.name] = current_status

    if status == {}:
        return command.fail("Unable to find matching outlets.")

    return command.finish(status=status)

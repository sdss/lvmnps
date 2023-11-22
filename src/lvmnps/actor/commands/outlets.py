#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-05-22
# @Filename: outlets.py
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
async def outlets(
    command: NPSCommand,
    switches: dict[str, PowerSwitchBase],
    switchname: str | None = None,
):
    """Returns the list of names for each outlet on a specific power switch."""

    if switchname:
        if switchname not in switches:
            return command.fail(f"Unknown switch {switchname}.")
        switch_instances = [switches[switchname]]
    else:
        switch_instances = list(switches.values())

    outlets = []
    for switch in switch_instances:
        for o in switch.outlets:
            if o.inuse or not switch.onlyusedones:
                outlets.append(o.name)

    return command.finish(outlets=outlets)

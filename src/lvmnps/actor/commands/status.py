#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from lvmnps.actor.commands.onoff import OutletNameParamType

from . import lvmnps_command_parser


if TYPE_CHECKING:
    from src.lvmnps.actor.actor import NPSCommand


__all__ = ["status"]


@lvmnps_command_parser.command()
@click.argument("OUTLET", type=OutletNameParamType(), required=False)
async def status(command: NPSCommand, outlet: int | str | None = None):
    """Outputs the status of the network power switch.

    If an OUTLET is passed, returns only the status of that outlet.

    """

    nps = command.actor.nps

    await nps.refresh()

    if outlet is not None:
        try:
            outlet_obj = nps.get(outlet)
            return command.finish(outlet_info=outlet_obj.model_dump())
        except Exception:
            return command.fail(f"Invalid outlet {outlet!r}.")

    command.info(nps_type=nps.nps_type)
    command.info(outlet_names=list(nps.outlets))

    outlets = [outlet.model_dump() for outlet in nps.outlets.values()]
    command.info(outlets=outlets)

    command.finish()

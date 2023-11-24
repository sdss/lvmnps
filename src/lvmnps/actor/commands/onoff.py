#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: onoff.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from . import lvmnps_command_parser


if TYPE_CHECKING:
    from src.lvmnps.actor.actor import NPSCommand


__all__ = ["on", "off", "cycle", "all_off"]


class OutletNameParamType(click.ParamType):
    name = "outlet_name"

    def convert(self, value, param, ctx):
        if isinstance(value, int):
            return value

        try:
            return int(value, 10)
        except ValueError:
            return value


@lvmnps_command_parser.command()
@click.argument("OUTLETS", type=OutletNameParamType(), nargs=-1)
@click.option("--off-after", type=float, help="Turns the outlet off after N seconds.")
async def on(
    command: NPSCommand,
    outlets: tuple[str | int, ...],
    off_after: float | None = None,
):
    """Turns an outlet or outlets on.

    OUTLETS can be a single outlet name or outlet ID, or a list of them that will
    be switched on as quickly as possible. An argument that can be casted into
    an integer will be considered an outlet ID.

    """

    nps = command.actor.nps

    outlet_data = await nps.set_state(outlets, on=True, off_after=off_after)

    command.finish(outlets=[outlet.model_dump() for outlet in outlet_data])


@lvmnps_command_parser.command()
@click.argument("OUTLETS", type=OutletNameParamType(), nargs=-1)
async def off(command: NPSCommand, outlets: tuple[str | int, ...]):
    """Turns an outlet or outlets off.

    OUTLETS can be a single outlet name or outlet ID, or a list of them that will
    be switched on as quickly as possible. An argument that can be casted into
    an integer will be considered an outlet ID.

    """

    nps = command.actor.nps

    outlet_data = await nps.set_state(outlets, on=False)

    command.finish(outlets=[outlet.model_dump() for outlet in outlet_data])


@lvmnps_command_parser.command()
@click.argument("OUTLETS", type=OutletNameParamType(), nargs=-1)
@click.option(
    "--delay",
    type=float,
    default=3,
    help="Delay between off an on in seconds",
)
async def cycle(command: NPSCommand, outlets: tuple[str | int, ...], delay: float = 3):
    """Cycles an outlet or outlets.

    OUTLETS can be a single outlet name or outlet ID, or a list of them that will
    be switched on as quickly as possible. An argument that can be casted into
    an integer will be considered an outlet ID.

    """

    nps = command.actor.nps

    outlet_data = await nps.cycle(outlets, delay=delay)

    command.finish(outlets=[outlet.model_dump() for outlet in outlet_data])


@lvmnps_command_parser.command()
async def all_off(command: NPSCommand):
    """Turns all outlets off."""

    nps = command.actor.nps

    await nps.all_off()

    return command.finish()

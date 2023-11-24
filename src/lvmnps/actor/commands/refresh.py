#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: refresh.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from . import lvmnps_command_parser


if TYPE_CHECKING:
    from src.lvmnps.actor.actor import NPSCommand


__all__ = ["refresh"]


@lvmnps_command_parser.command()
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Does not output status after refreshing",
)
async def refresh(command: NPSCommand, quiet: bool = False):
    """Refreshes the internal list of outlets."""

    nps = command.actor.nps

    await nps.refresh()

    if not quiet:
        await command.child_command("status")

    command.finish()

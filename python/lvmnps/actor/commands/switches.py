#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2022-05-22
# @Filename: switches.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

from . import parser


if TYPE_CHECKING:
    from lvmnps.actor.actor import NPSCommand
    from lvmnps.switch.powerswitchbase import PowerSwitchBase


@parser.command()
async def switches(command: NPSCommand, switches: dict[str, PowerSwitchBase]):
    """Lists the available switches."""

    return command.finish(switches=list(switches.keys()))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

from . import lvmnps_command_parser


if TYPE_CHECKING:
    from src.lvmnps.actor.actor import NPSCommand


__all__ = ["status"]


@lvmnps_command_parser.command()
async def status(command: NPSCommand):
    """Returns the status of the network power switch."""

    command.finish()

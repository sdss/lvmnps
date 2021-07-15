#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError

from lvmnps.switch.lvmpower import LVMPowerSwitch as PowerSwitch

@parser.command()
async def status(command: Command, switches: dict[str, PowerSwitch]):
    """print the status of the NPS."""
    
    for switch in switches:
        try:
            await switches[switch].add_client()
            get = await switches[switch].getstatus()
            command.info(text="Status of the NPS", status = get)
            await switches[switch].close()
        except NpsActorError as err:
            return command.fail(error=str(err))

    return command.finish()

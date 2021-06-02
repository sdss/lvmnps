#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from clu.command import Command
from lvmnps.actor.commands import parser
from lvmnps.switch.dlipower import PowerSwitch
from lvmnps.exceptions import NpsActorError

@parser.command()
async def status(command: Command, switches: dict[str, PowerSwitch]):
    """print the status of the NPS."""
    
    for switch in switches:
        if switches[switch].name == 'nps1':
            command.info(text='name is nps1')
        try:
            get = await switches[switch].getstatus()
            command.info(text="Status of the NPS", status = get)
        except NpsActorError as err:
            return command.fail(error=str(err))

    return command.finish()

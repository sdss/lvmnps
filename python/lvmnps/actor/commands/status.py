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
from requests.api import get
from lvmnps.switch.dli.dlipower import PowerSwitch

#switch = dlipower.PowerSwitch(hostname="10.7.45.22",userid="admin",password='rLXR3KxUqiCPGvA')

@parser.command()
async def status(command: Command, switches: dict[str, PowerSwitch]):
    """print the status of the NPS."""
    
    for switch in switches:
        try:
            get = switches[switch].getstatus()
            command.info(text="Status of the NPS", status = get)
        except NpsActorError as err:
            return command.fail(error=str(err))

    return command.finish()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from clu.command import Command
from npsactor.actor.commands import parser
from npsactor.switch import dlipower
from npsactor.switch.dlipower import PowerSwitch
from npsactor.exceptions import NpsActorError
#import dlipower

#switch = dlipower.PowerSwitch(hostname="10.7.45.22",userid="admin",password='rLXR3KxUqiCPGvA')

@parser.command()
async def status(command: Command, switches: dict[str, PowerSwitch]):
    """print the status of the NPS."""
    
    for switch in switches:
        if switches[switch].name == 'nps1':
            command.info(text='name is nps1')
        try:
            command.info(text="Status of the NPS", status = switches[switch].getstatus())
        except NpsActorError as err:
            return command.fail(error=str(err))
    """
    command.info(
        status = {
            "outlet_1":switch[0].name,
            "state_1":switch[0].state,
            "outlet_2":switch[1].name,
            "state_2":switch[1].state,
            "outlet_3":switch[2].name,
            "state_3":switch[2].state,
            "outlet_4":switch[3].name,
            "state_4":switch[3].state,
            "outlet_5":switch[4].name,
            "state_5":switch[4].state,
            "outlet_6":switch[5].name,
            "state_6":switch[5].state,
            "outlet_7":switch[6].name,
            "state_7":switch[6].state,
            "outlet_8":switch[7].name,
            "state_8":switch[7].state,
        }
    )
    """
    return command.finish()

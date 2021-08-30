#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang(mingyeong@khu.ac.kr)
# @Date: 2021-08-30
# @Filename: switches.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.switch.dli.powerswitch import PowerSwitch
from lvmnps.switch.exceptions import PowerException
from lvmnps.exceptions import NpsActorError

@parser.command()
async def switches(command: Command, switches: PowerSwitch,):
    """return the list of switches"""
    
    command.info(text=f"the list of switches")
    
    try:
        names = []
        
        for switch in switches:
            names.append(switch.name)

        command.info(list=names)
        
    except NpsActorError as err:
        return {str(err)}
    
    return command.finish(text="done")
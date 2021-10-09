#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang(mingyeong@khu.ac.kr)
# @Date: 2021-08-30
# @Filename: switches.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.dli.powerswitch import PowerSwitch


@parser.command()
async def switches(
    command: Command,
    switches: PowerSwitch,
):
    """Returns the list of switches which is reachable."""

    command.info(info="the list of switches")

    try:
        names = []

        for switch in switches:
            names.append(switch.name)

        command.info(list=names)

    except NpsActorError as err:
        return {str(err)}

    return command.finish()

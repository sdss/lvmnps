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
from lvmnps.switch.exceptions import PowerException


@parser.command()
@click.argument("NAME", type=str, default="")
@click.argument("PORTNUM", type=int, default=0)
async def status(command: Command, switches: [], name: str, portnum: int):
    """print the status of the NPS."""

    status = {}

    for switch in switches:
        try:
            # status |= await switch.statusAsJson(name, portnum) works only with python 3.9
            status = dict(list(status.items()) + list((await switch.statusAsJson(name, portnum)).items()))

        except PowerException as ex:
            return command.fail(error=str(ex))

    command.info(
        STATUS=status
    )

    return command.finish("done")

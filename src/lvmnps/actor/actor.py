#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr), Florian Briegel (briegel@mpia.de)
# @Date: 2021-03-22
# @Filename: lvmnps/actor/actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pathlib
from os import PathLike

from typing import TYPE_CHECKING

from clu import Command
from clu.actor import AMQPActor

from lvmnps import __version__
from lvmnps import log as nps_log
from lvmnps.actor.commands import lvmnps_command_parser


if TYPE_CHECKING:
    from sdsstools.logger import SDSSLogger


__all__ = ["NPSActor"]


AnyPath = str | PathLike[str]


class NPSActor(AMQPActor):
    """LVM network power switches base actor."""

    parser = lvmnps_command_parser

    def __init__(
        self,
        *args,
        schema: AnyPath | None = None,
        log: SDSSLogger | None = None,
        **kwargs,
    ):
        cwd = pathlib.Path(__file__).parent

        schema = schema or cwd / "schema.json"
        log = log or nps_log

        kwargs["version"] = __version__

        super().__init__(*args, log=log, schema=schema, **kwargs)


NPSCommand = Command[NPSActor]

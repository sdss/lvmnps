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
from sdsstools.configuration import Configuration

from lvmnps import __version__
from lvmnps import log as nps_log
from lvmnps.actor.commands import lvmnps_command_parser
from lvmnps.nps.core import NPSClient
from lvmnps.nps.implementations import VALID_NPS_TYPES


if TYPE_CHECKING:
    from sdsstools.logger import SDSSLogger


__all__ = ["NPSActor"]


AnyPath = str | PathLike[str]


def get_nps_from_config(config: Configuration) -> NPSClient:
    """Returns an `.NPSClient` instance from the configuration parameters."""

    if "nps" not in config:
        raise ValueError("nps section does not exist in the configuration.")

    nps_type = config["nps.type"]
    if nps_type is None:
        raise ValueError("nps.type not defined.")

    if nps_type not in VALID_NPS_TYPES:
        raise ValueError(f"Invalid NPS {nps_type}. Valid types are {VALID_NPS_TYPES}.")

    init_parameters = config.get("nps.init_parameters", {})

    if nps_type == "dli":
        from lvmnps.nps.implementations.dli import DLIClient

        return DLIClient(**init_parameters)

    elif nps_type == "netio":
        from lvmnps.nps.implementations.netio import NetIOClient

        return NetIOClient(**init_parameters)

    else:  # pragma: no cover - This should unreachable.
        raise ValueError(f"Invalid NPS {nps_type}. Valid types are {VALID_NPS_TYPES}.")


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

        if not isinstance(self.config, Configuration):
            self.config = Configuration(self.config)

        self.nps = get_nps_from_config(self.config)

    async def start(self, **kwargs):  # pragma: no cover
        """Starts the actor."""

        await self.nps.setup()

        return await super().start(**kwargs)

    async def stop(self):
        "Stops the actor."

        await self.nps.stop()

        return await super().stop()


NPSCommand = Command[NPSActor]

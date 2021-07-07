#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import os
import warnings
from contextlib import suppress

from lvmnps.actor.commands import parser as nps_command_parser
from clu.actor import AMQPActor
<<<<<<< HEAD
from lvmnps.switch.dli.dlipower import PowerSwitch
=======
from lvmnps.switch.lvmpower import PowerSwitch
from lvmnps.exceptions import NpsActorUserWarning
>>>>>>> 6fb77e8498290755cbe8025a8dc5681b3e4ef294

__all__ = ["lvmnps"]

class lvmnps(AMQPActor):
    """NPS actor.
    In addition to the normal arguments and keyword parameters for
    `~clu.actor.AMQPActor`, the class accepts the following parameters.
    Parameters (TBD)
    """
    parser = nps_command_parser # commands register..CK 20210402

    def __init__(
            self,
            *args,
            switches: tuple[PowerSwitch, ...] = (),
            **kwargs
    ):
        self.switches = {s.name: s for s in switches}
        self.parser_args = [self.switches]
        super().__init__(*args, **kwargs)

    async def start(self):
        connect_timeout = self.config["timeouts"]["switch_connect"]

        for switch in self.switches.values():
            try:
                await asyncio.wait_for(super().start(), timeout=connect_timeout)
            except asyncio.TimeoutError:
                warnings.warn(
                    f"Timeout out connecting to {switch.name!r}.",
                    NpsActorUserWarning,
                )

<<<<<<< HEAD
       
=======
>>>>>>> 6fb77e8498290755cbe8025a8dc5681b3e4ef294
    async def stop(self):
        with suppress(asyncio.CancelledError):
            for task in self._fetch_log_jobs:
                task.cancel()
                await task
        return super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from a configuration file."""

        instance = super(lvmnps, cls).from_config(config, *args, **kwargs)

        assert isinstance(instance,lvmnps)
        assert isinstance(instance.config, dict)

        if "switches" in instance.config:
            switches = (
                PowerSwitch(
                    hostname=ctr["host"],
                    port=ctr["port"],
                    userid="admin",
                    password=ctr["password"]
                )
                for (ctrname, ctr) in instance.config["switches"].items()
            )
            instance.switches = {s.name: s for s in switches}
            instance.parser_args = [instance.switches]
        return instance

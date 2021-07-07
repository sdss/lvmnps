#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr), Florian Briegel (briegel@mpia.de)
# @Date: 2021-03-22
# @Filename: lvmnps/actor/actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
from contextlib import suppress

from clu.actor import AMQPActor
from lvmnps.switch.dli.dlipower import PowerSwitch
from lvmnps.exceptions import NpsActorUserWarning
from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory

__all__ = ["lvmnps"]


class lvmnps(AMQPActor):
    """NPS actor.
    In addition to the normal arguments and keyword parameters for
    `~clu.actor.AMQPActor`, the class accepts the following parameters.
    Parameters (TBD)
    """

    parser = nps_command_parser  # commands register..CK 20210402

    def __init__(
            self,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

    async def start(self):
        connect_timeout = self.config["timeouts"]["switch_connect"]

        assert len(self.parser_args) == 1

        for switch in self.parser_args[0]:
            try:
                await asyncio.wait_for(super().start(), timeout=connect_timeout)
            except asyncio.TimeoutError:
                warnings.warn(
                    f"Timeout out connecting to {switch.name!r}.",
                    NpsActorUserWarning,
                )

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

        assert isinstance(instance, lvmnps)
        assert isinstance(instance.config, dict)
        if "switches" in instance.config:
            switches = []
            for (name, config) in instance.config["switches"].items():
                instance.log.info(f"Instance {name}: {config}")
                try:
                    switches.append(powerSwitchFactory(name, config, instance.log))

                except Exception as ex:
                    instance.log.error(f"Error in power switch factory {type(ex)}: {ex}")
            instance.parser_args = [switches]

        return instance

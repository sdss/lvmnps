#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr), Florian Briegel (briegel@mpia.de)
# @Date: 2021-03-22
# @Filename: lvmnps/actor/actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import os

from clu.actor import AMQPActor

from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory


__all__ = ["lvmnps"]


class lvmnps(AMQPActor):
    """LVM network power switches base actor.
    Subclassed from the AMQPActor class.
    """

    parser = nps_command_parser

    def __init__(self, *args, **kwargs):

        if "schema" not in kwargs:
            kwargs["schema"] = os.path.join(
                os.path.dirname(__file__),
                "../etc/schema.json",
            )
        super().__init__(*args, **kwargs)
        self.connect_timeout = 3

    async def start(self):
        """Start the actor and connect the power switches."""
        await super().start()

        self.connect_timeout = self.config["timeouts"]["switch_connect"]

        assert len(self.parser_args) == 1
        # self.parser_args[0] is the list of switch instances
        for switch in self.parser_args[0]:
            # switch is the instance of the power switch from the PowerSwitchFactory
            try:
                self.log.debug(f"Start {switch.name} ...")
                await asyncio.wait_for(switch.start(), timeout=self.connect_timeout)

            except Exception as ex:
                self.log.error(f"Unexpected exception {type(ex)}: {ex}")

        # self.load_schema(self.schema, is_file=False)

        self.log.debug("Start done")
        # self.log.debug(str(self.schema))

    async def stop(self):
        """Stop the actor and connect the power switches."""
        for switch in self.parser_args[0]:
            try:
                self.log.debug(f"Stop {switch.name} ...")
                await asyncio.wait_for(switch.stop(), timeout=self.connect_timeout)

            except Exception as ex:
                self.log.error(f"Unexpected exception dd {type(ex)}: {ex}")

        return super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from a configuration file."""

        instance = super(lvmnps, cls).from_config(config, *args, **kwargs)

        assert isinstance(instance, lvmnps)
        assert isinstance(instance.config, dict)
        switches = []

        if "switches" in instance.config:
            for (name, config) in instance.config["switches"].items():
                instance.log.info(f"Instance {name}: {config}")
                try:
                    switches.append(powerSwitchFactory(name, config, instance.log))

                except Exception as ex:
                    instance.log.error(
                        f"Error in power switch factory {type(ex)}: {ex}"
                    )
            instance.parser_args = [switches]

        return instance

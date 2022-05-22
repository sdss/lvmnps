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
from typing import ClassVar, Dict

import click

from clu import Command
from clu.actor import AMQPActor

from lvmnps.actor.commands import parser as nps_command_parser
from lvmnps.switch.factory import powerSwitchFactory


__all__ = ["NPSActor"]


class NPSActor(AMQPActor):
    """LVM network power switches base actor.

    Subclassed from the `.AMQPActor` class.

    """

    parser: ClassVar[click.Group] = nps_command_parser
    BASE_CONFIG: ClassVar[str | Dict | None] = None

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

        if "timeouts" in self.config and "switch_connect" in self.config["timeouts"]:
            self.connect_timeout = self.config["timeouts"]["switch_connect"]

        assert len(self.parser_args) == 1

        switches = list(self.parser_args[0].values())

        # self.parser_args[0] is the list of switch instances

        tasks = [
            asyncio.wait_for(switch.start(), timeout=self.connect_timeout)
            for switch in switches
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_switches = []
        for ii, result in enumerate(results):
            switch_name = switches[ii].name
            if isinstance(result, Exception):
                self.log.error(
                    f"Unexpected exception of type {type(result)} while initialising "
                    f"switch {switch_name}: {str(result)}"
                )
            else:
                valid_switches.append(switches[ii])

        self.parser_args[0] = {switch.name: switch for switch in valid_switches}

        all_names = [
            outlet.name.lower()
            for switch in valid_switches
            for outlet in switch.outlets
        ]

        if len(all_names) != len(list(set(all_names))):
            self.log.warning("Repeated outlet names. This may lead to errors.")

        self.log.debug("Start done")

    async def stop(self):
        """Stop the actor and disconnect the power switches."""

        for switch in self.parser_args[0].values():
            try:
                self.log.debug(f"Stop {switch.name} ...")
                await asyncio.wait_for(switch.stop(), timeout=self.connect_timeout)
            except Exception as ex:
                self.log.error(f"Unexpected exception of {type(ex)}: {ex}")

        return await super().stop()

    @classmethod
    def from_config(cls, config, *args, **kwargs):
        """Creates an actor from a configuration file."""

        if config is None:
            if cls.BASE_CONFIG is None:
                raise RuntimeError("The class does not have a base configuration.")
            config = cls.BASE_CONFIG

        instance = super(NPSActor, cls).from_config(config, *args, **kwargs)

        assert isinstance(instance, NPSActor)
        assert isinstance(instance.config, dict)

        switches = {}

        if "switches" in instance.config:
            for (key, swconfig) in instance.config["switches"].items():
                if "name" in swconfig:
                    name = swconfig["name"]
                else:
                    name = key

                instance.log.info(f"Instance {name}: {swconfig}")
                try:
                    switches[name] = powerSwitchFactory(name, swconfig, instance.log)
                except Exception as ex:
                    instance.log.error(f"Power switch factory error {type(ex)}: {ex}")

        instance.parser_args = [switches]

        return instance


NPSCommand = Command[NPSActor]

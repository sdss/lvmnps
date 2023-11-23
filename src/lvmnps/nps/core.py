#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: core.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import abc
import asyncio

from typing import Any, Sequence

from pydantic import BaseModel, ConfigDict, Field

from lvmnps import log
from lvmnps.tools import get_outlet_by_id, get_outlet_by_name, normalise_outlet_name


__all__ = ["NPSClient", "OutletModel", "OutletArgType"]


class OutletModel(BaseModel):
    """A model for an outlet status."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: int
    name: str
    normalised_name: str = ""
    state: bool = False

    client: NPSClient | None = Field(None, repr=False, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.normalised_name = normalise_outlet_name(self.name)
        return super().model_post_init(__context)

    def set_client(self, nps: NPSClient):
        """Sets the NPS client."""

        self.client = nps

    async def on(self):
        """Sets the state of the outlet to "on"."""

        if not self.client:
            raise RuntimeError("NPS client not set.")

        await self.client.set_state(self, on=True)

    async def off(self):
        """Sets the state of the outlet to "off"."""

        if not self.client:
            raise RuntimeError("NPS client not set.")

        await self.client.set_state(self, on=False)


OutletArgType = OutletModel | int | str | Sequence[str | int | OutletModel]


class NPSClient(abc.ABC):
    """Base NPS client."""

    nps_type: str

    def __init__(self):
        self.outlets: dict[str, OutletModel] = {}

        # Time after switching an outlet on during which switching outlets on is
        # delayed to prevent simultaneous inrush currents on power-on time.
        self.delay: float = 1

    async def setup(self):
        """Sets up the power supply, setting any required configuration options."""

        pass

    async def stop(self):
        """Performs any necessary operations to gracefully disconnect from the NPS."""

        pass

    @abc.abstractmethod
    async def verify(self):
        """Checks that the NPS is connected and responding."""

        pass

    @abc.abstractmethod
    async def refresh(self):
        """Refreshes the list of outlets."""

        pass

    async def set_state(self, outlets: OutletArgType, on: bool = False):
        """Sets the state of an outlet or list of outlets.

        Parameters
        ----------
        outlets
            An outlet or list of outlets whose state will be set. An outlet
            can be specified by its name, number, or model instance. If a list
            of outlet is provided the behaviour will depend on the client
            implementation. Outlets may be switched concurrently or sequentially,
            with a delay to avoid in-rush currents.
        on
            Whether to turn the outlet on (if ``True``) or off.

        """

        _outlets: list[OutletModel] = []

        if isinstance(outlets, str) or not isinstance(outlets, Sequence):
            outlets = [outlets]

        for outlet in outlets:
            if isinstance(outlet, str):
                _outlets.append(get_outlet_by_name(self.outlets, outlet))
            elif isinstance(outlet, int):
                _outlets.append(get_outlet_by_id(self.outlets, outlet))
            else:
                _outlets.append(outlet)

        names = [outlet.name for outlet in _outlets]
        log.debug(f"Setting outlets {names} to state on={on}.")
        await self._set_state_internal(_outlets, on=on)

        await self.refresh()

    @abc.abstractmethod
    async def _set_state_internal(self, outlets: list[OutletModel], on: bool = False):
        """Internal method for setting the outlet state.

        This method is intended to be overridden by each specific implementation.
        All implementations should handle switching single outlets or multiple ones,
        and do it in a way that is safe and efficient given the hardware specifications.

        """

    async def cycle(self, outlets: OutletArgType, delay: float = 3):
        """Turns off the selected outlets and turns them on again after a delay.

        Parameters
        ----------
        outlets
            An outlet or list of outlets whose state will be set. An outlet
            can be specified by its name, number, or model instance.
        delay
            Number of seconds the code will wait before turning on the
            outlets again.

        """

        await self.set_state(outlets, on=False)
        await asyncio.sleep(delay)
        await self.set_state(outlets, on=True)
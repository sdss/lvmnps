#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: conftest.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pytest

from lvmnps.nps.core import NPSClient, OutletModel


class NPSTestClient(NPSClient):
    """Test NPS client."""

    nps_type = "test"

    async def setup(self):
        await self.refresh()

    async def refresh(self):
        if "test_1" in self.outlets:
            return

        self.outlets = {"test_1": OutletModel(id=1, name="test_1", state=False)}
        self.outlets["test_1"].set_client(self)

    async def verify(self):
        pass

    async def _set_state_internal(self, outlets: list[OutletModel], on: bool = False):
        for outlet in outlets:
            outlet.state = on


@pytest.fixture
async def nps_test_client():
    _client = NPSTestClient()
    await _client.setup()

    yield _client

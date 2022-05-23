#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import pytest

from lvmnps.actor.actor import NPSActor


@pytest.mark.xfail
async def test_status(actor: NPSActor):

    command = await actor.invoke_mock_command("status DLI-01")
    await command
    assert command.status.did_succeed
    assert command.replies[-1].message["status"] == {}

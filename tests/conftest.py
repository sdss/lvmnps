#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import os

import pytest

import clu.testing
from sdsstools import read_yaml_file
from sdsstools.logger import get_logger

from lvmnps.actor.actor import NPSActor
from lvmnps.switch.factory import powerSwitchFactory


@pytest.fixture()
def test_config():
    yield read_yaml_file(os.path.join(os.path.dirname(__file__), "test_switch.yml"))


@pytest.fixture
def switches(test_config):
    assert "switches" in test_config

    switches = []
    for name, conf in test_config["switches"].items():
        try:
            switches.append(powerSwitchFactory(name, conf, get_logger("test")))
        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


@pytest.fixture()
async def actor(switches, test_config: dict):
    _actor = NPSActor.from_config(test_config)
    _actor = await clu.testing.setup_test_actor(_actor)  # type: ignore

    _actor.parser_args = [{switch.name: switch for switch in switches}]
    await _actor.start()

    yield _actor

    _actor.mock_replies.clear()
    await _actor.stop()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import os

import pytest

import clu.testing
from clu import AMQPActor
from sdsstools import merge_config, read_yaml_file
from sdsstools.logger import get_logger

from lvmnps import config
from lvmnps.actor.actor import lvmnps as NpsActor
from lvmnps.switch.factory import powerSwitchFactory


@pytest.fixture()
def test_config():

    extra = read_yaml_file(os.path.join(os.path.dirname(__file__), "test_switch.yml"))
    yield merge_config(extra, config)


@pytest.fixture
def switches():

    default_config_file = os.path.join(os.path.dirname(__file__), "test_switch.yml")
    default_config = AMQPActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, conf) in default_config["switches"].items():
        try:
            switches.append(powerSwitchFactory(name, conf, get_logger("test")))
        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


# now working to define the fixture for the dli power class...
@pytest.fixture
def dli_switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "test_dli_switch.yml")
    default_config = AMQPActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, conf) in default_config["switches"].items():
        try:
            switches.append(powerSwitchFactory(name, conf, get_logger("test")))
        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


@pytest.fixture()
async def actor(switches, test_config: dict, mocker):

    _actor = NpsActor.from_config(test_config)
    _actor = await clu.testing.setup_test_actor(_actor)  # type: ignore

    _actor.parser_args = [switches]
    await _actor.start()

    yield _actor

    _actor.mock_replies.clear()
    await _actor.stop()

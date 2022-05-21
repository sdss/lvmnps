# encoding: utf-8
#
# conftest.py

"""
Here you can add fixtures that will be used for all the tests in this
directory. You can also add conftest.py files in underlying subdirectories.
Those conftest.py will only be applies to the tests in that subdirectory and
underlying directories. See https://docs.pytest.org/en/2.7.3/plugins.html for
more information.
"""

import os

import pytest

import clu.testing
from clu import AMQPActor
from clu.actor import AMQPBaseActor
from sdsstools import merge_config, read_yaml_file
from sdsstools.logger import get_logger

from lvmnps import config
from lvmnps.actor.actor import lvmnps as NpsActor
from lvmnps.switch.factory import powerSwitchFactory


@pytest.fixture()
def test_config():

    extra = read_yaml_file(
        os.path.join(os.path.dirname(__file__), "test_01_switch.yml")
    )
    yield merge_config(extra, config)


@pytest.fixture
def switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "test_01_switch.yml")
    default_config = AMQPActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, conf) in default_config["switches"].items():
        print(f"Switch {name}: {conf}")
        try:
            switches.append(powerSwitchFactory(name, conf, get_logger("test")))

        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


# now working to define the fixture for the dli power class...
@pytest.fixture
def dli_switches():
    default_config_file = os.path.join(
        os.path.dirname(__file__), "test_02_dli_switch.yml"
    )
    default_config = AMQPActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, conf) in default_config["switches"].items():
        print(f"Switch {name}: {conf}")
        try:
            switches.append(powerSwitchFactory(name, conf, get_logger("test")))

        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches


@pytest.fixture()
async def actor(switches, test_config: dict, mocker):

    # We need to call the actor .start() method to force it to create the
    # controllers and to start the tasks, but we don't want to run .start()
    # on the actor.
    mocker.patch.object(AMQPBaseActor, "start")

    _actor = NpsActor.from_config(test_config)

    _actor.parser_args = [switches]
    await _actor.start()

    _actor = await clu.testing.setup_test_actor(_actor)  # type: ignore

    yield _actor

    _actor.mock_replies.clear()
    await _actor.stop()

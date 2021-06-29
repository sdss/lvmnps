import asyncio
import logging
import sys
import os

import pytest

import click

from sdsstools import get_logger, read_yaml_file
from sdsstools.logger import SDSSLogger, get_logger

from clu.parsers import command_parser
from clu.testing import setup_test_actor, LegacyActor
from clu.model import Model
from clu import AMQPActor

#import lvmnps.actor
from lvmnps.switch.factory import powerSwitchFactory

from lvmnps.actor.commands import parser as nps_command_parser


@pytest.fixture
def switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "lvmnps.yml")
    default_config = LegacyActor._parse_config(default_config_file)

    assert("switches" in default_config)

    switches = []
    for (name, config) in default_config["switches"].items():
        print(f"Switch {name}: {config}")
        try:
            switches.append(powerSwitchFactory(name, config, get_logger("test")))

        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")
   
    return switches


@pytest.mark.asyncio
async def test_actor(switches):

    test_actor = await setup_test_actor(LegacyActor('my_actor',
                                                    host='localhost',
                                                    port=9999))

    

    test_actor.parser = nps_command_parser
    test_actor.parser_args = [switches]  

    
    # The following is not needed, start() is replaced with a MagicMock()
    await test_actor.start()

    # Invoke command and wait until it finishes
    command = test_actor.invoke_mock_command('status')
    await command

    # Make sure the command finished successfully
    assert command.status.is_done

    # Get the last reply and check its "text" keyword
    last_reply = test_actor.mock_replies[-1]
    
    print(last_reply)




import pytest

import click
from clu.parsers import command_parser
from clu.testing import setup_test_actor, LegacyActor


#import lvmnps.actor

@command_parser.command()
@click.argument('NAME', type=str)
async def greeter(command, name):
    command.finish(text=f'Hi {name}!')


@pytest.mark.asyncio
async def test_actor():

    test_actor = await setup_test_actor(LegacyActor('my_actor',
                                              host='localhost',
                                              port=9999))

    # The following is not needed, start() is replaced with a MagicMock()
    await test_actor.start()

    # Invoke command and wait until it finishes
    command = test_actor.invoke_mock_command('greeter John')
    await command

    # Make sure the command finished successfully
    assert command.status.is_done

    # Get the last reply and check its "text" keyword
    last_reply = test_actor.mock_replies[-1]
    assert last_reply.flag == ':'
    assert last_reply['text'] == '"Hi John!"'



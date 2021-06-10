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

import asyncio
import pytest

from clu import AMQPActor
from lvmnps.actor.actor import lvmnps

@pytest.fixture
async def test_lvmnps(AMQPActor):

    actor = AMQPActor(name="amqp_actor", schema=DATA_DIR / "schema.json", port=port)
    await actor.start()

    yield actor

    await actor.stop()

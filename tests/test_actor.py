# encoding: utf-8
#
# main.py

import pytest
from clu import AMQPActor
from lvmnps.actor.actor import lvmnps

pytestmark = [pytest.mark.asyncio]

@pytest.mark.asyncio
async def test_lvmnps():
    assert lvmnps.start() == super.start()
    yield lvmnps
    assert lvmnps.stop() == super.stop()
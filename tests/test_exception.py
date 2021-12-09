import pytest

from lvmnps.actor.actor import lvmnps as NpsActor


pytestmark = [pytest.mark.asyncio]


async def test_command_error_on(actor: NpsActor):
    assert actor

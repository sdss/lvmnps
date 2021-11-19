import pytest


# from lvmnps.actor.actor import lvmnps as NpsActor


pytestmark = [pytest.mark.asyncio]

@pytest.fixture(scope='session')
async def test_actor():

    _actor = setup_test_actor(LegacyActor('my_actor', host='localhost', port=9999))

    yield _actor

    # Clear replies
    _actor.mock_replies.clear()
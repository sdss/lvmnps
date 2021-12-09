import pytest

from lvmnps.actor.actor import lvmnps as NpsActor


@pytest.mark.asyncio
async def test_actor(actor: NpsActor):

    assert actor


@pytest.mark.asyncio
async def test_ping(actor: NpsActor):

    command = await actor.invoke_mock_command("ping")
    await command

    assert command.status.did_succeed
    assert len(command.replies) == 2
    assert command.replies[1].message["text"] == "Pong."


@pytest.mark.asyncio
async def test_actor_no_config():

    with pytest.raises(RuntimeError):
        NpsActor.from_config(None)

import pytest


# from lvmnps.actor.actor import lvmnps as NpsActor


pytestmark = [pytest.mark.asyncio]

"""
async def test_status(actor: NpsActor):

    command = await actor.invoke_mock_command("status")
    await command

    assert command.status.did_succeed

    print(f"reply is {command.replies}")
    print(f"reply 0 is {command.replies[0].message}")
    print(f"reply 1 is {command.replies[1].message}")
    print(f"reply 2 is {command.replies[2].message}")
    print(f"reply 3 is {command.replies[3].message}")

    assert len(command.replies) == 4

    # assert command.replies[1].message["text"] == "Pong."
"""

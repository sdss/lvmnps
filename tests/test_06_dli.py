# working on this at 20211209 CK
import pytest

from lvmnps.actor.actor import lvmnps as NpsActor


@pytest.mark.asyncio
async def test_status(dli_switches, actor: NpsActor):

    assert actor

    command = await actor.invoke_mock_command("status DLI-01")
    await command
    assert command.status.did_succeed
    assert command.replies[-2].message['status'] == -1
    # errors on here . . .

    assert dli_switches
    assert dli_switches[0].name == "DLI-01"
    assert dli_switches[0].outlets[0].name == "Outlet 1"
    assert dli_switches[0].outlets[0].state == -1
    dli_switches[0].outlets[0].state == 0
    assert dli_switches[0].outlets[0].state == 0
    
    

    
    
    
    # status = await dli_switches[0].statusAsDict()
    
    # assert dli_switches[0].dli.userid == 'admin'
    # assert dli_switches[0].dli.password == 'admin'
    
    # dli_switches[0].dli.add_client()
    # assert dli_switches[0].reachable == False
    # outlets = dli_switches[0].outlets
    
    # dli_switches[0].isReachable()
    
    
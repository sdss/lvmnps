

import asyncio

import pytest


#@pytest.fixture(scope="session")
#def event_loop():
    #loop = asyncio.get_event_loop_policy().new_event_loop()
    #yield loop
    #loop.close()


#@pytest.fixture(scope="session", autouse=True)
#async def test_data(event_loop):
    #await asyncio.open_connection(
        #host="127.0.0.1",
        #port=3306,
        #loop=event_loop
    #)


#@pytest.mark.asyncio
#async def test_something():
    #assert True

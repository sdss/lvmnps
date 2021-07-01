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

# import os
# import shutil

import pytest
from clu import AMQPActor, AMQPClient
# from pytest_rabbitmq import factories


# rabbitmq_local_proc = shutil.which('rabbitmq-server', path="/usr/local/sbin:/usr/sbin")
# rabbitmq_local_plugindir = '/usr/lib64/rabbitmq/lib/rabbitmq_server-3.8.11/plugins/'
# rabbitmq_proc = factories.rabbitmq_proc(host='127.0.0.1',
#                                        port=None,
#                                         node="test",
#                                         logsdir='/tmp/rabbitmq/logs',
#                                         plugindir=rabbitmq_local_plugindir,
#                                         server=rabbitmq_local_proc,
#                                         ctl=f"{os.path.dirname(rabbitmq_local_proc)}/rabbitmqctl")


@pytest.fixture
async def amqp_actor(rabbitmq, event_loop):

    port = rabbitmq.args["port"]

    actor = AMQPActor(name="amqp_actor", port=port)
    await actor.start()

    yield actor

    await actor.stop()


@pytest.fixture
async def amqp_client(rabbitmq, amqp_actor, event_loop):

    port = rabbitmq.args["port"]

    client = AMQPClient(name="amqp_client", models=["amqp_actor"], port=port)
    await client.start()

    yield client

    await client.stop()

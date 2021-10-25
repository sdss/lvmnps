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

import os
# import shutil

import clu.testing

import pytest
from clu import AMQPActor, AMQPClient
from lvmnps import config
from lvmnps.actor.actor import lvmnps as NpsActor
from sdsstools import merge_config, read_yaml_file

from clu.actor import AMQPBaseActor

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


@pytest.fixture()
def test_config():

    extra = read_yaml_file(os.path.join(os.path.dirname(__file__), "test_01_switch.yml"))
    yield merge_config(extra, config)


@pytest.fixture
def switches():
    default_config_file = os.path.join(os.path.dirname(__file__), "test_01_switch.yml")
    default_config = AMQPActor._parse_config(default_config_file)

    assert "switches" in default_config

    switches = []
    for (name, config) in default_config["switches"].items():
        print(f"Switch {name}: {config}")
        try:
            switches.append(powerSwitchFactory(name, config, get_logger("test")))

        except Exception as ex:
            print(f"Error in power switch factory {type(ex)}: {ex}")

    return switches

@pytest.fixture()
async def actor(test_config: dict, switches, mocker):

    # We need to call the actor .start() method to force it to create the
    # controllers and to start the tasks, but we don't want to run .start()
    # on the actor.
    mocker.patch.object(AMQPBaseActor, "start")

    #test_config["controllers"]["sp1"]["host"] = controller.host
    #test_config["controllers"]["sp1"]["port"] = controller.port

    _actor = NpsActor.from_config(test_config)
    await _actor.start()

    _actor = await clu.testing.setup_test_actor(_actor)  # type: ignore

    yield _actor

    _actor.mock_replies.clear()
    await _actor.stop()
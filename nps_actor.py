import asyncio
import dlipower
import click
from clu import AMQPActor, command_parser

switch = dlipower.PowerSwitch(hostname="10.7.45.22",userid="admin",password='rLXR3KxUqiCPGvA')

@command_parser.command()
async def status(command):
    """print the status of the NPC."""

    command.info(text="Status of NPC", status = {
        "outlet 1":switch[0].name,
        "state 1":switch[0].state,
        "outlet 2":switch[1].name,
        "state 2":switch[1].state,
        "outlet 3":switch[2].name,
        "state 3":switch[2].state,
        "outlet 4":switch[3].name,
        "state 4":switch[3].state,
        "outlet 5":switch[4].name,
        "state 5":switch[4].state,
        "outlet 6":switch[5].name,
        "state 6":switch[5].state,
        "outlet 7":switch[6].name,
        "state 7":switch[6].state,
        "outlet 8":switch[7].name,
        "state 8":switch[7].state,
        })
    # Here we would implement the actual communication
    return

@command_parser.command()
@click.argument("OUTLET", type=float)
async def on(command, outlet):
    """Turn on the Outlet"""

    command.info(text="Turn on the outlet %d" % (outlet))

    switch.on(outlet)

    return command.finish(text="Turn on the outlet %d done!" % (outlet))

@command_parser.command()
@click.argument("OUTLET", type=float)
async def off(command, outlet):
    """Turn off the Outlet"""

    command.info(text="Turn off the outlet %d" % (outlet))

    switch.off(outlet)

    return command.finish(text="Turn off the outlet %d done!" % (outlet))

@command_parser.command()
async def onall(command):
    """Turn on all Outlet"""

    command.info(text="Turn on all of the outlet")

    for outlet in switch:
        outlet.on()
    return command.finish(text="Turn on all of the outlet done!")

@command_parser.command()
async def offall(command):
    """Turn off all Outlet"""

    command.info(text="Turn off all of the outlet")

    for outlet in switch:
        outlet.off()
    return command.finish(text="Turn off all of the outlet done!")

class NPCActor(AMQPActor):
    def __init__(self):
        super().__init__(
            name="npc_actor",
            user="guest",
            password="guest",
            host="localhost",
            port=5672,
            version="0.1.0",
        )


async def run_actor():
    actor = await NPCActor().start()
    await actor.run_forever()


asyncio.run(run_actor())


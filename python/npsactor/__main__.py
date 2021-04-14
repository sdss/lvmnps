import os
import asyncio
import click
from click_default_group import DefaultGroup
from clu.tools import cli_coro

from sdsstools.daemonizer import DaemonGroup

from npsactor.actor.actor import NpsActor as NpsActorInstance


@click.group(cls=DefaultGroup, default="actor", default_if_no_args=True)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the user configuration file.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.pass_context
def NpsActor(ctx, config_file, verbose):
    """Nps controller"""

    ctx.obj = {"verbose": verbose, "config_file": config_file}


@NpsActor.group(cls=DaemonGroup, prog="nps_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""
   # default_config_file = os.path.join(os.path.dirname(__file__), "etc/NpsActor.yml")
    #config_file = ctx.obj["config_file"] or default_config_file

    #npsactor_obj = NpsActor.from_config(config_file)
    npsactor_obj = NpsActorInstance()

    if ctx.obj["verbose"]:
        npsactor_obj.log.fh.setLevel(0)
        npsactor_obj.log.sh.setLevel(0)

    await npsactor_obj.start()
    await npsactor_obj.run_forever()

if __name__ == "__main__":
    NpsActor()


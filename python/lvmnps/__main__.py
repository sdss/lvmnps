import os

import click
from click_default_group import DefaultGroup

from clu.tools import cli_coro
from sdsstools.daemonizer import DaemonGroup

from lvmnps.actor.actor import NPSActor


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
def lvmnps(ctx, config_file, verbose):
    """Nps Actor."""

    ctx.obj = {"verbose": verbose, "config_file": config_file}


@lvmnps.group(cls=DaemonGroup, prog="nps_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""

    default_config_file = os.path.join(os.path.dirname(__file__), "etc/lvmnps.yml")
    config_file = ctx.obj["config_file"] or default_config_file

    lvmnps = NPSActor.from_config(config_file)

    if ctx.obj["verbose"]:
        if lvmnps.log.fh:
            lvmnps.log.fh.setLevel(0)
        lvmnps.log.sh.setLevel(0)

    await lvmnps.start()
    await lvmnps.run_forever()


if __name__ == "__main__":
    lvmnps()

import asyncio
import functools
import logging
import os

import click
from click_default_group import DefaultGroup

from sdsstools.daemonizer import DaemonGroup

from lvmnps.actor.actor import NPSActor


def cli_coro(f):
    """Decorator function that allows defining coroutines with click."""

    if hasattr(asyncio, "coroutine"):
        f = getattr(asyncio, "coroutine")(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return functools.update_wrapper(wrapper, f)


@click.group(cls=DefaultGroup, default="actor", default_if_no_args=True)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to the user configuration file.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Debug mode.",
)
@click.pass_context
def lvmnps(ctx: click.Context, config_file: str, verbose: bool = False):
    """Network Power Supply actor."""

    ctx.obj = {"verbose": verbose, "config_file": config_file}


@lvmnps.group(cls=DaemonGroup, prog="nps_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""

    config_file = ctx.obj["config_file"]

    lvmnps = NPSActor.from_config(config_file, verbose=ctx.obj["verbose"])

    if lvmnps.log.fh:
        lvmnps.log.fh.setLevel(logging.NOTSET)

    if ctx.obj["verbose"]:
        lvmnps.log.sh.setLevel(logging.NOTSET)
    else:
        lvmnps.log.sh.setLevel(logging.INFO)

    await lvmnps.start()
    await lvmnps.run_forever()


def main():
    lvmnps(auto_envvar_prefix="LVMNPS")


if __name__ == "__main__":
    main()

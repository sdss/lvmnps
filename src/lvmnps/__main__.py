import asyncio
import functools
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
    help="Path to the user configuration file.",
)
@click.option(
    "-r",
    "--rmq_url",
    "rmq_url",
    default=None,
    type=str,
    help="rabbitmq url, eg: amqp://guest:guest@localhost:5672/",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.option(
    "-s",
    "--simulate",
    count=True,
    help="Simulation mode. Overwrite configured nps device with a dummy device",
)
@click.pass_context
def lvmnps(ctx, config_file, rmq_url, verbose, simulate):
    """Nps Actor."""

    ctx.obj = {
        "verbose": verbose,
        "config_file": config_file,
        "rmq_url": rmq_url,
        "simulate": simulate,
    }


@lvmnps.group(cls=DaemonGroup, prog="nps_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""

    default_config_file = os.path.join(os.path.dirname(__file__), "etc/lvmnps.yml")
    config_file = ctx.obj["config_file"] or default_config_file

    lvmnps = NPSActor.from_config(
        config_file,
        url=ctx.obj["rmq_url"],
        verbose=ctx.obj["verbose"],
        simulate=ctx.obj["simulate"],
    )

    if ctx.obj["verbose"]:
        if lvmnps.log.fh:
            lvmnps.log.fh.setLevel(0)
        lvmnps.log.sh.setLevel(0)

    await lvmnps.start()
    await lvmnps.run_forever()


def main():
    lvmnps(auto_envvar_prefix="LVMNPS")


if __name__ == "__main__":
    main()

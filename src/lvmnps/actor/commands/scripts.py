#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: scripts.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING

import click

from . import lvmnps_command_parser


if TYPE_CHECKING:
    from src.lvmnps.actor.actor import NPSCommand


__all__ = ["scripts"]


def validate_nps(command: NPSCommand):
    """Checks that the NPS implements scripting."""

    nps = command.actor.nps

    if nps.implementations.get("scripting", False) is False:
        command.fail("Scripting not allowed for this NPS.")
        return False

    return True


@lvmnps_command_parser.group()
def scripts():
    """Handles user scripts."""

    pass


@scripts.command()
@click.argument("SCRIPT", type=str, nargs=-1)
async def run(command: NPSCommand, script: tuple[str, ...]):
    """Runs a user script.

    The first argument is expected to be the name of the script. Additional
    argument will be considered arguments to pass to the script function.

    """

    if not validate_nps(command):
        return

    if len(script) == 0:
        return command.fail("Not enough parameters.")

    nps = command.actor.nps

    script_name = script[0]
    script_args = script[1:]

    try:
        thread_id = await nps.run_script(script_name, *script_args)
    except Exception as err:
        return command.fail(f"Failed executing script {script_name!r}: {err}")

    return command.finish(
        script={
            "name": script_name,
            "args": list(script_args),
            "running": True,
            "thread_id": thread_id,
        }
    )


@scripts.command()
@click.argument("THREAD", type=int, required=False)
async def stop(command: NPSCommand, thread: int | None):
    """Runs a user script.

    If the thread number is not provided, stops all running scripts.

    """

    if not validate_nps(command):
        return

    nps = command.actor.nps

    try:
        await nps.stop_script(thread_num=thread)
    except Exception:
        return command.fail("Failed stopping scripts.")

    return command.finish()


@scripts.command(name="list")
async def list_scripts(command: NPSCommand):
    """Lists running scripts."""

    if not validate_nps(command):
        return

    nps = command.actor.nps

    threads = await nps.list_running_scripts()

    scripts = [
        {"name": threads[id_], "args": [], "running": True, "thread_id": id_}
        for id_ in threads
    ]

    return command.finish(scripts=scripts)

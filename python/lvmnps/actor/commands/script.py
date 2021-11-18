# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-08-12
# @Filename: status.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import click
from clu.command import Command

from lvmnps.actor.commands import parser
from lvmnps.exceptions import NpsActorError
from lvmnps.switch.powerswitchbase import PowerSwitchBase as PowerSwitch


@parser.command()
@click.argument("SWITCHNAME", type=str, required=False)
async def script(command: Command, switches: PowerSwitch, switchname: str):
    """Returns the dictionary of a specific outlet."""

    if switchname is None:
        command.info(text="Printing the current status of all outlets")
    elif switchname:
        command.info(text=f"Printing the current status of switch {switchname}")

    try:
        if switchname is None:
            for switch in switches:
                result = await switch.scripting()
                print(result)
        elif switchname:
            for switch in switches:
                # status |= await switch.statusAsDict(name, portnum) works only with python 3.9
                if switchname == switch.name:
                    result = await switch.scripting()
                    print(result)
                    break

    except NpsActorError as ex:
        return command.fail(error=str(ex))

    return command.finish()

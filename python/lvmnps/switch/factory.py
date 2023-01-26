# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-22
# @Update: 2021-10-09
# @Filename: lvmnps/switch/factory.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from sdsstools.logger import SDSSLogger

from lvmnps.exceptions import PowerException

from .dli.powerswitch import DLIPowerSwitch
from .dummy.powerswitch import PowerSwitch as DummyPowerSwitch
from .iboot.powerswitch import PowerSwitch as IBootPowerSwitch
from .netio.powerswitch import PowerSwitch as NetIOPowerSwitch


if TYPE_CHECKING:
    from lvmnps.switch.powerswitchbase import PowerSwitchBase


# from .iboot.powerswitch import PowerSwitch as IBootPowerSwitch


def powerSwitchFactory(
    name: str, config: dict, log: SDSSLogger, simulate: bool = False
):
    """Power switch factory method which helps the user to select the `.PowerSwitch`
    class based on the configuration file that is selected.

    Parameters
    ----------
    name
        the name of the Dli Controller
    config
        The configuration dictionary from the configuration file .yml
    log
        The logger for logging
    simulate
        on True overwrite type from config with dummy

    """

    def throwError(n, c):
        """The method to throw the Exception."""
        raise PowerException(f"Power switch {n} with type {c['type']} not defined")

    factorymap: dict[str, Type[PowerSwitchBase]] = {
        "dli": DLIPowerSwitch,
        "netio": NetIOPowerSwitch,
        "iboot": IBootPowerSwitch,
        "dummy": DummyPowerSwitch,
    }

    log.info(f"{simulate:-}")
    return factorymap.get(
        config["type"] if not simulate else "dummy", lambda n, c, _: throwError(n, c)
    )(name, config, log)

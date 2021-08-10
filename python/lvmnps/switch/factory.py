# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-22
# @Filename: lvmnps/switch/__init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools.logger import SDSSLogger

from .dli.powerswitch import PowerSwitch as DliPowerSwitch
from .dummy.powerswitch import PowerSwitch as DummyPowerSwitch
from .exceptions import PowerException
from .iboot.powerswitch import PowerSwitch as IBootPowerSwitch


def powerSwitchFactory(name: str, config: dict, log: SDSSLogger):
    def throwError(n, c):
        raise PowerException(f"Power switch {n} with type {c['type']} not defined")

    factorymap = {
        "dli": DliPowerSwitch,
        "iboot": IBootPowerSwitch,
        "dummy": DummyPowerSwitch,
    }

    return factorymap.get(config["type"], lambda n, c: throwError(n, c))(
        name, config, log
    )

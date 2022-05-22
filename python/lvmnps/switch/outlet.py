# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-22
# @Filename: lvmnps/switch/outlet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


class Outlet(object):
    """Outlet class to manage the power switch.

    Parameters
    ----------
    swname
        the name of the switch (from the configuration file)
    name
        The name of the outlet
    portnum
        The number of the port (in the range of 1~8)
    description
        The description about the outlet
    state
        the state of the outlet (on: 1, off:0)

    """

    def __init__(self, swname, name, portnum, description, state):

        self.swname = swname
        self.name = name if name else f"{swname}.port{portnum}"
        self.portnum = portnum
        self.description = description if description else f"{swname} Port {portnum}"
        self.inuse = bool(name) or bool(description)
        self.state = state

    def __str__(self):
        return f"#{self.portnum}:{self.name}={self.state}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def parse(value):
        """Parse the input data for ON/OFF."""

        if value in ["off", "OFF", "0", 0, False]:
            return 0
        if value in ["on", "ON", "1", 1, True]:
            return 1
        return -1

    def setState(self, value):
        """Class method: Set the state of the outlet inside the class."""
        self.state = Outlet.parse(value)

    def isOn(self):
        """Return the state of the outlet."""
        return self.state == 1

    def isOff(self):
        """Return the state of the outlet."""
        return self.state == 0

    def isValid(self):
        """Return the validity of the outlet."""
        return self.state == -1

    def toDict(self):
        """Return the dictionary describing the status of the outlet."""
        return {
            "state": self.state,
            "descr": self.description,
            "switch": self.swname,
            "port": self.portnum,
        }

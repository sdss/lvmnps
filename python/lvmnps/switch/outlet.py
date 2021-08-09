# -*- coding: utf-8 -*-
#
# @Author: Florian Briegel (briegel@mpia.de)
# @Date: 2021-06-22
# @Filename: lvmnps/switch/outlet.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import datetime

class Outlet(object):
    """
    A power outlet class
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
        if value in ['off', 'OFF', '0', 0, False]:
            return 0
        if value in ['on', 'ON', '1', 1, True]:
            return 1
        return -1

    def setState(self, value):
        self.state = Outlet.parse(value)

    def isOn(self):
        return self.state == 1

    def isOff(self):
        return self.state == 0

    def isValid(self):
        return self.state == -1

    def toJson(self):
        return {
            'STATE': self.state,
            'DESCR': self.description,
            'SWITCH': self.swname,
            'PORT': self.portnum,
        }

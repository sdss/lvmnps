# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr), Changgon Kim (changgonkim@khu.ac.kr)
# @Date: 2021-08-24
# @Update: 2021-10-09
# @Filename: lvmnps/switch/dli/dli.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


from __future__ import annotations

import asyncio

import httpx


class Dli(object):
    """Powerswitch class to manage the dli power switch.

    Parameters
    ----------
    log
        The logger for logging
    name
        the name of the Dli Controller
    userid
        The username from the configuration (the id for login)
    password
        The password from the configuration (the password for login)
    hostname
        The hostname from the configuration (the ip address for connection)
    onoff_timeout
        the onoff_timeout seconds for sending the on/off command.
    """

    def __init__(
        self,
        log=None,
        name=None,
        userid=None,
        password=None,
        hostname=None,
        onoff_timeout=3,
    ):
        self.log = log
        if userid:
            self.userid = userid
        if password:
            self.password = password
        if hostname:
            self.hostname = hostname
        if name:
            self.name = name
        if onoff_timeout:
            self.onoff_timeout = onoff_timeout
        self.clients = {}
        self.outlets_dict = {}

    async def add_client(self):
        """Add the httpx AsyncClient on the Dli object."""

        try:
            auth = httpx.DigestAuth(self.userid, self.password)
            self.clients[self.hostname] = httpx.AsyncClient(
                auth=auth,
                base_url=f"http://{self.hostname}/restapi",
                headers={},
            )
        except Exception as ex:
            self.log.error(
                f"{type(ex)}: {ex} couldn't access to clients {self.hostname}"
            )

    async def close(self):
        """Close the Client."""
        try:
            await self.clients[self.hostname].aclose()

        except Exception as ex:
            self.log.error(f"{type(ex)}: {ex} couldn't close the request")

    async def verify(self, outlets):
        """Verifies if we can reach the switch by the "get" method.
        Also compares the outlet lists with the configuration, and returns true if it's identical.

        Parameters
        ----------
        outlets
            list of Outlet objects defined on /switch/outlet.py
            each Oulet object indicates one of eight outlets of the dli power switch.
        """
        result = False
        if self.hostname not in self.clients:
            raise ValueError(f"Client for host {self.hostname} not defined.")

        r = await self.clients[self.hostname].get("relay/outlets/")
        if r.status_code != 200:
            raise RuntimeError(f"GET returned code {r.status_code}.")
        else:
            result = await self.compare(r.json(), outlets)

        return result

    async def compare(self, json, outlets):
        """Compares the name of outlets from the json object and the
        name of the Outlet object list.
        The name of the Outlet object is from the configuration file in /etc/lvmnps_dli.yml

        Parameters
        ----------
        json
            The json list from the restful API.
            The current status of the power switch is contained here.
        outlets
            list of Outlet objects defined on /switch/outlet.py
            each Oulet object indicates one of eight outlets of the dli power switch.
        """
        same = True
        assert len(outlets) == len(json)

        for i in range(len(outlets)):
            if json[i]["name"] != "":
                print(json[i]["name"])
                print(outlets[i].name)
                if json[i]["name"] != outlets[i].name:
                    same = False
                    break

        return same

    async def on(self, outlet=0):
        """Turn on the power of the outlet.
        Set the value of the outlet state by "put" method.
        The outlet value is integer, but the outlet number is
        1, 2, 3, 4, 5, 6, 7 ,8
        So we have to put
        0, 1, 2, 3, 4, 5, 6, 7
        to indicate the outlet inside the python list.

        Parameters
        ----------
        outlet
            (int) The number indicating the outlet.
            The input will be 1, 2, 3, 4, 5, 6, 7, 8.
        """

        if self.hostname not in self.clients:
            raise ValueError(f"Client for host {self.hostname} not defined.")

        outlet = outlet - 1

        r = await asyncio.wait_for(
            self.clients[self.hostname].put(
                f"relay/outlets/{outlet}/state/",
                data={"value": True},
                headers={"X-CSRF": "x"},
            ),
            self.onoff_timeout,
        )
        if r.status_code != 204:
            raise RuntimeError(f"PUT returned code {r.status_code}.")

    async def off(self, outlet=0):
        """Turn off the power of the outlet.
        Set the value of the outlet state by "put" method.
        The outlet value is integer, but the outlet number is
        1, 2, 3, 4, 5, 6, 7 ,8
        So we have to put
        0, 1, 2, 3, 4, 5, 6, 7
        to indicate the outlet inside the python list.

        Parameters
        ----------
        outlet
            (int) The number indicating the outlet.
            The input will be 1, 2, 3, 4, 5, 6, 7, 8.
        """

        if self.hostname not in self.clients:
            raise ValueError(f"Client for host {self.hostname} not defined.")

        outlet = outlet - 1

        r = await asyncio.wait_for(
            self.clients[self.hostname].put(
                f"relay/outlets/{outlet}/state/",
                data={"value": False},
                headers={"X-CSRF": "x"},
            ),
            self.onoff_timeout,
        )
        if r.status_code != 204:
            raise RuntimeError(f"PUT returned code {r.status_code}.")

    async def statusdictionary(self):
        """Sets the status as a dictionary memeber of the class from the outlets of the real switch.
        Receives the data from the switch by the 'get' method as a json.
        """

        if self.hostname not in self.clients:
            raise ValueError(f"Client for host {self.hostname} not defined.")

        r = await self.clients[self.hostname].get("relay/outlets/")
        if r.status_code != 200:
            raise RuntimeError(f"GET returned code {r.status_code}.")

        data = r.json()
        num = range(0, 8)
        for n in num:
            outlet_num = n + 1
            self.outlets_dict[outlet_num] = data[n]["state"]
        return

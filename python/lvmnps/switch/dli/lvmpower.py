# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2021-08-12


from __future__ import annotations

import httpx
from bs4 import BeautifulSoup


CONFIG_DEFAULTS = {
    "userid": "admin",
    "password": "1234",
    "hostname": "192.168.0.100",
    "port": "80",
    "name": "switch"
}

class PowerSwitch(object):
    def __init__(
        self,
        userid=None,
        password=None,
        hostname=None,
        name=None,
        port=None,
        use_https=False,
    ):
        """
        Class initialization
        """

        config = self.load_configuration()
        if userid:
            self.userid = userid
        else:
            self.userid = config["userid"]
        if password:
            self.password = password
        else:
            self.password = config["password"]
        if hostname:
            self.hostname = hostname
        else:
            self.hostname = config["hostname"]
        if port:
            self.port = port
        else:
            self.port = config["port"]
        if name:
            self.name = name
        else:
            self.name = config["name"]

        self.scheme = "http"
        self.base_url = "%s://%s" % (self.scheme, self.hostname)
        self.clients = {}

    def load_configuration(self):
        """Return a configuration dictionary"""
        return CONFIG_DEFAULTS

    async def add_client(self):
        """Access the url object"""

        auth = httpx.DigestAuth(self.userid, self.password)
        self.clients[self.hostname] = httpx.AsyncClient(
            auth=auth,
            base_url=self.base_url,
            headers={},
        )

    async def login(self):
        """Access plaintext URL logins"""

        login_url = "%s/login.tgi" % self.base_url
        data = {"Username": self.userid, "Password": self.password}
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0)\
                Gecko/20100101 Firefox/89.0",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            res = await self.clients[self.hostname].post(
                url=login_url,
                data=data,
                headers=headers,
            )
        except httpx.RequestError as exc:
            print(f"An error {exc} occurred while requesting {login_url!r}.")

        if res.status_code != 200:
            raise Exception(
                f"Error response {res.status_code} while requesting {login_url}."
            )

    async def close(self):
        """Close the Connection with URL"""
        await self.clients[self.hostname].aclose()

    async def verify(self):
        """Verify we can reach the switch, returns true if ok"""
        if await self.geturl():
            return True
        return False

    async def geturl(self, url="index.htm"):
        """Get a URL"""

        await self.add_client()
        await self.login()
        full_url = "%s/%s" % (self.base_url, url)

        if self.hostname not in self.clients:
            raise ValueError(f"Client for hostname {self.hostname} not defined.")

        res = await self.clients[self.hostname].get(url=full_url)

        if res.status_code != 200:
            raise RuntimeError(f"GET returned code {res.status_code}.")
        else:
            result = res.content

        await self.close()

        return result

    async def on(self, outlet_number=0):
        """Turn on power to an outlet"""
        await self.geturl(url="outlet?%d=ON" % outlet_number)

    async def onall(self):
        """Turn on all outlets"""
        await self.geturl(url="outlet?%s=ON" % "a")

    async def off(self, outlet_number=0):
        """Turn off power to an outlet"""
        await self.geturl(url="outlet?%d=OFF" % outlet_number)

    async def cycle(self, outlet_number: int):
        """cycle power to an outlet"""
        await self.geturl(url="outlet?%d=CCL" % outlet_number)


    async def statuslist(self):
        """Return the status of all outlets in a list,
        each item will contain 3 items plugnumber, hostname and state"""
        outlets = []
        url = await self.geturl("index.htm")
        if not url:
            return None
        soup = BeautifulSoup(url, "html.parser")
        # Get the root of the table containing the port status info
        try:
            root = soup.findAll("td", text="1")[0].parent.parent.parent
        except IndexError:
            # Finding the root of the table with the outlet info failed
            # try again assuming we're seeing the table for a user
            # account insteaed of the admin account (tables are different)
            try:
                self._is_admin = False
                root = soup.findAll("th", text="#")[0].parent.parent.parent
            except IndexError:
                return None
        for temp in root.findAll("tr"):
            columns = temp.findAll("td")
            if len(columns) == 5:
                plugnumber = columns[0].string
                name = columns[1].string
                state = columns[2].find("font").string.upper()
                outlets.append([int(plugnumber), name, state])

        return outlets

    async def statusdictionary(self):
        """Return the status of all outlets in a dictionary,
        each item will contain 2 items plugnumber, status"""

        outlets = await self.statuslist()
        outlets_dict = {}

        num = range(0, 8)
        for n in num:
            plugnumber = outlets[n][0]
            outlets_dict[plugnumber] = outlets[n][2]

        return outlets_dict

    async def printstatus(self):
        """Print the status off all the outlets as a table to stdout"""
        if not await self.statuslist():
            print("Unable to communicate to the Web power switch at %s" % self.hostname)
            return None
        print("Outlet\t%-15.15s\tState" % "Name")
        for item in await self.statuslist():
            print("%d\t%-15.15s\t%s" % (item[0], item[1], item[2]))
        return

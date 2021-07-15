# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr)
# @Date: 2021-07-05


from __future__ import annotations
import asyncio
import httpx
from bs4 import BeautifulSoup


class LVMPowerSwitch(object):

    def __init__(self, hostname=None, userid=None, password=None, name=None, port=None):
        """
        Class initialization
        """

        self.host = hostname
        self.userid = userid
        self.password = password
        self.port = port
        self.name = name

        self.scheme = 'http'
        self.base_url = '%s://%s' % (self.scheme, self.host)
        self.clients = {}

    async def add_client(self):
        """Access the url object"""
        
        auth = httpx.DigestAuth(self.userid, self.password)
        self.clients[self.host] = httpx.AsyncClient(
            auth=auth,
            base_url=self.base_url,
            headers={},
        )

    async def login(self):
        """Access plaintext URL logins"""

        login_url = '%s/login.tgi' % self.base_url
        data = {
            'Username': self.userid,
            'Password': self.password
            }
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0', 
                'Content-Type': 'application/x-www-form-urlencoded'
                }

        try:
            login = await self.clients[self.host].post(
                url=login_url,
                data=data,
                headers=headers,
                )
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {login_url!r}.")

        if login.status_code != 200:
            raise Exception(f"Error response {login.status_code} while requesting {login_url}.")

    async def close(self):
        """Close the Connection with URL"""
        await self.clients[self.host].aclose()


    async def geturl(self, url='index.htm'):
        """Get a URL"""
        
        await self.login()
        full_url = "%s/%s" % (self.base_url, url)

        if self.host not in self.clients:
            raise ValueError(f"Client for host {self.host} not defined.")
        
        response = await self.clients[self.host].get(url=full_url)
        
        if response.status_code != 200:
            raise RuntimeError(f"GET returned code {response.status_code}.")
        else:
            result = response.content

        #await self.clients[self.host].aclose()

        return result


    async def on(self, name:str='Outlet 0', outlet_number:int=0):
        """Turn on power to an outlet
           False = Success
           True = Fail
        """
        outlets = await self.statuslist()
        len = range(0, 7)

        if outlet_number != 0:
             await self.geturl(url='outlet?%s=ON' % outlet_number)
        else:
            for plug in len:
                if name == outlets[plug][1]:
                    plug_number = outlets[plug][0]
                    await self.geturl(url='outlet?%s=ON' % plug_number)


    async def onall(self):
        """Turn on all outlets"""
        await self.geturl(url='outlet?%s=ON' % 'a')


    async def outlet(self):
        outlet = await self. statuslist()
        print(outlet)


    async def off(self, name:str='Oetlet 0', outlet_number:int=0):
        """Turn on power to an outlet
           False = Success
           True = Fail
        """
        outlets = await self.statuslist()
        len = range(0, 7)

        if outlet_number != 0:
             await self.geturl(url='outlet?%s=OFF' % outlet_number)
        else:
            for plug in len:
                if name == outlets[plug][1]:
                    plug_number = outlets[plug][0]
                    await self.geturl(url='outlet?%s=OFF' % plug_number)


    async def offall(self):
        """Turn off all outlets"""
        await self.geturl(url='outlet?%s=OFF' % 'a')


    async def cycle(self, outlet_number:int):
        """cycle power to an outlet"""

        if outlet_number!=0:
            await self.geturl(url='outlet?%d=CCL' % outlet_number)
        else:
            await self.geturl(url='outlet?%s=CCL' % 'a')


    async def getstatus(self):
        i = 1
        data = {}
        list = await self.statuslist()
        for item in list:
            out_name = "outlet_" + str(i)
            out_state = "state_" + str(i)
            data[out_name] = item[1]
            data[out_state] = item[2]
            i+=1
        return data


    async def statuslist(self):
        """ Return the status of all outlets in a list,
        each item will contain 3 items plugnumber, hostname and state  """
        outlets = []
        url = await self.geturl('index.htm')
        if not url:
            return None
        soup = BeautifulSoup(url, "html.parser")
        # Get the root of the table containing the port status info
        try:
            root = soup.findAll('td', text='1')[0].parent.parent.parent
        except IndexError:
            # Finding the root of the table with the outlet info failed
            # try again assuming we're seeing the table for a user
            # account insteaed of the admin account (tables are different)
            try:
                self._is_admin = False
                root = soup.findAll('th', text='#')[0].parent.parent.parent
            except IndexError:
                return None
        for temp in root.findAll('tr'):
            columns = temp.findAll('td')
            if len(columns) == 5:
                plugnumber = columns[0].string
                name = columns[1].string
                state = columns[2].find('font').string.upper()
                outlets.append([int(plugnumber), name, state])

        return outlets

    async def printstatus(self):
        """ Print the status off all the outlets as a table to stdout """
        if not await self.statuslist():
            print("Unable to communicate to the Web power switch at %s" % self.hostname)
            return None
        print('Outlet\t%-15.15s\tState' % 'Name')
        for item in await self.statuslist():
            print('%d\t%-15.15s\t%s' % (item[0], item[1], item[2]))
        return

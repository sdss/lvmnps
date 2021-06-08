#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-06-07
# @Filename: lvmpower.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import hashlib
import logging
import multiprocessing
import os
import json
import requests
import requests.exceptions
import time
import urllib3
from urllib.parse import quote

from clu.device import Device

from bs4 import BeautifulSoup
import httpx


logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DLIPowerException(Exception):
    """
    An error occurred talking the the DLI Power switch
    """
    pass

class PowerSwitch():
    """ Powerswitch class to manage the Digital Loggers Web power switch """
    __len = 0
    login_timeout = 2.0
    secure_login = False

    def __init__(self, userid=None, password=None, hostname=None, timeout=None,
                 cycletime=None, retries=None, use_https=False, name=None, port=None):
        #Device.__init__(self, hostname, port)
        self.name = name
        """
        Class initializaton
        """
        #config = self.load_configuration()
        self.retries = retries
        self.userid = userid
        self.password = password
        self.hostname = hostname
        self.timeout = float(timeout)
        
        self.scheme = 'http'
        if use_https:
            self.scheme = 'https'
        self.base_url = '%s://%s' % (self.scheme, self.hostname)
        self._is_admin = True
        self.session = requests.Session()
        #self.client = httpx.AsyncClient()
        #self.login()
    
    #functions for 'status' command
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


    async def geturl(self, url='index.htm'):
        """
        Get a URL from the userid/password protected powerswitch page Return None on failure
        """
        full_url = "%s/%s" % (self.base_url, url)
        result = None
        request = None
        logger.debug(f'Requesting url: {full_url}')
        for i in range(0, self.retries):
            try:
                if self.secure_login and self.client:
                    request = await self.client.get(full_url, timeout=self.timeout, verify=False, allow_redirects=True)
                else:
                    request = httpx.get(full_url, auth=(self.userid, self.password,), timeout=self.timeout, verify=False, allow_redirects=True)  # nosec
            except httpx.RequestError as e:
                logger.exception("Caught exception: An error occurred while requesting %s", str(e.request.url))
                continue
            if request.status_code == 200:
                result = request.content
                break

        logger.debug('Response code: %s', request.status_code)
        logger.debug(f'Response content: {result}')
        return result

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
                hostname = columns[1].string
                state = columns[2].find('font').string.upper()
                outlets.append([int(plugnumber), hostname, state])
        if self.__len == 0:
            self.__len = len(outlets)
        return outlets


    #functions for 'on/off' command
    def determine_outlet(self, outlet=None):
        """ Get the correct outlet number from the outlet passed in, this
            allows specifying the outlet by the name and making sure the
            returned outlet is an int
        """
        outlets = self.statuslist()
        if outlet and outlets and isinstance(outlet, str):
            for plug in outlets:
                plug_name = plug[1]
                if plug_name and plug_name.strip() == outlet.strip():
                    return int(plug[0])
        try:
            outlet_int = int(outlet)
            if outlet_int <= 0 or outlet_int > self.__len__():
                raise DLIPowerException('Outlet number %d out of range' % outlet_int)
            return outlet_int
        except ValueError:
            raise DLIPowerException('Outlet name \'%s\' unknown' % outlet)

    def off(self, outlet=0):
        """ Turn off a power to an outlet
            False = Success
            True = Fail
        """
        self.geturl(url='outlet?%d=OFF' % self.determine_outlet(outlet))
        return self.status(outlet) != 'OFF'

    def on(self, outlet=0):
        """ Turn on power to an outlet
            False = Success
            True = Fail
        """
        self.geturl(url='outlet?%d=ON' % self.determine_outlet(outlet))
        return self.status(outlet) != 'ON'

    def status(self, outlet=1):
        """
        Return the status of an outlet, returned value will be one of:
        ON, OFF, Unknown
        """
        outlet = self.determine_outlet(outlet)
        outlets = self.statuslist()
        if outlets and outlet:
            for plug in outlets:
                if plug[0] == outlet:
                    return plug[2]
        return 'Unknown'

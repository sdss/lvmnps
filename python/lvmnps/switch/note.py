import asyncio
import functools
import aiohttp


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

    async def __getitem__(self, index):
        outlets = []
        if isinstance(index, slice):
            status = (await self.statuslist())[index.start:index.stop]
        else:
            status = [(await self.statuslist())[index]]
        for outlet_status in status:
            power_outlet = Outlet(
                switch=self,
                outlet_number=outlet_status[0],
                description=outlet_status[1],
                state=outlet_status[2]
            )
            outlets.append(power_outlet)
        if len(outlets) == 1:
            return outlets[0]
        return outlets


#Asyncio + requests 

    async def geturl(self, url='index.htm'):
        """
        Get a URL from the userid/password protected powerswitch page Return None on failure
        """
        full_url = "%s/%s" % (self.base_url, url)
        result = None
        request = None
        logger.debug(f'Requesting url: {full_url}')
        loop = asyncio.get_event_loop()

        for i in range(0, self.retries):
            try:
                if self.secure_login and self.session:
                    request = partial(self.session.get, full_url, timeout=self.timeout, verify=False, allow_redirects=True)
                    res = await loop.run_in_executor(None, request)
                else:
                    request = partial(requests.get, full_url, auth=(self.userid, self.password,), timeout=self.timeout, verify=False, allow_redirects=True)  # nosec
                    res = await loop.run_in_executor(None, request)
            except requests.exceptions.RequestException as e:
                logger.warning("Request timed out - %d retries left.", self.retries - i - 1)
                logger.exception("Caught exception %s", str(e))
                continue
            if res.status_code == 200:
                result = res.content
                break
        logger.debug('Response code: %s', res.status_code)
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



#asyncio + aiohttp

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
                if self.secure_login:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(full_url, timeout=self.timeout, verify=False, allow_redirects=True) as res
                else:
                    res = requests.get(full_url, auth=(self.userid, self.password,), timeout=self.timeout, verify=False, allow_redirects=True)  # nosec
            except requests.exceptions.RequestException as e:
                logger.warning("Request timed out - %d retries left.", self.retries - i - 1)
                logger.exception("Caught exception %s", str(e))
                continue
            if res.status_code == 200:
                result = res.content
                break
        logger.debug('Response code: %s', res.status_code)
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
                if self.secure_login and self.session:
                    request = self.session.get(full_url, timeout=self.timeout, verify=False, allow_redirects=True)
                else:
                    request = requests.get(full_url, auth=(self.userid, self.password,), timeout=self.timeout, verify=False, allow_redirects=True)  # nosec
            except requests.exceptions.RequestException as e:
                logger.warning("Request timed out - %d retries left.", self.retries - i - 1)
                logger.exception("Caught exception %s", str(e))
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

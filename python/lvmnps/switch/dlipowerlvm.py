
import logging
import urllib3
import os
import requests
import requests.exceptions

from bs4 import BeautifulSoup
from clu.device import Device
import httpx


logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Global settings
TIMEOUT = 20
RETRIES = 3
CYCLETIME = 3
CONFIG_DEFAULTS = {
    'timeout': TIMEOUT,
    'cycletime': CYCLETIME,
    'userid': 'admin',
    'password': '4321',
    'hostname': '192.168.0.100'
}
CONFIG_FILE = os.path.expanduser('~/.dlipower.conf')


class PowerSwitch(Device):
    """ Powerswitch class to manage the Digital Loggers Web power switch """
    __len = 0
    login_timeout = 2.0
    secure_login = False

    async def __init__(self, userid=None, password=None, hostname=None, timeout=None,
                 cycletime=None, retries=None, use_https=False, name=None, port=None):
        Device.__init__(self, hostname, port)
        self.name = name
        """
        Class initializaton
        """
        if not retries:
            retries = RETRIES
        config = self.load_configuration()
        if retries:
            self.retries = retries
        if userid:
            self.userid = userid
        else:
            self.userid = config['userid']
        if password:
            self.password = password
        else:
            self.password = config['password']
        if hostname:
            self.hostname = hostname
        else:
            self.hostname = config['hostname']
        if timeout:
            self.timeout = float(timeout)
        else:
            self.timeout = config['timeout']
        if cycletime:
            self.cycletime = float(cycletime)
        else:
            self.cycletime = config['cycletime']
        self.scheme = 'http'
        if use_https:
            self.scheme = 'https'
        self.base_url = '%s://%s' % (self.scheme, self.hostname)
        self._is_admin = True
        self.client = httpx.AsyncClient()
        self.login()

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
                logger.warning("Request timed out - %d retries left.", self.retries - i - 1)
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
# Changelog


## 0.2.1e,f - October 22, 2021

This was a Minor update of version 0.2.1 , based on the code review from @albireox

Update for documentation
- Changed parts under ~/sphinx for sphinx documentation
- actor-schema documentation added
- removed README.rst


## 0.2.1c,d - October 22, 2021

This was a Minor update of version 0.2.1 , based on the code review from @albireox

Update for usage of json.schema
- Added code for using json.schema
- Changed the json.schema

Update for commands
- Changed the code for commands(on, off, status) since the schema changed.
- added 'reachable' command for checking out the reachable power switches.
- Changed the configuration file(.yml) under ~/etc

Update for configuration
- Using one configuration file, ~/lvmnps.yml

Update for unit test
- changing code for pytest


## 0.2.1 - October 10, 2021

This was a Major update, based on the code review from @albireox

Update for Code reliability
- Added docstring for functions and classes
- changed functionality of codes for configuration
- changed name of the dli power switch library
- changed the way connecting to the powerswitch using 'get' and 'put' method from 'httpx'


## 0.2.0 - August 13, 2021

    * Initial version of the library and actor. Supports communication with the Network power switch, lvmnps command to on, off and cycle the nps and return the status of power.
    
    * wrench Basic documentation(https://lvmnps.readthedocs.io/en/latest/).


## 0.1.4 - July 28, 2021

Update pyproject.toml


## 0.1.3 -July 2, 2021

removed test with pytest-rabbitmq

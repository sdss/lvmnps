# Changelog

## 1.0.3 - November 24, 2023

### ✨ Improved

* Added `all-off` command.


## 1.0.2 - November 24, 2023

### ✨ Improved

* It's now possible to call `status` with an outlet and a summary of the status for only that outlet will be issued.

### 🔧 Fixed

* Issue an NPS refresh before issuing any status.

### 📖 Documentation

* Added section on how to use the library.


## 1.0.1 - November 24, 2023

### ✨ Improved

* Added `NPSClient.all_off()` to turn off all outlets at once.


## 1.0.0 - November 24, 2023

### 🔥 Breaking changes

* [#36](https://github.com/sdss/lvmnps/pull/36) Complete rewrite, mostly to simplify the code and to take advantage of some additional features in the DLI REST API and to support calling DLI user scripts.
  * The main difference in this version is that the code has been significantly simplified by requiring that one instance of the `lvmnps` actor can only control one NPS. This means that all the `switch` flags and parameters have been deprecated.
  * The code has been simplified. It still follows the approach of a core, abstract `NPSClient` class with multiple implementations for different switches, but some options that were not used have been removed.
  * It's now possible to switch multiple outlets at the same time. This takes advantage of the DLI and NetIO implementations to turn on several outlets as quickly as possible without risking an in-rush overcurrent.
  * The DLI client now allows to command user functions (scripts).


## 0.4.0 - July 10, 2023

### 🚀 New

* [#34](https://github.com/sdss/lvmnps/pull/34) Add support for ``netio`` devices.

### ✨ Improved

* Bump `CLU` to 2.1.0.
* Various Docker image and build modifications for deployment in Kubernetes.
* Lock connections to DLI during a request.


## 0.3.0 - May 28, 2022

### 🔥 Breaking changes

* Major update with some breaking changes. Some of the main features are:
  * General clean-up, typing, linting, etc.
  * A few changes to how outlets are resolved depending on whether the name or the port are provided.
  * Some clean-up of the `DLI` and `DLIPowerSwitch` classes (new names). Nothing very major except that now if `ouo=False` in the configuration file, the port information is read directly from the API. This means that the outlet name is not `XXX.portN` anymore but whatever name is defined in the switch internal configuration. The default configuration for the LVM DLI switches does not specify the outlets anymore and instead reads them directly from the device.
  * Converted the switches list in `NPSActor.parser_args` to a dictionary.
  * For the `status`, `on` and `off` commands, changed the options and arguments. Now for `status` one can provide no arguments (all outlets are printed, as before), the switch name, the switch and port numbers, or the outlet to print.
  * Removed the `reachable` command group since it was confusing. Instead, added `outlets` and `switches` commands that output the same as `reachable outlets` and `reachable switches`.
  * Refactored the test fixtures a bit and increased test coverage to 85%-ish.
  * Changed documentation theme and cleaned up documentation a bit.


## 0.2.2 - May 23, 2022

* Added IEB02 to NPS configuration.
* Removed `iboot` power switch code.
* Improvements to testing and docs.


## 0.2.1e,f - October 25, 2021

This was a Minor update of version 0.2.1 , based on the code review from @albireox:

* Update for documentation
* Changed parts under ~/sphinx for sphinx documentation
* actor-schema documentation added
* removed README.rst


## 0.2.1c,d - October 22, 2021

This was a Minor update of version 0.2.1 , based on the code review from @albireox:

* Update for usage of json.schema
* Added code for using json.schema
* Changed the json.schema

* Update for commands
* Changed the code for commands(on, off, status) since the schema changed.
* Added 'reachable' command for checking out the reachable power switches.
* Changed the configuration file(.yml) under ~/etc

* Update for configuration
* Using one configuration file, ~/lvmnps.yml

* Update for unit test
* Changing code for pytest


## 0.2.1 - October 10, 2021

This was a Major update, based on the code review from @albireox:

* Update for Code reliability
* Added docstring for functions and classes
* Changed functionality of codes for configuration
* Changed name of the dli power switch library
* Changed the way connecting to the powerswitch using 'get' and 'put' method from 'httpx'


## 0.2.0 - August 13, 2021

* Initial version of the library and actor. Supports communication with the Network power switch, lvmnps command to on, off and cycle the nps and return the status of power.

* Basic documentation ([https://lvmnps.readthedocs.io/en/latest/](https://lvmnps.readthedocs.io/en/latest/)).


## 0.1.4 - July 28, 2021

Update pyproject.toml


## 0.1.3 -July 2, 2021

Removed test with pytest-rabbitmq

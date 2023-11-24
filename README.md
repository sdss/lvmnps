# lvmnps

![Versions](https://img.shields.io/badge/python->3.10-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/lvmnps/badge/?version=latest)](https://lvmnps.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/sdss/lvmnps/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/lvmnps/actions/workflows/test.yml)
[![Docker](https://github.com/sdss/lvmnps/actions/workflows/docker.yml/badge.svg)](https://github.com/sdss/lvmnps/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/sdss/lvmnps/branch/main/graph/badge.svg?token=M0RPGO77JH)](https://codecov.io/gh/sdss/lvmnps)

LVM Network Power Switch

## Features

- CLU Actor based interface
- Supports [Digital Loggers Web Power](https://www.digital-loggers.com/lpc7.html).
- Supports [NetIO](https://shop.netio.eu/netio-power-sockets/powerpdu-4ps--iec-320-c13-switched-power-distribution-unit/) power supplies.


## Installation

```console
pip install sdss-lvmnps
```

Or to install for development

```console
git clone https://github.com/sdss/lvmnps
cd lvmnps
poetry install
```

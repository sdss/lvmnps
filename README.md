# lvmnps

![Versions](https://img.shields.io/badge/python->3.8-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/lvmnps/badge/?version=latest)](https://lvmnps.readthedocs.io/en/latest/?badge=latest)
[![Test](https://github.com/sdss/lvmnps/actions/workflows/test.yml/badge.svg)](https://github.com/sdss/lvmnps/actions/workflows/test.yml)
[![Docker](https://github.com/sdss/lvmnps/actions/workflows/docker.yml/badge.svg)](https://github.com/sdss/lvmnps/actions/workflows/docker.yml)
[![codecov](https://codecov.io/gh/sdss/lvmnps/branch/main/graph/badge.svg?token=M0RPGO77JH)](https://codecov.io/gh/sdss/lvmnps)

LVM Network Power Switch

## Features

- CLU Actor based interface
- Supports a Dummy PDU
- Supports [iBOOT g2](https://dataprobe.com/iboot-g2/) with python code from [here](https://github.com/dprince/python-iboot)
- Supports [Digital Loggers Web Power](https://www.digital-loggers.com/lpc7.html) with python code from [here](https://github.com/dwighthubbard/python-dlipower)
- Supports [netio](https://shop.netio.eu/netio-power-sockets/powerpdu-4ps--iec-320-c13-switched-power-distribution-unit/) with python code from [here](https://github.com/netioproducts/PyNetio)


## Installation

Clone this repository.

```console
git clone https://github.com/sdss/lvmnps
cd lvmnps
```

## Quick Start

### Start the actor

Start `lvmnps` actor.

```console
lvmnps start
```

In another terminal, type `clu` and `lvmnps ping` for test.

```console
clu
lvmnps ping
     07:41:22.636 lvmnps >
     07:41:22.645 lvmnps : {
         "text": "Pong."
         }
```

Stop `lvmnps` actor.

```console
lvmnps stop
```

## Config file structure

```yaml
switches:
    name_your_switch_here:    # should be a unique name
        type: dummy           # currently dummy, iboot, dli
        num: 8                # number of ports
        ports:
            1:
            name: "skyw.pwi"  # should also be a unique name
            desc: "Something that make sense"
    should_be_a_unique_name:
        type: dummy
        ports:
            1:
            name: "skye.pwi"
            desc: "PlaneWavemount Skye"
```

## Status return for all commands

- if `name` is not defined then the port name will be `switch name.port number`, e.g. `nps_dummy_1.port1`. Otherwise `name` from the config file will be used.
- `STATE: 1: ON, 0: OFF, -1: UNKNOWN`

```yaml
    "STATUS": {
    "nps_dummy_1.port1": {
        "STATE": -1,
        "DESCR": "was 1",
        "SWITCH": "nps_dummy_1",
        "PORT": 1
    },
```

## Run the example lvmnps_dummy

```console
cd lvmnps
poetry run lvmnps -vvv -c $(pwd)/python/lvmnps/etc/lvmnps_dummy.yml start

poetry run clu
```

- Status command without parameter returns all ports of all switches.
- The default is to return only configured ports, otherwise define 'ouo' false in the config file, see [lvmnps_dummy.yml](https://github.com/sdss/lvmnps/blob/main/python/lvmnps/etc/lvmnps_dummy.yml)

```console
>>> lvmnps status

12:02:08.649 lvmnps >
12:02:08.660 lvmnps i {
    "STATUS": {
        "nps_dummy_1.port1": {
            "STATE": -1,
            "DESCR": "was 1",
            "SWITCH": "nps_dummy_1",
            "PORT": 1
        },
        "skye.what.ever": {
            "STATE": -1,
            "DESCR": "whatever is connected to skye",
            "SWITCH": "nps_dummy_1",
            "PORT": 2
        },
        "skyw.what.ever": {
            "STATE": -1,
            "DESCR": "Something @ skyw",
            "SWITCH": "nps_dummy_1",
            "PORT": 4
        },
        "skye.pwi": {
            "STATE": -1,
            "DESCR": "PlaneWavemount Skye",
            "SWITCH": "skye.nps",
            "PORT": 1
        },
            "skyw.pwi": {
            "STATE": -1,
            "DESCR": "PlaneWavemount Skyw",
            "SWITCH": "nps_dummy_3",
            "PORT": 1
        }
    }
}
```

- status command with port name skyw.what.ever

```console
>>> lvmnps status skyw.what.ever

12:07:12.349 lvmnps >
12:07:12.377 lvmnps i {
    "STATUS": {
        "skyw.what.ever": {
            "STATE": -1,
            "DESCR": "Something @ skyw",
            "SWITCH": "nps_dummy_1",
            "PORT": 4
}
```

- status command with switch name nps_dummy_1

```console
>>> lvmnps status nps_dummy_1

12:07:12.349 lvmnps >
12:12:21.349 lvmnps i {
    "STATUS": {
        "nps_dummy_1.port1": {
            "STATE": -1,
            "DESCR": "was 1",
            "SWITCH": "nps_dummy_1",
            "PORT": 1
        },
        "skye.what.ever": {
            "STATE": -1,
            "DESCR": "whatever is connected to skye",
            "SWITCH": "nps_dummy_1",
            "PORT": 2
        },
        "skyw.what.ever": {
            "STATE": -1,
            "DESCR": "Something @ skyw",
            "SWITCH": "nps_dummy_1",
            "PORT": 4
        }
    }
}
```

- status command with switch name nps_dummy_1 and port 4 returns

```console
      lvmnps status nps_dummy_1 4

      12:07:12.349 lvmnps >
      12:12:21.349 lvmnps i {
          "STATUS": {
              "skyw.what.ever": {
                  "STATE": -1,
                  "DESCR": "Something @ skyw",
                  "SWITCH": "nps_dummy_1",
                  "PORT": 4
              }
          }
      }


- the commands on and off use the same addressing scheme as status

## Test

```console
poetry run pytest
poetry run pytest -p no:logging -s -vv
```

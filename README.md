# lvmnps

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmnps/badge/?version=latest)](https://sdss-lvmnps.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmnps)](https://travis-ci.org/sdss/lvmnps)
[![codecov](https://codecov.io/gh/sdss/lvmnps/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmnps)
[![Test with RabbitMQ](https://github.com/wasndas/lvmnps/actions/workflows/test-rabbitmq.yml/badge.svg)](https://github.com/wasndas/lvmnps/actions/workflows/test-rabbitmq.yml)

Lvm Network Power Switch

## Features

- CLU Actor based interface
- Supports a Dummy PDU
- Supports [iBOOT g2](https://dataprobe.com/iboot-g2/) with python code from [here](https://github.com/dprince/python-iboot)
- Supports [Digital Loggers Web Power](https://www.digital-loggers.com/lpc7.html) with python code from [here](https://github.com/dwighthubbard/python-dlipower)

## Config file structure

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

## Status return for all commands
* if 'name' is not defined then the port name will be 'switch name'.'port number' eg nps_dummy_1.port1 otherwise 'name' from the config file will be used.
* STATE: 1: ON, 0: OFF, -1: UNKNOWN

             "STATUS": {
              "nps_dummy_1.port1": {
                  "STATE": -1,
                  "DESCR": "was 1",
                  "SWITCH": "nps_dummy_1",
                  "PORT": 1
              },

## Run the example lvmnps_dummy
    #> cd lvmnps
    #> poetry run lvmnps -vvv -c $(pwd)/python/lvmnps/etc/lvmnps_dummy.yml start

    #> poetry run clu
* status command without parameter returns all ports of all switches.    
* the default is to return only configured ports, otherwise define 'ouo' false in the config file, see [lvmnps_dummy.yml](https://github.com/sdss/lvmnps/blob/master/python/lvmnps/etc/lvmnps_dummy.yml)
    
      lvmnps status
      
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

* status command with port name skyw.what.ever

      lvmnps status skyw.what.ever
      
      12:07:12.349 lvmnps > 
      12:07:12.377 lvmnps i {
          "STATUS": {
              "skyw.what.ever": {
                  "STATE": -1,
                  "DESCR": "Something @ skyw",
                  "SWITCH": "nps_dummy_1",
                  "PORT": 4
        }

* status command with switch name nps_dummy_1

      lvmnps status nps_dummy_1
      
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
     
* status command with switch name nps_dummy_1 and port 4 returns

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
     

* the commands on and off use the same addressing scheme as status

## Test
     poetry run pytest
     poetry run pytest -p no:logging -s -vv 

## Quick Start

### Prerequisite

Install [CLU](https://clu.readthedocs.io/en/latest/) by using PyPI.
```
$ pip install sdss-clu
```

Install [RabbitMQ](https://www.rabbitmq.com/) by using apt-get.

```
$ sudo apt-get install -y erlang
$ sudo apt-get install -y rabbitmq-server
$ sudo systemctl enable rabbitmq-server
$ sudo systemctl start rabbitmq-server
```

Install [pyenv](https://github.com/pyenv/pyenv) by using [pyenv installer](https://github.com/pyenv/pyenv-installer).

```
$ curl https://pyenv.run | bash
```

You should add the code below to `~/.bashrc` by using your preferred editor.
```
# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

### Ping-pong test

Clone this repository.
```
$ git clone https://github.com/sdss/lvmnps
$ cd lvmnps
```

Set the python 3.9.1 virtual environment.
```
$ pyenv install 3.9.1
$ pyenv virtualenv 3.9.1 lvmnps-with-3.9.1
$ pyenv local lvmnps-with-3.9.1
```

Install [poetry](https://python-poetry.org/) and dependencies. For more information, check [sdss/archon](https://github.com/sdss/archon).
```
$ pip install poetry
$ python create_setup.py
$ pip install -e .
```

Start `lvmnps` actor.
```
$ lvmnps start
```

In another terminal, type `clu` and `lvmnps ping` for test.
```
$ clu
lvmnps ping
07:41:22.636 lvmnps > 
07:41:22.645 lvmnps : {
    "text": "Pong."
}
```

Stop `lvmnps` actor.
```
$ lvmnps stop
```

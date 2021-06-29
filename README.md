# lvmnps

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-lvmnps/badge/?version=latest)](https://sdss-lvmnps.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/lvmnps)](https://travis-ci.org/sdss/lvmnps)
[![codecov](https://codecov.io/gh/sdss/lvmnps/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmnps)


Lvm Network Power Switch

## Features

- CLU Actor based interface
- Supports a Dummy PDU
- Supports [iBOOT g2](https://dataprobe.com/iboot-g2/)
- Supports DLI...

## Config file structure

    switches:
        name_your_switch_here:
            type: dummy           # currently dummy, iboot, dli
            num: 8                # number of ports 
            ports: 
              1: 
                name: "skye.pwi"  # should also be a unique name
                desc: "Something that make sense"
        should_be_a_unique_name:
            type: dummy
            ports:
              1:  
                name: "skye.pwi"
                desc: "PlaneWavemount Skye"

## Run the example lvmnps_dummy
    #> cd lvmnps
    #> poetry run lvmnps -vvv -c $(pwd)/python/lvmnps/etc/lvmnps_dummy.yml start

    #> poetry run clu
* status command without parameter returns all ports of all switches.    
    
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
     


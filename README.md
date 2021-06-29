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
    cd lvmnps
    poetry run lvmnps -vvv -c $(pwd)/python/lvmnps/etc/lvmnps_dummy.yml 

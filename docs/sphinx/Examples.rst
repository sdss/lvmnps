.. _Examples:

Examples
=====================

Starting the Actor
----------------------

lvmnps actor provides the control system to manage the NPS.
First you have to start the actor by the terminal command line in the python virtual environment that you installed the lvmnps package. ::

  $ lvmnps start


If you want to start with debugging mode, you can start like this.
In this case, you can finish the software by ctrl + c on the terminal ::

  $ lvmnps start --debug


Also you can check the status of the actor is running by this command ::

  $ lvmnps status


After your work is done, you can finish the actor by this command ::

  $ lvmnps stop


Finally, you can restart(stop -> start) the actor when the actor is running by this command ::

  $ lvmnps restart


Interface with the Actor
----------------------------------

If you started the actor by the *lvmnps start* command, you can interface with the actor by the clu CLI(Command Line Interface) ::

  $ clu


If you want to ignore the status message from other actors, you can use this command ::

  $ clu -b


Then you will enter to the clu CLI. 
You can check if the actor is running by the ping-pong commands. ::

    lvmnps ping
    04:57:53.183 lvmnps > 
    04:57:53.198 lvmnps : {
        "text": "Pong."
    }
 


Help command
----------------------
          
First you can confirm the existing commands of *lvmnps* by the *help* command ::

    lvmnps help
    09:26:59.497 lvmnps > 
    09:26:59.512 lvmnps : {
        "help": [
            "Usage: lvmnps [OPTIONS] COMMAND [ARGS]...",
            "",
            "Options:",
            "  --help  Show this message and exit.",
            "",
            "Commands:",
            "  cycle     cycle power to an Outlet",
            "  device    return the list of devices connected with switch",
            "  help      Shows the help.",
            "  off       Turn off the Outlet",
            "  on        Turn on the Outlet",
            "  ping      Pings the actor.",
            "  status    print the status of the NPS.",
            "  switches  return the list of switches",
            "  version   Reports the version."
        ]
    }


switches command
-------------------

If you run the switches command via lvmnps, you can get the list of switches ::

    lvmnps switches

will return this kind of reply.::

    lvmnps switches
    09:27:25.948 lvmnps > 
    09:27:25.960 lvmnps i {
        "text": "the list of switches"
    }
    09:27:25.973 lvmnps i {
        "list": [
            "DLI-NPS-01",
            "DLI-NPS-02",
            "DLI-NPS-03"
        ]
    }
    09:27:25.985 lvmnps : {
        "text": "done"
    }


device command
---------------

If you run the device command via lvmnps, you can get the list of devices connected with the switch.::

    lvmnps device DLI-NPS-01

will return this kind of reply.::

    lvmnps device DLI-NPS-01
    08:19:36.478 lvmnps > 
    08:19:36.491 lvmnps i {
        "text": "Individual Control of DLI-NPS-01..."
    }
    08:19:37.191 lvmnps i {
        "IndividualControl": [
            "DLI-NPS-01.port1",
            "-",
            "DLI-NPS-01.port3",
            "DLI-NPS-01.port4",
            "DLI-NPS-01.port5",
            "DLI-NPS-01.port6",
            "DLI-NPS-01.port7",
            "625 nm LED (M625L4)"
        ]
    }
    08:19:37.204 lvmnps : {
        "text": "done"
    }


On command
---------------

If you run the on command via lvmnps, you can turn on the power of the device which you want to control.::

    lvmnps on eight

will return this kind of reply.::

    lvmnps on eight
    05:38:07.617 lvmnps > 
    05:38:07.633 lvmnps i {
        "text": "Turning on port eight..."
    }
    05:38:08.706 lvmnps i {
        "STATUS": {
            "DLI Controller": {
                "eight": {
                    "STATE": 1,
                    "DESCR": "DLI Controller Port 8",
                    "SWITCH": "DLI Controller",
                    "PORT": 8
                }
            }
        }
    }
    05:38:08.719 lvmnps : {
        "text": "done"
    }


Off command
---------------

If you run the off command via lvmnps, you can turn off the power of the device which you want to control.::

    lvmnps off eight

will return this kind of reply.::

    lvmnps off eight
    05:42:01.403 lvmnps > 
    05:42:01.423 lvmnps i {
        "text": "Turning off port eight..."
    }
    05:42:02.418 lvmnps i {
        "STATUS": {
            "DLI Controller": {
                "eight": {
                    "STATE": 0,
                    "DESCR": "DLI Controller Port 8",
                    "SWITCH": "DLI Controller",
                    "PORT": 8
                }
            }
        }
    }
    05:42:02.426 lvmnps : {
        "text": "done"
    }


Cycle command
---------------

If you run the cycle command via lvmnps, you can cycle the power of the device which you want to control.::

    lvmnps cycle eight

will return this kind of reply.::

    lvmnps cycle eight
    05:43:26.118 lvmnps > 
    05:43:26.135 lvmnps i {
        "text": "Cycle port eight..."
    }
    05:43:26.841 lvmnps : {
        "text": "done"
    }


Status command
----------------------
  
If you run the status command via lvmnps, you can receive the telemetry data of power status of devices ::

  lvmnps status *command*

*status* command group have two members *what* and *all*

what command
~~~~~~~~~~~~~~

What command provides the status of one device. If you run the status what command via lvmnps, you can receive the power status of device which you want to know the current status.::

    lvmnps status what DLI-NPS-01.port1

will return this kind of status data ::

    lvmnps status what DLI-NPS-01.port1
    05:09:13.509 lvmnps > 
    05:09:13.523 lvmnps i {
        "text": "Printing the current status of port DLI-NPS-01.port1"
    }
    05:09:14.420 lvmnps i {
        "STATUS": {
            "DLI-NPS-01": {
                "DLI-NPS-01.port1": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 1",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 1
                }
            }
        }
    }
    05:09:14.437 lvmnps : {
        "text": "done"
    }

or you can also put name of the NPS as the argument.::

    lvmnps status what DLI-NPS-01

will return this kind of status data ::

    lvmnps status what DLI-NPS-01
    05:40:51.669 lvmnps > 
    05:40:51.682 lvmnps i {
        "text": "Printing the current status of port DLI-NPS-01"
    }
    05:40:53.626 lvmnps i {
        "STATUS": {
            "DLI-NPS-01": {
                "DLI-NPS-01.port1": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 1",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 1
                },
                "-": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 2",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 2
                },
                "DLI-NPS-01.port3": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 3",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 3
                },
                "DLI-NPS-01.port4": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 4",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 4
                },
                "DLI-NPS-01.port5": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 5",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 5
                },
                "DLI-NPS-01.port6": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 6",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 6
                },
                "DLI-NPS-01.port7": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 7",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 7
                },
                "625 nm LED (M625L4)": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 8
                }
            }
        }
    }
    05:40:53.639 lvmnps : {
        "text": "done"
    }



all command
~~~~~~~~~~~~~~

All command provides the status of all device connected with the NPS. If you run the status all command via lvmnps, you can receive the power status of all device.::

    lvmnps status all

will return this kind of status data ::

    lvmnps status all
    05:18:06.916 lvmnps > 
    05:18:06.929 lvmnps i {
        "text": "Printing the current status of switch DLI-NPS-01"
    }
    05:18:07.201 lvmnps i {
        "STATUS": {
            "DLI-NPS-01": {
                "DLI-NPS-01.port1": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 1",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 1
                },
                "-": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 2",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 2
                },
                "DLI-NPS-01.port3": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 3",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 3
                },
                "DLI-NPS-01.port4": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 4",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 4
                },
                "DLI-NPS-01.port5": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 5",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 5
                },
                "DLI-NPS-01.port6": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 6",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 6
                },
                "DLI-NPS-01.port7": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 7",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 7
                },
                "625 nm LED (M625L4)": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 8
                }
            }
        }
    }
    05:18:07.217 lvmnps i {
        "text": "Printing the current status of switch DLI-NPS-02"
    }
    05:18:07.497 lvmnps i {
        "STATUS": {
            "DLI-NPS-01": {
                "DLI-NPS-01.port1": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 1",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 1
                },
                "-": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 2",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 2
                },
                "DLI-NPS-01.port3": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 3",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 3
                },
                "DLI-NPS-01.port4": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 4",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 4
                },
                "DLI-NPS-01.port5": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 5",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 5
                },
                "DLI-NPS-01.port6": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 6",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 6
                },
                "DLI-NPS-01.port7": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 7",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 7
                },
                "625 nm LED (M625L4)": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 8
                }
            },
            "DLI-NPS-02": {
                "Router/Switch": {
                    "STATE": 1,
                    "DESCR": "Router power switch",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 1
                },
                "LN2 NIR valve": {
                    "STATE": 0,
                    "DESCR": "Cryogenic solenoid valve of NIR camera for liquid nitrogen.",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 2
                },
                "LVM-Archon-02": {
                    "STATE": 1,
                    "DESCR": "Archon controller",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 3
                },
                "IEB06": {
                    "STATE": 1,
                    "DESCR": "LVM Instrument Electronic Box",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 4
                },
                "LN2 Red Valve": {
                    "STATE": 0,
                    "DESCR": "Cryogenic solenoid valve of Red camera for liquid nitrogen.",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 5
                },
                "RPi": {
                    "STATE": 1,
                    "DESCR": "Raspberry Pi",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 6
                },
                "FFS LED": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 7
                },
                "Pressure transducers": {
                    "STATE": 1,
                    "DESCR": "Pressure transducers",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 8
                }
            }
        }
    }
    05:18:07.514 lvmnps i {
        "text": "Printing the current status of switch DLI-NPS-03"
    }
    05:18:07.811 lvmnps i {
        "STATUS": {
            "DLI-NPS-01": {
                "DLI-NPS-01.port1": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 1",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 1
                },
                "-": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 2",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 2
                },
                "DLI-NPS-01.port3": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 3",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 3
                },
                "DLI-NPS-01.port4": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 4",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 4
                },
                "DLI-NPS-01.port5": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 5",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 5
                },
                "DLI-NPS-01.port6": {
                    "STATE": 1,
                    "DESCR": "DLI-NPS-01 Port 6",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 6
                },
                "DLI-NPS-01.port7": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-01 Port 7",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 7
                },
                "625 nm LED (M625L4)": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-01",
                    "PORT": 8
                }
            },
            "DLI-NPS-02": {
                "Router/Switch": {
                    "STATE": 1,
                    "DESCR": "Router power switch",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 1
                },
                "LN2 NIR valve": {
                    "STATE": 0,
                    "DESCR": "Cryogenic solenoid valve of NIR camera for liquid nitrogen.",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 2
                },
                "LVM-Archon-02": {
                    "STATE": 1,
                    "DESCR": "Archon controller",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 3
                },
                "IEB06": {
                    "STATE": 1,
                    "DESCR": "LVM Instrument Electronic Box",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 4
                },
                "LN2 Red Valve": {
                    "STATE": 0,
                    "DESCR": "Cryogenic solenoid valve of Red camera for liquid nitrogen.",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 5
                },
                "RPi": {
                    "STATE": 1,
                    "DESCR": "Raspberry Pi",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 6
                },
                "FFS LED": {
                    "STATE": 0,
                    "DESCR": "LED",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 7
                },
                "Pressure transducers": {
                    "STATE": 1,
                    "DESCR": "Pressure transducers",
                    "SWITCH": "DLI-NPS-02",
                    "PORT": 8
                }
            },
            "DLI-NPS-03": {
                "Argon": {
                    "STATE": 0,
                    "DESCR": "Hg-Ar spectral calibration Lamp",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 1
                },
                "Outlet 2": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-03 Port 2",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 2
                },
                "Outlet 3": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-03 Port 3",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 3
                },
                "LDLS": {
                    "STATE": 0,
                    "DESCR": "LDLS spectral calibration Lamp",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 4
                },
                "Krypton": {
                    "STATE": 0,
                    "DESCR": "Krypton spectral calibration Lamp",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 5
                },
                "Neon": {
                    "STATE": 0,
                    "DESCR": "Neon spectral calibration Lamp",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 6
                },
                "Outlet 7": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-03 Port 7",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 7
                },
                "Outlet 8": {
                    "STATE": 0,
                    "DESCR": "DLI-NPS-03 Port 8",
                    "SWITCH": "DLI-NPS-03",
                    "PORT": 8
                }
            }
        }
    }
    05:18:07.828 lvmnps : {
        "text": "done"
    }
    
.. _examples:

Examples
========

Starting the Actor
------------------

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


Interface with the actor
------------------------

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



``help`` command
----------------

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


``reachable`` command
---------------------

If you run the switches command via lvmnps, you can get the list of switches ::

    lvmnps reachable switches

will return this kind of reply.::

    lvmnps reachable switches
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


If you run the outlet command via lvmnps reachable command, you can get the list of devices connected with the switch.::

    lvmnps reachable outlets DLI-NPS-01

will return this kind of reply.::

    lvmnps reachable outlets DLI-NPS-01
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


``on`` command
--------------

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


``off`` command
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


``status`` command
------------------

If you run the status command via lvmnps, you can receive the telemetry data of power status of devices ::

  lvmnps status *command*

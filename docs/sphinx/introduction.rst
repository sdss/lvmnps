.. _introduction:

Introduction
============

``lvmnps`` allows for basic, homogeneous control of a variety of network power supplies (NPS). Currently the supported NPS are

- `Digital Loggers Inc devices <http://www.digital-loggers.com>`__, in particular the `Pro Switch <http://www.digital-loggers.com/pro.html>`__
- `NetIO devices <https://www.netio-products.com/en>`__.

The code allows to retrieve the status of the various outlets, set outlet status (on, off, cycle), and execute user functions (only for DLI devices).


Installation
------------

``lvmscp`` can be installed using ``pip`` as

.. code:: shell

    pip install sdss-lvmnps

To install ``lvmnps`` for development, first clone the `repository <https://github.com/sdss/lvmnps>`__

.. code:: shell

    git clone https://github.com/sdss/lvmnps

and then install using `poetry <https://python-poetry.org>`__

.. code:: shell

    poetry install


Using the library
-----------------

To connect to an NPS, first import the switch client class (available implementations are `.DLIClient` and `.NetIOClient`) and instantiate them with the appropriate parameters. Then call `.NPSClient.setup` to initialise the connection and refresh the list of outlets.

.. code:: python

    from lvmnps import DLIClient

    client = DLIClient(host='127.0.0.1', port=8088, user='admin', password='admin')
    await client.setup()

We can then retrieve the list of outlets and their status

.. code:: python

    >>> client.outlets
    {'argon': DLIOutletModel(id=1, name='Argon', normalised_name='argon', state=False, index=0, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'neon': DLIOutletModel(id=2, name='Neon', normalised_name='neon', state=False, index=1, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'ldls': DLIOutletModel(id=3, name='LDLS', normalised_name='ldls', state=False, index=2, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'quartz': DLIOutletModel(id=4, name='Quartz', normalised_name='quartz', state=False, index=3, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'hgne': DLIOutletModel(id=5, name='HgNe', normalised_name='hgne', state=False, index=4, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'xenon': DLIOutletModel(id=6, name='Xenon', normalised_name='xenon', state=False, index=5, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'outlet_7': DLIOutletModel(id=7, name='Outlet 7', normalised_name='outlet_7', state=False, index=6, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None),
 'outlet8': DLIOutletModel(id=8, name='Outlet8', normalised_name='outlet8', state=False, index=7, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None)}

All outlets share some common attributes, including ``id`` (a numerical identifier), ``name``, ``normalised_name`` (a normalised version of the name, useful for programmatic access), and ``state`` (the current state of the outlet). Certain types of outlets may include additional parameters.

To retrieve an outlet by name or id ::

    >>> client.get(5)
    DLIOutletModel(id=5, name='HgNe', normalised_name='hgne', state=False, index=4, physical_state=False, transient_state=False, critical=False, locked=False, cycle_delay=None)

To refresh the internal state of the outlets you can issue ::

    await client.refresh()

And to switch an outlet on or off ::

    await client.set_state(5, on=True)
    await client.set_state('hgne', on=False)

`.NPSClient.set_state` accepts either a single outlet (identifid by its name or id) or a list of outlets. In the latter case, the NPS implementation will try to switch on/off the outlets are quickly as possible while preventing in-rush overcurrent.


Configuration files
-------------------

To run as an actor, a YAML configuration file is required. An example of a valid configuration file is

.. code:: yaml

    nps:
        type: dli
        init_parameters:
            host: 127.0.0.1
            port: 8088
            user: admin
            password: admin

    actor:
        name: lvmnps.test
        host: localhost
        port: 5672

The ``actor`` section is common to other CLU actors, and we refer the reader to the `CLU documentation <https://clu.readthedocs.io/en/latest/getting-started.html#configuration-files>`__. An ``nps`` section is required, defining the type of the power supply (valid types are ``dli`` and ``netio``) and the parameters necessary to initialise the relevant client class.


Running the actor
-----------------

The actor can be run by executing

.. code:: shell

    lvmnps -c CONFIG-FILE start [--debug]

where ``--debug`` allows to run the actor without detaching the running instance. To stop the actor use ``lvmnps stop``.

To test the communication with the actor you can install the CLU command line interface, then execute ``clu`` and issue ``lvmnps status``.

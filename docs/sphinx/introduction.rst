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

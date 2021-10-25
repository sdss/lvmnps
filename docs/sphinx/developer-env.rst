lvmnps
======

Lvm Network Power Switch

Features
--------

-  CLU Actor based interface
-  Supports a Dummy PDU
-  Supports `iBOOT g2 <https://dataprobe.com/iboot-g2/>`__ with python
   code from `here <https://github.com/dprince/python-iboot>`__
-  Supports `Digital Loggers Web
   Power <https://www.digital-loggers.com/lpc7.html>`__ with python code
   from `here <https://github.com/dwighthubbard/python-dlipower>`__

Installation
------------

Clone this repository.

::

    $ git clone https://github.com/sdss/lvmnps
    $ cd lvmnps

Quick Start
-----------

Prerequisite
~~~~~~~~~~~~

If your system already have rabbitmq, and already running with the actors, you don't have to install these below.
Install `RabbitMQ <https://www.rabbitmq.com/>`__ by using apt-get.
RabbitMQ is not the dependency of the 'lvmnps' but it is the system-wide configuration for running the software under CLU CLI(command line interface).

::

    $ sudo apt-get install -y erlang
    $ sudo apt-get install -y rabbitmq-server
    $ sudo systemctl enable rabbitmq-server
    $ sudo systemctl start rabbitmq-server


If your system already have pyenv, you don't have to install these below.
Install `pyenv <https://github.com/pyenv/pyenv>`__ by using `pyenv
installer <https://github.com/pyenv/pyenv-installer>`__.
Also, pyenv is the virtual environment for running the python package under your specific python environment.
This is very useful when you want to isolate your python package with others.

::

    $ curl https://pyenv.run | bash

You should add the code below to ``~/.bashrc`` by using your preferred
editor.

::

    # pyenv
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"

``pyenv`` builds Python from source. So you should install build
dependencies. For more information, check `Common build
problems <https://github.com/pyenv/pyenv/wiki/Common-build-problems>`__.

::

    $ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

Set the python 3.9.1 virtual environment.

::

    $ pyenv install 3.9.1
    $ pyenv virtualenv 3.9.1 lvmnps-with-3.9.1
    $ pyenv local lvmnps-with-3.9.1

Install `poetry <https://python-poetry.org/>`__ and dependencies. For
more information, check
`sdss/archon <https://github.com/sdss/archon>`__.

::

    $ pip install poetry
    $ python create_setup.py
    $ pip install -e .

Test
----

::

     poetry run pytest
     poetry run pytest -p no:logging -s -vv 
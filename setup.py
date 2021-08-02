# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['lvmnps',
 'lvmnps.actor',
 'lvmnps.actor.commands',
 'lvmnps.switch',
 'lvmnps.switch.dli',
 'lvmnps.switch.dummy',
 'lvmnps.switch.iboot']

package_data = \
{'': ['*'], 'lvmnps': ['etc/*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'asyncinit>=0.2.4,<0.3.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'daemonocle>=1.1.1,<2.0.0',
 'dlipower>=1.0.176,<2.0.0',
 'httpx>=0.18.1,<0.19.0',
 'sdss-access>=0.2.3',
 'sdss-clu>=1.0.3,<2.0.0',
 'sdss-tree>=2.15.2',
 'sdsstools>=0.4.0',
 'sphinx-bootstrap-theme>=0.7.1,<0.8.0']

extras_require = \
{'docs': ['Sphinx>=4.0.2,<5.0.0', 'sphinx_bootstrap_theme>=0.4.12']}

entry_points = \
{'console_scripts': ['lvmnps = lvmnps.__main__:lvmnps']}

setup_kwargs = {
    'name': 'sdss-lvmnps',
    'version': '0.1.3',
    'description': 'Simple Template package for creating SDSS Python projects',
    'long_description': '# lvmnps\n\n![Versions](https://img.shields.io/badge/python->3.7-blue)\n[![Documentation Status](https://readthedocs.org/projects/sdss-lvmnps/badge/?version=latest)](https://sdss-lvmnps.readthedocs.io/en/latest/?badge=latest)\n[![Travis (.org)](https://img.shields.io/travis/sdss/lvmnps)](https://travis-ci.org/sdss/lvmnps)\n[![codecov](https://codecov.io/gh/sdss/lvmnps/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/lvmnps)\n[![Test with RabbitMQ](https://github.com/wasndas/lvmnps/actions/workflows/test-rabbitmq.yml/badge.svg)](https://github.com/wasndas/lvmnps/actions/workflows/test-rabbitmq.yml)\n\nLvm Network Power Switch\n\n## Features\n\n- CLU Actor based interface\n- Supports a Dummy PDU\n- Supports [iBOOT g2](https://dataprobe.com/iboot-g2/) with python code from [here](https://github.com/dprince/python-iboot)\n- Supports [Digital Loggers Web Power](https://www.digital-loggers.com/lpc7.html) with python code from [here](https://github.com/dwighthubbard/python-dlipower)\n\n## Config file structure\n\n    switches:\n        name_your_switch_here:    # should be a unique name\n            type: dummy           # currently dummy, iboot, dli\n            num: 8                # number of ports \n            ports: \n              1: \n                name: "skyw.pwi"  # should also be a unique name\n                desc: "Something that make sense"\n        should_be_a_unique_name:\n            type: dummy\n            ports:\n              1:  \n                name: "skye.pwi"\n                desc: "PlaneWavemount Skye"\n\n## Status return for all commands\n* if \'name\' is not defined then the port name will be \'switch name\'.\'port number\' eg nps_dummy_1.port1 otherwise \'name\' from the config file will be used.\n* STATE: 1: ON, 0: OFF, -1: UNKNOWN\n\n             "STATUS": {\n              "nps_dummy_1.port1": {\n                  "STATE": -1,\n                  "DESCR": "was 1",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 1\n              },\n\n## Run the example lvmnps_dummy\n    #> cd lvmnps\n    #> poetry run lvmnps -vvv -c $(pwd)/python/lvmnps/etc/lvmnps_dummy.yml start\n\n    #> poetry run clu\n* status command without parameter returns all ports of all switches.    \n* the default is to return only configured ports, otherwise define \'ouo\' false in the config file, see [lvmnps_dummy.yml](https://github.com/sdss/lvmnps/blob/master/python/lvmnps/etc/lvmnps_dummy.yml)\n    \n      lvmnps status\n      \n      12:02:08.649 lvmnps > \n      12:02:08.660 lvmnps i {\n          "STATUS": {\n              "nps_dummy_1.port1": {\n                  "STATE": -1,\n                  "DESCR": "was 1",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 1\n              },\n              "skye.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "whatever is connected to skye",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 2\n              },\n              "skyw.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "Something @ skyw",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 4\n              },\n              "skye.pwi": {\n                  "STATE": -1,\n                  "DESCR": "PlaneWavemount Skye",\n                  "SWITCH": "skye.nps",\n                  "PORT": 1\n              },\n                  "skyw.pwi": {\n                  "STATE": -1,\n                  "DESCR": "PlaneWavemount Skyw",\n                  "SWITCH": "nps_dummy_3",\n                  "PORT": 1\n              }\n          }\n      }\n\n* status command with port name skyw.what.ever\n\n      lvmnps status skyw.what.ever\n      \n      12:07:12.349 lvmnps > \n      12:07:12.377 lvmnps i {\n          "STATUS": {\n              "skyw.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "Something @ skyw",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 4\n        }\n\n* status command with switch name nps_dummy_1\n\n      lvmnps status nps_dummy_1\n      \n      12:07:12.349 lvmnps > \n      12:12:21.349 lvmnps i {\n          "STATUS": {\n              "nps_dummy_1.port1": {\n                  "STATE": -1,\n                  "DESCR": "was 1",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 1\n              },\n              "skye.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "whatever is connected to skye",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 2\n              },\n              "skyw.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "Something @ skyw",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 4\n              }\n          }\n      }\n     \n* status command with switch name nps_dummy_1 and port 4 returns\n\n      lvmnps status nps_dummy_1 4\n      \n      12:07:12.349 lvmnps > \n      12:12:21.349 lvmnps i {\n          "STATUS": {\n              "skyw.what.ever": {\n                  "STATE": -1,\n                  "DESCR": "Something @ skyw",\n                  "SWITCH": "nps_dummy_1",\n                  "PORT": 4\n              }\n          }\n      }\n     \n\n* the commands on and off use the same addressing scheme as status\n\n## Test\n     poetry run pytest\n     poetry run pytest -p no:logging -s -vv \n\n',
    'author': 'Changgon Kim',
    'author_email': 'changgonkim@khu.ac.kr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sdss/lvmnps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

# This setup.py was autogenerated using poetry.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools import get_config, get_logger, get_package_version


NAME = "sdss-lvmnps"


log = get_logger(NAME, use_rich_handler=True)

__version__ = get_package_version(path=__file__, package_name=NAME)


from .actor import NPSActor, NPSCommand
from .nps import DLIClient, NPSClient

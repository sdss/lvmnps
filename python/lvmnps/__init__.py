#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools import get_config, get_logger, get_package_version


# pip package name
NAME = "sdss-lvmnps"

# Loads config. config name is the package name.
config = get_config("lvmnps")
log = get_logger(NAME)

# package name should be pip package name
__version__ = get_package_version(path=__file__, package_name=NAME)

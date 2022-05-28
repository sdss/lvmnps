# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Mingyeong Yang (mingyeong@khu.ac.kr), Changgon Kim (changgonkim@khu.ac.kr)
# @Date: 2021-08-24
# @Update: 2021-10-09
# @Filename: lvmnps/switch/dli/dli.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import absolute_import, division, print_function


class NpsActorError(Exception):
    """A custom core NpsActor exception"""

    def __init__(self, message=None):

        message = "There has been an error" if not message else message

        super(NpsActorError, self).__init__(message)


class NpsActorWarning(Warning):
    """Base warning for NpsActor."""


class PowerException(Exception):
    """An error Exception class for powerswitch factory."""

    pass

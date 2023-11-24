#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations


__all__ = [
    "DLIClient",
    "DLIOutletModel",
    "NetIOClient",
    "NetIOOutLetModel",
    "VALID_NPS_TYPES",
]


VALID_NPS_TYPES: list[str] = ["dli", "netio"]


from .dli import DLIClient, DLIOutletModel
from .netio import NetIOClient, NetIOOutLetModel

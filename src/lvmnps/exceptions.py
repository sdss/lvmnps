#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: exceptions.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations


class NPSException(Exception):
    """Base NPS exception."""


class VerificationError(NPSException):
    """Failed to connect to the power supply."""


class ResponseError(NPSException):
    """Invalid response from the power supply API."""


class NPSWarning(UserWarning):
    """Base NPS warning."""

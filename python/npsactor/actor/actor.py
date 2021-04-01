#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
import os
import warnings
from contextlib import suppress

from clu.actor import AMQPActor

__all__ = ["NpsActor"]

class NpsActor(AMQPActor):
    """NPS actor.
    In addition to the normal arguments and keyword parameters for
    `~clu.actor.AMQPActor`, the class accepts the following parameters.
    Parameters (TBD)
    """
    def __init__(self):
        super().__init__(
            name="NpsActor",
            user="guest",
            password="guest",
            host="localhost",
            port=5672,
            version="0.1.0",
            )

    async def start(self):
        await super().start()

    async def stop(self):
        with suppress(asyncio.CancelledError):
            for task in self._fetch_log_jobs:
                task.cancel()
                await task
        return super().stop()

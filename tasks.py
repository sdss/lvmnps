#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: tasks.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pathlib
import tempfile

from invoke.context import Context
from invoke.tasks import task


@task()
def docs_live(context: Context):
    """Uses sphinx-autobuild to build a temporary copy of the docs."""

    docs_dir = pathlib.Path(__file__).parent / "docs/sphinx"

    with context.cd(docs_dir):
        with tempfile.TemporaryDirectory() as destination:
            context.run(
                "sphinx-autobuild --port=0 --open-browser -b=dirhtml "
                f"-a {docs_dir} {destination} --watch ../../src/lvmnps",
                pty=True,
            )

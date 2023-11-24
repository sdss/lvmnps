#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-23
# @Filename: test_tools.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import pytest

from lvmnps.nps.core import OutletModel
from lvmnps.tools import get_outlet_by_id, get_outlet_by_name, normalise_outlet_name


@pytest.fixture
def outlets():
    _outlets: list[OutletModel] = []

    for id_ in range(1, 6):
        _outlets.append(OutletModel(id=id_, name=f"Outlet {id_}"))

    yield {_outlet.normalised_name: _outlet for _outlet in _outlets}


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        ["Outlet1", "outlet1"],
        ["oUtlEt 1", "outlet_1"],
        ["outlet_1", "outlet_1"],
    ],
)
def test_nomalise_name(input: str, expected: str):
    assert normalise_outlet_name(input) == expected


@pytest.mark.parametrize("input", ["outlet 1", "Outlet 1", "outlet_1"])
def test_get_outlet_by_name(outlets: dict[str, OutletModel], input: str):
    outlet = get_outlet_by_name(outlets, input)

    assert outlet.normalised_name == "outlet_1"
    assert outlet.id == 1


def test_get_outlet_by_name_not_found(outlets: dict[str, OutletModel]):
    with pytest.raises(ValueError):
        get_outlet_by_name(outlets, "outlet 7")


@pytest.mark.parametrize("input", [1, 3, 5])
def test_get_outlet_by_id(outlets: dict[str, OutletModel], input: int):
    outlet = get_outlet_by_id(outlets, input)

    assert outlet.id == input


def test_get_outlet_by_id_not_found(outlets: dict[str, OutletModel]):
    with pytest.raises(ValueError):
        get_outlet_by_id(outlets, 7)

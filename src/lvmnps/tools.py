#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-11-22
# @Filename: tools.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from lvmnps.nps.core import OutletModel


__all__ = ["normalise_outlet_name", "get_outlet_by_name", "get_outlet_by_id"]


def normalise_outlet_name(name: str):
    """Returns a normalised name for an outlet."""

    return name.lower().replace(" ", "_")


def get_outlet_by_name(
    outlet_data: dict[str, OutletModel],
    name: str,
    allow_non_normalised: bool = True,
):
    """Gets an outlet from a list of outlets.

    Parameters
    ----------
    outlet_data
        The mapping of outlet name to outlet model data.
    name
        The name of the outlet to retrieve.
    allow_non_normalised
        If `True`, and ``name`` does match any normalised outlet name, tries to
        find an outlet whose original name matches ``name``.

    Returns
    -------
    outlet
        The outlet matching the input name.

    Raises
    ------
    ValueError
        If the outlet cannot be found.

    """

    normalised_name = normalise_outlet_name(name)

    if normalised_name in outlet_data:
        return outlet_data[normalised_name]

    if allow_non_normalised:
        for outlet in outlet_data.values():
            if outlet.name == name:
                return outlet

    raise ValueError(f"Cannot find outlet with name {name!r}.")


def get_outlet_by_id(outlet_data: dict[str, OutletModel], id: int):
    """Gets an outlet by id.

    Parameters
    ----------
    outlet_data
        The mapping of outlet name to outlet model data.
    id
        The id of the outlet to retrieve.

    Returns
    -------
    outlet
        The outlet matching the id.

    Raises
    ------
    ValueError
        If the outlet cannot be found.

    """

    for outlet in outlet_data.values():
        if outlet.id == id:
            return outlet

    raise ValueError(f"Cannot find outlet with id {id!r}.")

#!/usr/bin/env python3
"""
This module provides utility functions for working with lists
of numbers, including functions that handle
mixed lists of integers and floats.

Functions:
- sum_mixed_list: Sums a list containing both integers
and floats, returning the total as a float.
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    Sums a mixed list of integers and floats.

    Parameters:
    mxd_lst (List[Union[int, float]]):
    A list containing both integers and floats.

    Returns:
    float: The sum of all elements in the list as a float.
    """
    return sum(mxd_lst)

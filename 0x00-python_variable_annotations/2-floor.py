#!/usr/bin/env python3
"""
This module provides utility functions for mathematical operations.

The module currently includes a custom implementation of the floor function,
which returns the floor of a given float number. The floor of a number is the
largest integer less than or equal to the number.

"""

import math


def floor(n: float) -> int:
    """
    Returns the floor of the float number.

    Parameters:
    n (float): The float number to find the floor of.

    Returns:
    int: The floor of n.
    """
    return math.floor(n)

#!/usr/bin/env python3
"""
This module provides a type-annotated function `to_kv` that takes a string and
an integer or float, then returns a tuple. The first element of the tuple is
the string, and the second element is the square of the integer or float,
returned as a float.
"""

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Converts a string and an int/float to a tuple with the string and the
    square of the int/float.

    Parameters:
    k (str): The string part of the tuple.
    v (Union[int, float]): The number to be squared and included in the tuple.

    Returns:
    Tuple[str, float]: A tuple of the string and the square of the number.
    """
    return (k, float(v ** 2))

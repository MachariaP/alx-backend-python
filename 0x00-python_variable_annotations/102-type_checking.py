#!/usr/bin/env python3
"""
Demonstrates type annotations by repeating elements in a tuple.
"""

from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Repeats each tuple element a specified number of times.

    Parameters:
    - lst: Tuple of integers.
    - factor: Repetition factor.

    Returns:
    - List of repeated elements.
    """
    return [item for item in lst for _ in range(factor)]


array = [12, 72, 91]

zoom_2x = zoom_array(tuple(array))

zoom_3x = zoom_array(tuple(array), 3)

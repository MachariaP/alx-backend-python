#!/usr/bin/env python3
"""
Defines a function `zoom_array` that repeats each element in
a tuple a specified
number of times, demonstrating the use of type annotations and type checking.
"""

from typing import Tuple, List


def zoom_array(lst: Tuple[int, ...], factor: int = 2) -> List[int]:
    """
    Repeats each element in a tuple a specified number of times.

    Parameters:
    lst (Tuple[int, ...]): Tuple of integers to be repeated.
    factor (int): Number of repetitions for each element.

    Returns:
    List[int]: List of repeated elements.
    """
    return [item for item in lst for _ in range(factor)]

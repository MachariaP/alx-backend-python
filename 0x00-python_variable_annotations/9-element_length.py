#!/usr/bin/env python3
"""
This module provides a function `element_length` that takes an iterable of
sequences (like lists, strings, etc.) and returns a list of tuples. Each tuple
contains an element from the iterable and the length of that element,
demonstrating an application of duck typing in Python.

Example:
    result = element_length(["hello", "world"])
    print(result)  # Output: [("hello", 5), ("world", 5)]
"""

from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples, each containing an element from
    the input iterable and the length of that element.

    Parameters:
    lst (Iterable[Sequence]): An iterable of sequences.

    Returns:
    List[Tuple[Sequence, int]]: A list of tuples with each tuple containing a
    sequence and its length.
    """
    return [(i, len(i)) for i in lst]

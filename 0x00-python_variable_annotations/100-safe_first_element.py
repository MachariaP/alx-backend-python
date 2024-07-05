#!/usr/bin/env python3
"""
This module demonstrates the concept of duck typing in Python by providing a
function `safe_first_element` that attempts to return the first element of a
sequence. The function is designed to work with any type of sequence (lists,
strings, etc.) without knowing the specific type of
elements it contains. If the
sequence is empty, the function returns None, showcasing a safe way to access
the first element of sequences that might be empty.

"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Returns the first element of a sequence, or None if the sequence is empty.

    Parameters:
    lst (Sequence[Any]): A sequence from which the first
    element is to be returned.

    Returns:
    Union[Any, None]: The first element of the sequence,
    or None if the sequence is empty.
    """
    if lst:
        return lst[0]
    else:
        return None

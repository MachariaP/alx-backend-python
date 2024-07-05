#!/usr/bin/env python3
"""
This module enhances a function with type annotations using TypeVar for more
precise type checking. The function `safely_get_value` attempts to return a
value from a dictionary for a given key. If the key is not found, it returns a
default value. Type annotations ensure compatibility with various types of keys
and values while maintaining the flexibility of the default value's type.

"""

from typing import Mapping, Any, TypeVar, Union

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """
    Returns the value for a given key from a dictionary.
    If the key is not found,returns a default value.

    Parameters:
    dct (Mapping): The dictionary from which to retrieve the value.
    key (Any): The key to look for in the dictionary.
    default (Union[T, None], optional): The default value to
    return if the key is not found.

    Returns:
    Union[Any, T]: The value associated with the key, or the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default

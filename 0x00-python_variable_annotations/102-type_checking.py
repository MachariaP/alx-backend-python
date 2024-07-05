#!/usr/bin/env python3

"""Module that contains a type-annotated function zoom_array
that takes a tuple of integers and returns a tuple of integers
with a factor of 2 or 3.0.
The type of the input tuple is Tuple and the type of
the output tuple is Tuple
"""


# import Tuple class from the typing module
from typing import Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> Tuple:
    """ Change the annotation for 1st and return the type
        to Tuple
        to indicate that the function accepts and
        returns a tuple of any type.
        Also, change type of array to tuple() instead of list[].
        Lastly, change the float value to interger
        when calling zoom_array
    """
    zoomed_in: Tuple = tuple(
        item for item in lst
        for i in range(factor)
    )
    return zoomed_in


array = (12, 72, 91)  # use tuple instead of list

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)  # use interger value for the factor

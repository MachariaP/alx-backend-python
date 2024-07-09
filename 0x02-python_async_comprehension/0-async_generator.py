#!/usr/bin/env python3

"""
This function asynchronously generates a sequence of 10 random numbers.

It uses an asymchronous loop to wait for 1 second between each yield.
Each yielded value is a random float between 0 and 10 (inclusive).

Args:
    None

Returns:
    An asynchronous generator object that yield random floats.
"""

import asyncio
import random


async def async_generator():
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)

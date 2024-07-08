#!/usr/bin/env python3
"""
Use of asyncio to run multiple instances of an
asynchronous function concurrently.
"""

import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Execute `wait_random` n times with the specified `max_delay`.
    Returns the list of wait times in the order they were initiated.

    Args:
        n (int): The number of times to run `wait_random`.
        max_delay (int): The maximum delay for `wait_random`.

    Returns:
        List[float]: A list of wait times for the completed tasks.
    """
    tasks= [wait_random(max_delay) for _ in range(n)]
    completed_delays = await asyncio.gather(*tasks)
    return completed_delays

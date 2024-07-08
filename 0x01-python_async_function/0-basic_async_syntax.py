#!/usr/bin/env python3
"""
The use of asyncio and random libraries to execute
an asynchronous function that awaits for
a random amount of time.
"""

import asyncio
import random


async def wait_random(max_delay=10):
    """
    Asynchronously waits for a random time.

    This coroutine waits for a random amount of time between 0
    and max_delay seconds, then returns the amount of time waited.

    Parameters:
    - max_delay (int, optional): The maximum delay time in seconds.
    Defaults to 10sec.

    Returns:
    - float: The actual delay time in seconds.
    """
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay

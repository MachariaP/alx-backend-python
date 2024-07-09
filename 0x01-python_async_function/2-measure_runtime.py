#!/usr/bin/env python3
"""
This module demonstrates how to measure the execution time of asynchronous
functions executed in parallel. It specifically measures the total runtime
of executing the `async_comprehension` function four times concurrently.
"""

import asyncio
import time
from typing import Callable

# Import wait_n from the previous file
wait_n = __import__('1-concurrent_coroutines').wait_n

def measure_time(n: int, max_delay: int) -> float:
    """
    Synchronously measures the total execution time for wait_n(n, max_delay),
    and returns total_time / n.

    Args:
        n (int): The number of times to run `wait_random`.
        max_delay (int): The maximum delay for `wait_random`.

    Returns:
        float: The average time per call.
    """
    start_time = time.time()

    # Define an inner asynchronous function to await wait_n
    async def async_wrapper():
        await wait_n(n, max_delay)

    # Run the asynchronous function using asyncio.run
    asyncio.run(async_wrapper())

    end_time = time.time()
    total_time = end_time - start_time
    return total_time / n

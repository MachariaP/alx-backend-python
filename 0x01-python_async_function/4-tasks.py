#!/usr/bin/env python3

"""
Module for managing asyncio tasks with random delays.
"""

import asyncio
from typing import List

task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    Executes `n` tasks with random delays up to `max_delay` and
    returns sorted results.

    Args:
        n (int): Number of tasks.
        max_delay (int): Maximum delay for each task.

    Returns:
        List[float]: Sorted delays from each task.
    """
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    completed_tasks = await asyncio.gather(*tasks)
    return sorted(completed_tasks)

#!/usr/bin/env python3
"""
Module provides functionality to create asyncio tasks that
execute with a random delay.
"""

import asyncio
from typing import Callable

# Import wait_random from the previous file
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
    Takes an integer max_delay and returns an asyncio.Task.

    Args:
        max_delay (int): The maximum delay before returning.

    Returns:
        asyncio.Task: A task that will complete after wait_random.
    """
    # Schedule the execution of wait_random using asyncio.create_task
    task = asyncio.create_task(wait_random(max_delay))
    return task

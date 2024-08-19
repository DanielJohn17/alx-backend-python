#!/usr/bin/env python3
'''Module with task_wait_n function'''
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''Executes multiple coroutines at the same time with async'''
    all_delays = []

    for _ in range(n):
        num = await task_wait_random(max_delay)
        all_delays.append(num)

    return sorted(all_delays)

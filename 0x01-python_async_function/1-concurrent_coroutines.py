#!/usr/bin/env python3
'''Module to execute multiple coroutines at the same time with async'''
import asyncio
from typing import List


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''Executes multiple coroutines at the same time with async'''
    all_delays = []

    for _ in range(n):
        num = await wait_random(max_delay)
        all_delays.append(num)

    return sorted(all_delays)

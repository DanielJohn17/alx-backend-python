#!/usr/bin/env python3
'''Module for Measure Runtime'''
import asyncio
from time import perf_counter


async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime():
    '''Measure Runtime'''
    start_time = perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = perf_counter()

    return end_time - start_time

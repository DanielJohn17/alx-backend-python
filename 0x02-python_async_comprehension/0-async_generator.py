#!/usr/bin/env python3
'''Module for Asynchronous Generator'''
import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    '''Asynchronous Generator'''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10

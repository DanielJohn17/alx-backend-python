#!/usr/bin/env python3
'''Module for Asynchronous Comprehension'''
from typing import List


async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    '''Asynchronous Comprehension'''
    return [num async for num in async_generator()]

#!/usr/bin/env python3
'''Type-annotated function to_kv that takes a string k and an int OR float v'''
from typing import Union, Tuple
import math


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''Type-annotated function to_kv that
        takes a string k and an int OR float v'''
    return (k, math.pow(v, 2))

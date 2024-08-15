#!/usr/bin/env python3
'''Module that holds a type-annotated function safely_get_value'''
from typing import Mapping, Any, Union, TypeVar


T = TypeVar('T')
Res = Union[Any, T]
Def = Union[T, None]


def safely_get_value(dct: Mapping, key: Any, default: Def = None) -> Res:
    '''Retrieves the value safely from a dictionary.'''
    if key in dct:
        return dct[key]
    else:
        return default

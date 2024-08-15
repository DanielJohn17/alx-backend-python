#!/usr/bin/env python3
'''Module that holds a type-annotated function safe_first_element'''
from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''Retrieves the first element of a sequence if it exists.'''
    if lst:
        return lst[0]
    else:
        return None

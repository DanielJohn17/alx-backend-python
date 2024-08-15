#!/usr/bin/env python3
'''Module that holds a type-annotated
    function element_length that takes a list'''
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''Type-annotated function element_length that takes a list input_list of
        strings and returns a list of tuples where each tuple’s first element
        is the string and the second element is the length of the string.'''
    return [(i, len(i)) for i in lst]

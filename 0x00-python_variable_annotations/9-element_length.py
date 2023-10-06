#!/usr/bin/env python3
"""type-annotated function"""
from typing import Iterable, List, Sequence, Tuple


def element_length(lst: Iterable) -> List[Tuple[Sequence, int]]:
    """ function parameters and return values with the appropriate types"""
    return [(i, len(i)) for i in lst]

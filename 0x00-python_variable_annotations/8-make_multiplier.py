#!/usr/bin/env python3
"""type-annotated function"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """takes a float multiplier as argument
    returns a function that multiplies a float by multiplier"""
    def multiply_by_multiplier(num: float) -> float:
        """takes a float num as argument
        returns the product of num and multiplier"""
        return num * multiplier
    return multiply_by_multiplier

#!/usr/bin/env python3
"""0. Async Generator"""


import asyncio


async def async_generator():
    """Yield a random number between 0 and 10"""
    import random
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)

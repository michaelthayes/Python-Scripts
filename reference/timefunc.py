# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:34:32 2021

@author: Mike
"""


# https://www.kdnuggets.com/2021/03/simple-way-time-code-python.html

"""Build the timefunc decorator."""

import time
import functools
import random


def timefunc(func):
    """timefunc's doc"""

    @functools.wraps(func)
    def time_closure(*args, **kwargs):
        """time_wrapper's doc string"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        time_elapsed = time.perf_counter() - start
        print(f"Function: {func.__name__}, Time: {time_elapsed}")
        return result

    return time_closure


@timefunc
def single_thread(inputs):
    """
    Compute single threaded.
    """
    return [x*2 for x in inputs]


if __name__ == "__main__":

    demo_inputs = [random.randint(1, 100) for _ in range(10_000)]

    single_thread(demo_inputs)
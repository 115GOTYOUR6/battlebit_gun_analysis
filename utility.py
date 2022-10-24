import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Function '{func.__name__}' took {end - start}s")
        return ret
    return wrapper

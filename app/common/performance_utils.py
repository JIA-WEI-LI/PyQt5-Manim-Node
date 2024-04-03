import time
from functools import wraps

def calculate_time(show_time=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if show_time:
                print(f"Function::{func.__name__} executed in --- {execution_time} --- seconds")
            return result
        return wrapper
    return decorator
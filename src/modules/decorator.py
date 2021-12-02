# -*- coding: utf-8 -*-
"""
z
"""
# import constants as C
from functools import wraps
from .display import Display

display = Display()


def stages(desc):
    # message = '-'*9 + '<' + desc + '>' + '-'*9
    # display.info(message)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # display.step(desc)
            # results = func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


# def switcher(func):
#     def wrapper(*args, **kwargs):
#         if C.LOG_ON:
#             return func(*args, **kwargs)
#         else:
#             pass
#     return wrapper




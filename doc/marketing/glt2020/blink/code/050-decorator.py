#!/usr/bin/python

import math


def debug(fun):
    def wrapper(*args, **kwargs):
        print('args:', args, ', kwargs:', kwargs)
        return fun(*args, **kwargs)
    return wrapper

@debug
def hypotenuse(a, b):
    return math.sqrt(a**2 + b**2)

print(hypotenuse(3, 4))

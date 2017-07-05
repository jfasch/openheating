#!/usr/bin/python3

import numpy

a = numpy.array([1, 2, 2, 3, 3.4, 4, 3.6, 4.5], dtype=numpy.float)

print(numpy.gradient(a))

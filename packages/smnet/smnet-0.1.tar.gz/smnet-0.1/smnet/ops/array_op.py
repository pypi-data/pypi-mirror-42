# -----------------
# SMNet
# Written by smarsu
# -----------------
"""The operation aboat np.array()"""

import numpy as np


def matmul(a, b):
    """Matrix product of two arrays.
    
    TODO(smarsu): Check the validity of array @a and @b, such as type and shape.
    """
    # np.matmul will raise error in some special cases.
    return np.matmul(a, b)


def add(a, b):
    """TODO(smarsu): Separate bias_add() from add()."""
    return a + b


def multiply(a, b):
    return a * b


def divide(a, b):
    # // is the absolute division.
    return a / b


def sigmoid(a):
    """It will not go to np.nan.
    TODO(smarsu): Solve RuntimeWarning: overflow encountered in exp
    """
    return 1 / (1 + np.exp(-a))


def tanh(a):
    """Deformation from $(e(x) - e(-x)) / (e(x) + e(-x))
    """
    return 1 - 2 / (np.exp(2 * a) + 1)
    return -1 + 2 / (1 + np.exp(-2 * a))

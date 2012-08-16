"""reginergine"""

import numpy as np


def ratio(arr):
    """Returns a matrix whose elements are the ratios of the input's
    elements.  This is specifically to be used on the 0-dimensional
    array of the singular values."""
    
    # Figure out a way to make this work for non-integers...np.float
    # doesn't work
    ratios = np.zeros((len(arr)-1,))
    for i in range(len(arr)-1):
        ratios[i-1] = (arr[i-1]/arr[i])
    return ratios[:-1]


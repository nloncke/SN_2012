"""Converts supernova data in a file to an array
format.  Splits all data into an array of the day #s, wavelength values,
and flux data per day. Plots the flux values vs. wavelength for any
given day."""

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np

def plotcoeffs(coeffs, x_axis=None, y_axis=None, ext='pdf'):
    """Generates plots for all of the coordinates against each other
    and saves them in the format 'c{a}-c{b}.png'."""
# FYI: This function doesn't really work yet...  We need more
# troubleshooting and Gabe-asking

    i = 0
    if x_axis is not None and y_axis is None:
        while i < len(coeffs) and i!=x_axis:
            plt.plot(coeffs[x_axis],coeffs[i], 'o')
            plt.savefig('c{0}-c{1}.{2}'.format(x_axis, i, ext))
            plt.close()
            i += 1
    j = 0
    if y_axis is not None and x_axis is None:
        while j < len(coeffs) and j!=y_axis:
            plt.plot(coeffs[j],coeffs[y_axis], 'o')
            plt.savefig('c{0}-c{1}.{2}'.format(j, y_axis))
            plt.close()
            j += 1
    (i,j) = (0,0)
    if x_axis is None and y_axis is None:
        while i < len(coeffs):
            if j < len(coeffs):
                if i!=j:
                    plt.plot(coeffs[i],coeffs[j], 'o')
                    plt.savefig('c{0}-c{1}.png'.format(i, j))
                    plt.close()
                    j += 1
                else:
                    j += 1
            else:
                j = 0
                i += 1
    return 'Figures saved!'

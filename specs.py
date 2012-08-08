"""This module holds our most fundamental functions for extracting
spectral data from a file and plotting relevant information without
really modifying the data."""

import numpy as np
import matplotlib.pyplot as plt


def process_data(filename):
    """Converts raw column data from a file into arrays.  For our
    purposes, we want to extract an array for day numbers,
    wavelengths, and flux values, so we've sliced the arrays and given them
    suggestive names.  
    """

    file_arr = np.genfromtxt(filename)

    dayarr = np.unique(file_arr[:, 0])
    lams = np.unique(file_arr[:, 1]) 
    specs = file_arr[:, 2].reshape((len(dayarr),len(lams)))

    return dayarr, lams, specs


def day_idx(day,dayarr):
    """Returns the index number of the input day relative to dayarr.
    """

    idx = np.where(dayarr==day)[0][0]
    return idx


# Also, two other ways to do it:

## (y==day).tolist().index(True)

## minday = dayarr[0]
## idx_list= []
    ## for entry in dayarr:
    ## index = entry - minday
    ## index = np.array()
# return index


def plotspec(day, dayarr, lams, specs, display=True, save=False, ext='pdf'):
    """Plots flux values vs. wavelength for a specified day value (not
    an index number.
    """

    xvals = lams
    yvals = specs[day_idx(day, dayarr),:]
    title = 'Day {0:+04d}'.format(day)

    plt.plot(xvals,yvals)
    plt.xlabel(r'$\lambda$')    
    plt.ylabel(r'$f(\lambda)$')
    plt.title(title)

    if display:
        plt.show()

    if save:
        outfile = 'day{0:+04}.{1}'.format(day, ext)
        plt.savefig(outfile)
    else:
        outfile = None

    return outfile


def specplotter(dayarr, lams, specs, ext='pdf'):
    """Function factory that produces plotter_func, a function that
    takes in a day and plots the spectrum for that day.
    """
    def plotter_func(day):
        return plotspec(day, dayarr, lams, specs, ext)
    return plotter_func


def filespecplotter(filename, ext='pdf'):
    """'Plotting function for spectra in {0}'.format(filename)"""

    dayarr, lams, specs = process_data(filename)
    return specplotter(dayarr, lams, specs, ext)


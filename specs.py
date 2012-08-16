"""This module holds our most fundamental functions for extracting
spectral data from a file and plotting relevant information without
really modifying the data."""

import numpy as np
import matplotlib.pyplot as plt


def process_data(filename):
    """Converts file with astronomical data into three arrays: an
    array of the epochs, the wavelengths, and the fluxes.  This only
    works with the Hsiao file.
    """

    file_arr = np.genfromtxt(filename)

    dayarr = np.unique(file_arr[:, 0])
    lams = np.unique(file_arr[:, 1]) 
    specs = file_arr[:, 2].reshape((len(dayarr),len(lams)))

    return dayarr, lams, specs


def day_idx(day,dayarr):
    """Returns the index number of the input day relative to the array
    of days.
    """

    idx = np.where(dayarr==day)[0][0]
    return idx
        

def plotspec(day, dayarr, lams, specs, display=True, save=False, ext='pdf'):
    """Plots flux values (or flams :D) vs. wavelength for a specified day (not
    an index number).
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
    """'Plotting function for spectra in input file."""

    dayarr, lams, specs = process_data(filename)
    return specplotter(dayarr, lams, specs, ext)

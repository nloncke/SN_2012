"""Converts supernova data in a file to an array
format.  Splits all data into an array of the day #s, wavelength values,
and flux data per day. Plots the flux values vs. wavelength for any
given day."""

import matplotlib.mlab
import matplotlib.pyplot as plt
import numpy as np

def process_data(filename):
    """Converts raw data from a file into three arrays..."""

    file_arr = np.genfromtxt(filename)

## Note to self: these are not separate arrays yet!!!  They are only
## pointers and have the same base as file_arr.  Potential source of
## confusion...
    dayarr = np.unique(file_arr[:, 0]) ## This array holds all the day
                                ## numbers in increasing order
                                ## (starting negative through zero, to
                                ## the positive
    lams = np.unique(file_arr[:, 1]) ## All the wavelengths
                                ## values, non-repeating
    specs = file_arr[:, 2].reshape((len(dayarr),len(lams))) ## All the
                                ## spectra values per day in order of
                                ## increasing wavelength
    return dayarr, lams, specs


def whiten(arr):
    """Given an array, calculate the mean by columns.  Return the mean
    matrix and then the zero-meaned matrix."""
    
    col_avg = np.zeros(arr.shape)
    for i in range(len(arr)):
        col_avg[i] = np.mean(arr, axis=0)
    whitened_arr = arr - col_avg

    return col_avg, whitened_arr


def day_idx(day,dayarr):
    """Prints the index number of the input day in dayarr.  E.g. '-15'
    yields '5' or something like that."""
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


def plotspec(day, dayarr, lams, specs, display=True, save=False, ext='.pdf'):
    """Plots flux values vs. wavelength for a specified day"""

    # day_idx(dayarr,day)
    # idx = np.where(dayarr==day)[0][0]
    # title = 'Day ' + str(day)

    xvals = lams
    yvals = specs[day_idx(day, dayarr),:]
    title = 'Day {0:+04d}'.format(day)

    specgraph = plt.plot(xvals,yvals)
    
    plt.xlabel(r'$\lambda$')    
    plt.ylabel(r'$f(\lambda)$')
    plt.title(title)

    plt.show()
    plt.savefig('day{0:+04}{1}'.format(day, ext))
    
    return specgraph


def specplotter(dayarr, lams, specs, ext='.pdf'):
    """Function factory that produces plotter_func, a function that
    takes in just the day and plots everything"""
    def plotter_func(day):
        return plotspec(day, dayarr, lams, specs, ext)
    return plotter_func

def filespecplotter(filename, ext='.pdf'):
    """Plotting function for spectra in {0}.""".format(filename)

    dayarr, lams, specs = process_data(filename)
    return specplotter(dayarr, lams, specs, ext)

def svd_specs(filename):
    """The ultimate function!  All you have to do is enter a filename
    that you want to SVD the data of and poof, out comes U S V, after
    the main data matrix has been 'whitened'."""

    def call_processdata(filename):
        return process_data(filename)
    days, lams, specs = process_data(filename)
    zspecs = mlab.center_matrix(specs)
    U, S, V = np.linalg.svd(zspecs)
    return U, S, V

# def pcs_specs(filename):
#     def call_processdata(filename):
#         return process_data(filename)
#     days, lams, specs = process_data(filename)
#     plt.PCA

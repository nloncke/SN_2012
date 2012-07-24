"""Converts supernova data in a file to an array
format.  Splits all data into an array of the day #s, wavelength values,
and flux data per day. Plots the flux values vs. wavelength for any
given day."""

import matplotlib.mlab as mlab
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

def ratio(arr):
    """Returns a matrix whose elements are the ratios of the input's
    elements.  This is specifically to be used on the 0-dimensional
    array of the singular values."""
    
    ratios = np.zeros((len(arr)-1,))
    for i in range(len(arr)-1):
        ratios[i-1] = (arr[i-1]/arr[i])
    return ratios[:-1]

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

def residuals(whitespecs, reconspecs):
    """This function returns the residual percent error of an
    n-dimensional basis approximation of our original specs data."""

    percent_error = np.abs(np.abs(whitespecs - reconspecs)/whitespecs)
    tol = percent_error[np.unravel_index(np.argmax(percent_error), percent_error.shape)]
    avg_err = np.average(percent_error)

    return percent_error, avg_err, tol

def tribute(specs, n):
    """Because I'm sooo sloow on the interpreter, I'm writing us a
    funtion that will cut and reconstruct an our data from an
    n-dimensional basis.  Here goes!"""

    U, singvals, Vt = np.linalg.svd(whiten(specs)[1])
    Vt = np.vstack((np.mean(specs, axis=0), Vt))
    Ucut = U.T[n].T
    S = np.zeros((n, n))
    S[:] = np.diag(singvals[:n])
    Vtcut = Vt[n]
    coeffs = hstack((np.ones((1, len(U))), np.dot(U,S)))
    tribute = coeffs[n] * Vtcut
    
    return tribute 

def everything(specs):
    """Produces a three-dimensional matrix.
    axis0=n, where n is the number of basis vectors used in the
    reconstruction
    axis1=day, the day # of the flux data over all wavelengths
    (i.e., corresponding to a row of specs)
    axis2=flux data"""
    
    everything = np.zeros((len(specs), len(specs), specs.shape[1]))
    everything[0,:,:] = whiten(specs)[0]
    for n in range(1, len(specs)):
        X = reconstruct(specs, n)
        everything[n,:,:] = X



def resid_by_n(specs, day):
    """Returns a plot of the residuals for a given day over all n's, where n is the
    number of principal components used to recreate the data."""
    
    recons = np.zeros(len(specs), specs.shape)
    
    for n in range(len(specs)):
        X = reconstruct(specs, n+1)
        residuals[] = residuals(whiten(specs)[1], X)[2]

def reconmat(specs, n):

    U, singvals, Vt = np.linalg.svd(whiten(specs)[1])
    Ucut = U.T[:n].T
    S = np.zeros((n, n))
    S[:] = np.diag(singvals[:n])
    Vtcut = Vt[:n]
    new_data = np.dot(np.dot(Ucut,S), Vtcut)

    return new_data


# def pcs_specs(filename):
#     def call_processdata(filename):
#         return process_data(filename)
#     days, lams, specs = process_data(filename)
#     plt.PCA

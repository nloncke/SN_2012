"""This module holds all of our residual related functions."""

import numpy as np
import matplotlib.pyplot as plt

import specs
import pca

def residuals(act, est, scale=None):
    """Returns the residual matrix of the original data and
    reconstructed data.
    """
    act = np.array(act, dtype=float)
    if scale is None:
        scale = act
    return (act - est)/scale


def maxresidual(residuals, axis=None):
    """Finds the maximum residual from the input array.  NB: doesn't
    tell us whether it is negative or positive.
    """

    return np.amax(np.abs(residuals), axis)
    

def graphresiduals(day, N, resids, lams, dayarr, style='o-',
                   save=False, ext='pdf'):
    """Graphs the residuals by the wavelengths for a given day and
    an N-degree approximation for that day.
    """

    dayidx = specs.day_idx(day, dayarr)
    plt.semilogy(lams, np.abs(resids[N, dayidx, :]), style)

    plt.xlabel(r'$\lambda$')
    plt.ylabel(r'$log(Residuals)$')
    plt.title('{0}th order Residuals for Day {1}'.format(N, day))
    plt.show()

    if save:
        plt.savefig('day{0}-n{1}.{2}'.format(day, n, ext))
        print 'Figure saved!'

    return None


def graphmaxresiduals(resids, dayarr, day=None, display=True, save=False,
    style='o-', ext='pdf'):
    """Returns a plot of the maximum residuals over all Ns for a
    given day, or all days, if left unspecified, where N
    is the number of principal components used to recreate the
    data.
    """
    maxbyday = maxresidual(resids, axis=2)

    if day is not None:
        dayidx = specs.day_idx(day, dayarr)
        yvals = maxbyday[:, dayidx]
        daystr = 'Day {0}'.format(day)
        filename = 'day{0}alln'.format(day)
    else:
        daystr = 'All Days'
        yvals = np.amax(maxbyday, axis=1)
        filename = 'alldaysalln'

    plt.semilogy(yvals, style)
    plt.title('Maximum Residuals over all N for {0}'.format(daystr))
    plt.xlabel('N')
    plt.ylabel('Maximum residuals')
    
    if display==True:
        plt.show()

    if save==True:
        plt.savefig('{0}.{1}'.format(filename, ext))

    return np.array(yvals)

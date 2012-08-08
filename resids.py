"""This module holds all of our residual related functions."""

import numpy as np
import matplotlib.pyplot as plt

import specs
import pca

def residuals(act, est):
    """Returns the residual matrix of the original data and
    reconstructed data.
    """
    # act = np.array(act, dtype=float)
    return (act - est)/act


def maxresidual(residuals, axis=None):
    """Finds the maximum residual from the input array.  NB: doesn't
    tell us whether it is negative or positive.
    """
    # If you care about signed error, then uncomment this:
    # indices = np.unravel_index(np.argmax(np.abs(residuals), axis),
    #                            residuals.shape)
    return np.amax(np.abs(residuals), axis)
    

def graphresiduals(day, N, resids, lams, dayarr, style='o-',
                   save=True, ext='pdf'):
    """Produces a graph of the residuals by the wavelengths for a
    given day and a given n-degree approximation of the data.
    """

    dayidx = specs.day_idx(day, dayarr)

    plt.semilogy(lams, np.abs(resids[N, dayidx, :]), style)
    plt.title('{0}th Order Resids for Day{1}'.format(N, day))
    plt.xlabel(r'log($\lambda$)')
    plt.ylabel(r'log(Residuals)')
    plt.show()

    if save:
        plt.savefig('day{0}_n{1}.{2}'.format(day, n, ext))
        print 'Figure saved!'

    return


def graphmaxresiduals(resids, dayarr, day=None, display=True, save=False,
    style='o-', ext='pdf'):
    """If day is specified, returns a plot of the maximum residuals
    for a given day over all n's, where n is the number of principal
    components used to recreate the data. If day is not specified,
    produces a plot of the maximum residual for an nth order
    approximation as a function of n.
    """
    maxbyday = maxresidual(resids, axis=2)

    if day is not None:
        day = specs.day_idx(day, dayarr)
        yvals = maxbyday[:, day]
        daystr = 'Day {0}'.format(day)
        filename = 'day{0}resids'.format(day)
    else:
        daystr = 'All Days'
        yvals = np.amax(maxbyday, axis=1)
        filename = 'alldaysalln'

    plt.semilogy(yvals, style)
    plt.title('Maximum Residuals over all N for {0}'.format(daystr))
    plt.xlabel('N')
    plt.ylabel('Maximum residuals')
    
    if display:
        plt.show()

    if save:
        plt.savefig('{0}.{1}'.format(filename, ext))

    return np.array(yvals)



# def allresids_by_n(resids, dayarr, ext='pdf'):
#     """Maximum residual over all days vs. n-degree approximation."""
    
    
#     # max_resids = maxresidual(np.array(max_resids), axis=0)

#     # plt.plot(range(len(spex)), np.log(np.abs(max_resids)), 'o-')
#     # plt.title('Maximum residual vs. Approximation Order N')
#     # plt.xlabel('N')
#     # plt.ylabel('log(maximum residual)')
#     # plt.savefig('maxresids.{0}'.format(ext))
    
#     return np.array(max_resids)

"""This module holds all of our residual related functions."""

import pca
import numpy as np
import matplotlib.pyplot as plt


def residuals(act, est):
    """This function returns the residual percent error of an
    n-dimensional basis approximation of our original specs data.
    """

    return (act - est)/act

def maxresiduals(residuals, axis=None):
    """Finds the maximum percent error and not just the absolute
    value.
    """
    indices = np.unravel_index(np.argmax(np.abs(residuals), axis), 
                               residuals.shape)

    return residuals[indices]
    

def resids_by_lams(specs, day, n, save=True, ext='pdf'):
    """Produces a graph of the residuals by the wavelengths for a
    given day and a given n-degree approximation of the data.
    """

    whitespecs = pca.whiten(specs)[1]
    singvals, coeffs, basisvecs = pca.pca(specs)
    allmats = pca.pca_partial_sums(coeffs, basisvecs)
    resids = residuals(specs, allmats[n,:,:])

    plt.plot(np.arange(1000, 25010, 10), resids[day,:], 'o-')
    plt.title('Day{0}-N{1} Residuals'.format(day, n))
    plt.xlabel(r'$\lambda$')
    plt.ylabel('Max residuals')
    plt.show()

    if save==True:
        plt.savefig('day{0}-n{1}.{2}'.format(day, n, ext))
        print 'Figure saved!'

    return


def resids_by_n(specs, day, save=True, ext='pdf'):
    """Returns a plot of the maximum residuals for a given day over
    all n's, where n is the number of principal components used to
    recreate the data.
    """
    
    resids = []
    singvals, coeffs, basisvecs = pca.pca(specs)
    allmats = pca.pca_partial_sums(coeffs, basisvecs)

    for n in range(len(specs)):
        resids.append(maxresiduals(residuals(specs[day],
                                    allmats[n,day,:])))
    plt.plot(range(len(specs)), resids, 'o-')
    plt.title('Day {0} Residuals'.format(day))
    plt.xlabel('N')
    plt.ylabel('Maximum residuals')
    plt.show()

    if save==True:
        plt.savefig('day{0}_resids.{1}'.format(day, ext))

    return np.array(resids)

def maxresids_by_n(specs, ext='pdf'):
    """Maximum residual over all days vs. n-degree approximation."""
    
    max_resids = []
    singvals, coeffs, basisvecs = pca.pca(specs)
    allmats = pca.pca_partial_sums(coeffs, basisvecs)
    for day in range(len(specs)):
        max_resids.append(resids_by_n(specs, day, save=False))
    max_resids = maxresiduals(np.array(max_resids), axis=0)

    plt.plot(range(len(specs)), max_resids, 'o-')
    plt.title('Maximum residual vs. Approximation Order N')
    plt.xlabel('N')
    plt.ylabel('Maximum residual')
    plt.savefig('maxresids.{0}'.format(ext))
    
    return


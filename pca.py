import numpy as np

def whiten(arr):
    """Given an array, calculate the mean by columns.  Return the mean
    vector (row) and then the zero-meaned matrix.
    """
    
    meandata = np.mean(arr, axis=0)
    whitened_arr = arr[:,] - meandata

    return meandata, whitened_arr

def pca(arr):
    """Enter the array of the data you want to PCA and return singvals
    (an array of the singular values from SVD), coeffs, and bigVt.
    """

    arrmean, whitened_arr = whiten(arr)
    U, singvals, Vt = np.linalg.svd(whitened_arr)
    
    S = np.zeros(arr.shape)
    numsings = len(singvals)
    S[:numsings, :numsings] = np.diag(singvals)

    coeffs = np.hstack((np.ones((len(U),1)), np.dot(U,S)))
    basisvecs = np.vstack((arrmean, Vt))

    return singvals, coeffs, basisvecs

def nth_pca_term(n, coeffs, basisvecs):
    """Because I'm sooo sloow on the interpreter, I'm writing us a
    funtion that will return the constribution of the nth vector of
    our PCA'd basis.  Not all of the vectors from one through n, only
    the nth.  **Note that the 0th vector is now the mean, and is
    weighted by ones in the coefficient matrix (coeffs).**
    """

    coeffs_n = coeffs[:,n].reshape((len(coeffs),1))
    return coeffs_n * basisvecs[n]
    

def pca_partial_sums(coeffs, basisvecs):
    """Produces a three-dimensional matrix.  axis0=n, where n is the
    number of basis vectors used in the reconstruction axis1=day, the
    day # of the flux data over all wavelengths (i.e., corresponding
    to a row of specs) axis2=flux data.
    """
    
    result_shape = (coeffs.shape[0],) + coeffs[:,1:].shape
    result = np.zeros(result_shape)
    result[0,:,:] = nth_pca_term(0, coeffs, basisvecs)
    for n in range(1, len(result)):
        result[n,:,:] = (result[n-1,:,:] +
                         nth_pca_term(n, coeffs, basisvecs))

    return result

# def reconmat(specs, n):
#     """Kind of superfluous function that we're keeping so that we can
#     check stuff on the interpreter.  Basically, it returns the
#     re-creation of the data using up to n vectors.  Our replacement
#     function mk.tribute(specs, n) just gives us the contribution of the nth vector."""

#     U, singvals, Vt = np.linalg.svd(whiten(specs)[1])
#     Ucut = U.T[:n].T
#     S = np.zeros((n, n))
#     S[:] = np.diag(singvals[:n])
#     Vtcut = Vt[:n]
#     new_data = np.dot(np.dot(Ucut,S), Vtcut)

#     return new_data

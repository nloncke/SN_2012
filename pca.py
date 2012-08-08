import numpy as np

def whiten(data):
    """Given an array, calculate the mean by columns.  Return the mean
    vector (row) and then the zero-meaned matrix.
    """
    
    meandata = np.mean(data, axis=0)
    whiteneddata = data[:,] - meandata

    return meandata, whiteneddata

def pca(data):
    """PCA from SVD, returns the singular values, the coefficients (in
    rows, with a column of ones at the beginning), and the basis
    vectors (also in rows, with the mean stacked on top).
    """

    meandata, whitedata = whiten(data)
    U, singvals, Vt = np.linalg.svd(whitedata)
    
    S = np.zeros(data.shape)
    numsings = len(singvals)
    S[:numsings, :numsings] = np.diag(singvals)

    coeffs = np.hstack((np.ones((len(U),1)), np.dot(U,S)))
    basisvectors = np.vstack((meandata, Vt))

    return singvals, coeffs, basisvecs

def nthpcaterm(N, coeffs, basisvectors):
    """Returns the Nth term of the partial sum from our PCA'd basis.
    """

    is_coeffs_1D = (len(coeffs.shape) == 1)
    if is_coeffs_1D:
        coeffs = coeffs.reshape((1, len(coeffs)))
        # len(coeffs) will be 1 if "if"-body executed
    coeffs_n = coeffs[:,N].reshape((len(coeffs),1))
    # Previous line makes broadcast rules work for next line
    result = coeffs_n * basisvectors[N]
    if is_coeffs_1D:
        result.resize((result.shape[1],))
    return result
    

def partial_sums(coeffs, basisvectors):
    """Input: Coeffs (in rows), Basisvectors (in rows). Output:
    three-dimensional matrix of partial sums. If coeffs is J x M, and
    basisvectors is M x N, then the result will be M x J x N
    """

    result_shape = (len(basisvectors), len(coeffs), len(basisvectors.T))
    result = np.zeros(result_shape)
    result[0,:,:] = nthpcaterm(0, coeffs, basisvectors)
    for n in range(1, len(result)):
        result[n,:,:] = (result[n-1,:,:] +
                         nthpcaterm(n, coeffs, basisvectors))
    
    return result


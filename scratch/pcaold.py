"""Faciilitates the process of interpreting our PCA data that we get
from np.linalg.svd"""

import ~/Documents/summerprog/hsiao_spectra/pca.py as pca
import numpy as np

def recover_basis(data):
    """This function takes in your data matrix and returns the
    eigenvectors of the associated variance matrix (or covariance
    matrix???)  After this you must manually slice the array to
    include the relevant vectors according to the singular values."""
    
    cent_data = py.center_matrix(data)
    xTx = np.dot(cent_data.T, cent_data)
    new_basis = np.array(np.linalg.eig(xTx)[1])

    return new_basis



def encode_data(data):
    """This function takes in your data matrix and its
    dimension-reduced basis and displays the projection of the
    original data on said basis in lower-dimensional space."""

    cent_data = pca.whiten(data)[1]
    new_basis = recover_basis(data)
    Y = np.dot(cent_data, new_basis)

    return np.array(Y)



def reconstruct_data(data, new_basis):
    """Given the reduced-dimension basis and the data with repsect to
    that new basis, we can recover the original centered data
    matrix.  Unfortunately"""

    Y = encode_data(data, new_basis)
    recon_data = mp.mult(Y, new_basis.T)

    return np.array(recon_data)


def whiten(mtx):
    """Calculates the average of the columns of a matrix and then
    subtracts..."""

    whitened_ellipse = []
    i = 0
    while i < 3:
        mtx_mean = np.mean(mtx.T[i])
        whitened_ellipse = whitened_ellipse.append(mtx.T[i] - np.mean(mtx.T[i], out=array))
        i+1
    return whitened_ellipse

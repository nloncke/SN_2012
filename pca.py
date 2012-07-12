"""Faciilitates the process of interpreting our PCA data that we get
from np.linalg.svd"""

import pylab as py
import numpy as np
import multiply as mp

def recover_basis(data):
    """This function takes in your data matrix and returns the
    eigenvectors of the associated variance matrix (or covariance
    matrix???)  After this you must manually slice the array to
    include the relevant vectors according to the singular values."""
    
    cent_data = py.center_matrix(data)
    xTx = mp.mult(cent_data.T,cent_data)
    new_basis = np.array(np.linalg.eig(xTx)[1])

    return new_basis



def encode_data(data, new_basis):
    """This function takes in your data matrix and its
    dimension-reduced basis and displays the projection of the
    original data on said basis in lower-dimensional space."""

    cent_data = py.center_matrix(data)
    new_basis = recover_basis(data)
    Y = mp.mult(cent_data, new_basis)

    return Y



def reconstruct_data(data, new_basis):
    """Given the reduced-dimension basis and the data with repsect to
    that new basis, we can recover the original centered data
    matrix.  Unfortunately"""

    Y = encode_data(data, new_basis)
    recon_data = mp.mult(Y, new_basis.T)

    return np.array(recon_data)

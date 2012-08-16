"""Gives you coordinate information about an ellipse with
user-specified axes."""

import numpy as np
# import matplotlib.pyplot as plt

def polar_ellipse(x_axis, y_axis, theta):
    """Returns the coordinates of a specified point on an ellipse in
    polar form. Note that theta is in radians."""

    r = (x_axis * y_axis) / np.sqrt((y_axis * np.cos(theta))**2 + (x_axis
    * np.sin(theta))**2)
    return theta, r


def rect_ellipse(x_axis, y_axis, theta):
    """Returns the coordinates of a specified point on an ellipse in
    rectangular coords. Note that theta is still in radians."""

    theta, r = polar_ellipse(x_axis, y_axis, theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def deg_ellipse(x_axis, y_axis, degrees):
    """Operates in terms of degrees instead of radians.  And spits out
    rectangular coordinates."""

    theta = (degrees/360) * (2 * np.pi)
    x, y = rect_ellipse(x_axis, y_axis, theta)
    return x, y

def ellipse_pts(x_axis, y_axis, step=np.pi/6):
    """Returns a list of points on an ellipse of semimajor/semiminor
    axes of length x_axis and y_axis in increments of the given step
    size."""

    degrees = np.arange(0, 2*np.pi, step)
    rect_coords = rect_ellipse(x_axis, y_axis, degrees)
    rect_coords = zip(rect_coords[0], rect_coords[1])
    return np.array(rect_coords)

def lincomb(coeffs, u, v):
    """Creates linear combinations of u and v with coefficients
    arranged in the nx2 array coeffs."""

    return np.array([c1*u + c2*v for c1,c2 in coeffs])


    # k=0
    # vectors=[]
    # while k < len(coeffs):
    #     y = coeffs[k][0]*u + coeffs[k][1]*v
    #     y = y.tolist()
    #     vectors.append(y)
    #     k +=1
    # return np.array(vectors)


def make_int(arr2D):
    # rownums, colnums = range(len(arr)), range(len(arr[0]))
    rownums, colnums = arr.shape
    for i in rownums:
        for j in colnums:
            arr[i][j] = int(arr[i][j])
    return arr

def vlen(vector):
    """Calculates the Euclidean length of any n-Dimensional vector."""
    
    v_sq = np.array(vector)**2
    v_sq_sum = v_sq.sum()
    vlen = np.sqrt(v_sq_sum)
    return vlen

def normalize(vector):
    """Using vlen() we normalize an input vector"""

    length = vlen(vector)
    unit_v = vector/length
    return unit_v

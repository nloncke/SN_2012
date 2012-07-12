"""Gives you coordinate information about an ellipse with user-specified
axes."""

import pylab as py
import numpy as np

def polar_ellipse(x_axis, y_axis, theta):
    """Returns the coordinates of a specified point on an ellipse in
    polar form. Note that theta is in radians."""

    r = (x_axis * y_axis) / py.sqrt((y_axis * py.cos(theta))**2 + (x_axis
    * py.sin(theta))**2)
    return theta, r


def rect_ellipse(x_axis, y_axis, theta):
    """Returns the coordinates of a specified point on an ellipse in
    rectangular coords. Note that theta is still in radians."""

    theta, r = polar_ellipse(x_axis, y_axis, theta)
    x = r * py.cos(theta)
    y = r * py.sin(theta)
    return x, y

def deg_ellipse(x_axis, y_axis, degrees):
    """Operates in terms of degrees instead of radians.  And spits out
    rectangular coordinates."""

    theta = (degrees/360) * (2 * py.pi)
    x, y = rect_ellipse(x_axis, y_axis, theta)
    return x, y

def ellipse_pts(x_axis, y_axis, step=py.pi/6):
    """Returns a list of points on an ellipse of semimajor/semiminor
    axes of length x_axis and y_axis in increments of the given step
    size."""

    degrees = np.arange(0, 2*py.pi, step)
    rect_coords = rect_ellipse(x_axis, y_axis, degrees)
    rect_coords = zip(rect_coords[0], rect_coords[1])
    return np.array(rect_coords)

def lincomb(waa, u, v):

    k=0
    vectors=[]
    while k < 10:
        y = waa[k][0]*u + waa[k][1]*v
        y = y.tolist()
        vectors.append(y)
        k +=1
    return np.array(vectors)


def make_int(array):
    rownums, colnums = range(len(array)), range(len(array[0]))
    for i in rownums:
        for j in colnums:
            array[i][j] = int(array[i][j])
    return array

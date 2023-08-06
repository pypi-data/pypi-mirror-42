# Copyright (c) 2018, Matheus Boni Vicari, LeafProp Project
# All rights reserved.
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


__author__ = "Matheus Boni Vicari"
__copyright__ = "Copyright 2018, LeafProp Project"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "0.2"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"

import numpy as np
from numba import jit


@jit
def norm_to_zenith(norm_vec):

    """
    Calculates the (acute) angles between an array of normal vectors
    and a purerely vertical vector (0, 0, 1).

    Parameters
    ----------
    norm_vec: numpy.ndarray
        n x 3 array of normal vectors.

    Returns
    -------
    angle: numpy.ndarray
        n x 1 array of zenith angles from vertical vector.

    """

    # Initializing array of angles as nans.
    angles = np.full(norm_vec.shape[0], np.nan)

    # Iterating over normal vectors to calculate their angle from [0, 0, 1]
    # using the function angle. Stores results to array 'angles'.
    for i, nn in enumerate(norm_vec):
        angles[i] = vector_angles([0., 0., 1.], nn)

    return rad_to_degree(angles)


@jit
def norm_to_azimuth(norm_vec):

    """
    Calculates the azimuth angles between from an array of normal vectors.

    Parameters
    ----------
    norm_vec: numpy.ndarray
        n x 3 array of normal vectors.

    Returns
    -------
    angle: numpy.ndarray
        n x 1 array of azimuth angles from vertical vector.

    """

    # Initializing array of angles as nans.
    angles = np.full(norm_vec.shape[0], np.nan)
    
    # Iterating over normal vectors to calculate their azimuth angle 
    # using the equation atan2(y / x). This step also already converts from
    # radians to degrees.
    for i, nn in enumerate(norm_vec):
        angles[i] = np.arctan2(nn[1], nn[0]) * (180 / np.pi)

    # If angle is negative (left side of the y-axis), get the remaining angle
    # to 360 degrees.
    angles[angles < 0] = angles[angles < 0] + 360

    return angles


@jit
def vector_angles(vec1, vec2):

    """
    Calculates the angle between two vectors.

    Parameters
    ----------
    vec1: list or numpy.ndarray
        First vector.
    vec2: list or numpy.ndarray
        Second vector.

    Returns
    -------
    angle: float
        Angle between v1 and v2
    """

    angle = np.arccos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) *
                      np.linalg.norm(vec2)))

    return angle


@jit
def rad_to_degree(angles):

    """
    Converts an angle, or array of angles, from radians to degree.

    Parameters
    ----------
    angles: scalar or numpy.ndarray
        Angle or set of angles.

    Return
    ------
    degree_angles: scalar or numpy.ndarray
        Converted angle or set of angles.

    """

    return angles * (180 / np.pi)


@jit
def angle_from_zenith(angle):

    """
    Calculates the smallest angular distance of an angle from
    zenith.

    Parameters
    ----------
    angle: scalar
        Input angle value, in degrees.

    Returns
    -------
    angle_from_zenith: scalar
        Angular distance from zenith.

    """

    # Setting up angular zenith values.
    quad = np.array([0, 180, 360])

    # Calculates and returns shortest angular distance from zenith.
    return np.min(np.abs(angle - quad))

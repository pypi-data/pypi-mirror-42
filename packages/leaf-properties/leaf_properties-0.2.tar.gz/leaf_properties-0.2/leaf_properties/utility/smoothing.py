#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:10:05 2018

@author: matheus
"""

from numba import jit
from nnsearch import set_nbrs_rad
import numpy as np

@jit
def angles_majority(points, angles, radius, weighted=True):
    
    """
    Smooths inclination angles based on local neighborhoods.
    
    Parameters
    ----------
    points : array
        Set of coordinates for points in 3D space.
    angles : array
        Pointwise inclination angles.
    radius : float
        Radius value that defines local neighborhoods of points.
    weighted : bool
        Option to do a weighted average (True) or simple average (False).
        
    Returns
    -------
    new_angles : array
        Smoothed pointwise inclination angles

    """

    # Runs a radius Nearest Neighbors search on all points.
    distance, indices = set_nbrs_rad(points, points, radius)
    # Initializes an array of new angles.
    new_angles = np.zeros([angles.shape[0]])
    # Looping over pairs of neighborhood indices and distances.
    for i, (d, ids) in enumerate(zip(distance, indices)):
        # Check if it's supposed to run a weighted or simple average.
        if weighted is False:
            # Calculates mean angle value and sets it as current new angle.
            new_angles[i] = np.mean(angles[ids])

        elif weighted is True:
            # Mask non zero angles and average them as a function of  the
            # inverse distance. The closest to central point, the largest
            # is the weight.
            mask = angles[ids] != 0
            if np.sum(mask > 0):
                new_angles[i] = np.average(angles[ids][mask],
                                           weights=(1 / d[mask]))

    return new_angles
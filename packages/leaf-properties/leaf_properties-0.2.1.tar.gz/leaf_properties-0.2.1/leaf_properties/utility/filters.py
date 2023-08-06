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
from nnsearch import set_nbrs_rad, set_nbrs_knn
from scipy.spatial.distance import cdist
from numba import jit
from normals import point_normals


@jit
def dist_outlier(points, dist_threshold):
    
    """
    Check outliers in a set of points based on the mean distance (plus 
    standard deviation) between all pairs of points in the input array.
   
    
    Parameters
    ----------
    points : array
        Set of points to filter.
    dist_threshold : float
        Maximum valid distance.
        
    Returns
    -------
    mask : bool
        Returns True if no outlier is present in the set of input points and
        False otherwise.
    
    """

    # Calculating pairwise distance of all points agains each other.
    cd = cdist(points, points)

    # Obtaining only the lower triangle of the distance matrix to avoid
    # duplicate results/processing.
    xt, yt = np.tril_indices(cd.shape[0], -1)

    # Calculates mean distance 
    mean_cd = np.mean(cd[xt, yt])
    std_cd = np.std(cd[xt, yt])

    # Compare threshold distance with mean + std distance of pairs of points.
    mask = dist_threshold <= (mean_cd + std_cd)

    return mask


@jit
def evals_ratio(evals, eval_threshold=0.02):
    
    """
    Filters out a set of points based on how plane each points' neighborhood
    is. The planicity of a neighborhood is defined by its third eigenvalue,
    calculated from 3D space coordinates of its points.
    
    Parameters
    ----------
    evals : array
        Set of eigenvalues to filter.
    eval_threshold : float
        Maximum valid eigenvalue that defines a plane enough neighborhood.
        
    Returns
    -------
    mask : array
        Set of booleans. Returns True for indices of points that are plane
        enough according to eval_threshold and False otherwise.
        
    """
    
    # Calculates the ratio of eigenvalues along axis 1.
    ratio = (evals.T / np.sum(evals, axis=1)).T
    # As the smallest eigenvalue is the one that defines planicity, calculates
    # the minimum eigenvalue of each neighborhood and checks it agains the
    # threshold.
    t = np.min(ratio, axis=1)
    mask = t <= eval_threshold

    return mask


@jit
def neighbors_dist(points, knn, dist_threshold):
    
    """
    Filters a set of points based on the mean distance between neighboring
    points.
    
    Parameters
    ----------
    points : array
        Set of coordinates for points in 3D space.
    knn : int
        Number of neighbors that are used to define a neighborhood.
    dist_threshold : float
        Maximum mean distance.
        
    Results
    -------
    mask : bool
        Returns True if mean distance is smaller than dist_threshold and
        False otherwise.
        
    """
    
    # Running a k-Nearest Neighbors search and calculate mean distance of
    # neighboring sets of points.
    dist, ids = set_nbrs_knn(points, points, knn)
    dmean = np.mean(dist[:, 1:], axis=1)
    # Check if mean distance is smaller than dist_threshold.
    mask = dmean <= dist_threshold
    
    return mask

@jit
def raw_eval(points, knn, target_eval, eval_threshold):
    
    """
    Filters out a set of points based on an absolute threshold applied to
    a given eigenvalue calculated from sets of neighborhoods.

    Parameters
    ----------
    points : array
        Set of coordinates for points in 3D space.
    knn : int
        Number of neighbors that are used to define a neighborhood.
    target_eval : int
        Index of the eigenvalue to check. Valid values from 0 to 2.
    eval_threshold : float
        Maximum valid target eigenvalue.
        
    Returns
    -------
    mask : array
        Set of booleans. Returns True for indices of points that are plane
        enough according to eval_threshold and False otherwise.
    """

    # Calculates eigenvalues for every local neighborhood of points.
    _, _, evals = point_normals(points, knn)
    # Compares each neighborhood's target eigenvalue against threshold.
    mask = evals[:, target_eval] <= eval_threshold
    
    return mask

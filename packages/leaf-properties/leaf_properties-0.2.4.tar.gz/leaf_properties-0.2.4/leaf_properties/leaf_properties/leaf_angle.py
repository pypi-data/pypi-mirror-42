# Copyright (c) 2018-2019, Matheus Boni Vicari, leaf_properties
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
__copyright__ = "Copyright 2018-2019, LeafProp Project"
__credits__ = ["Matheus Boni Vicari"]
__license__ = "GPL3"
__version__ = "0.2.4"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"

import numpy as np
from ..utility.filters import evals_ratio
from ..utility.angles import norm_to_zenith, norm_to_azimuth
from ..utility.point_utils import remove_duplicates
from ..utility.normals import point_normals


def angles_from_points(points, knn, r_thres=0.1):
    
    """
    Calculates the zenith and azimuth angles of local neighborhoods in a
    point cloud.
    
    Parameters
    ----------
    points: array
        3D coordinates of leaf point cloud.
    knn: int
        Number of neighbors around each point in 'points'. This parameter
        sets each local neighborhood that will be used to calculate
        inclination angles.
    r_tresh: float
        Eigenvalue threshold to filter out local neighborhoords. A
        neighborhood with 'r' = 0 is completely flat. Values from 0 to 1.
        
    Returns
    -------
    zenith_angles: array
        Pointwise zenith angle values for each input point. Invalid points 
        (local neighborhood not flat enough) are set as 'nan'.
    azimuth_angles: array
        Pointwise azimuth angle values for each input point. Invalid points 
        (local neighborhood not flat enough) are set as 'nan'.
    
    """

    # Removing duplicate points.
    points = remove_duplicates(points[:, :3])

    # Calculating normal vectors and eigenvalues for each point.
    normal_vectors, cc, evals = point_normals(points, knn)

    # Masking normals based on eigenvalues ratios.
    filter_mask = evals_ratio(evals, r_thres)

    # Calculating absolute angles between each normal vector and horizontal
    # plane [0, 0, 1].
    zenith_angles = norm_to_zenith(normal_vectors)
    azimuth_angles = norm_to_azimuth(normal_vectors)

    # Setting bad quality points' angles (detected by filtering normals) to 0.
    zenith_angles[~filter_mask] = np.nan
    azimuth_angles[~filter_mask] = np.nan

    return zenith_angles, azimuth_angles

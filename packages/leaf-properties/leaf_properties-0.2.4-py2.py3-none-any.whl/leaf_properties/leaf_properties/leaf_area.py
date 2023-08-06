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
from leaf_geometry import triangulate_cloud
from leaf_geometry import triangulation_centroids
from ..utility.area import triangle_area
from ..utility.point_utils import remove_duplicates
from ..utility.filters import neighbors_dist


def area_from_points(points, knn, dist_thresh=0.007, smoothing_iterations=1):
    
    """
    Calculate the leaf area from a point cloud representation. A triangular
    mesh is generated as a representation for leaf surface and its total area
    is calculated.
    
    Parameters
    ----------
    points: array
        3D coordinates of leaf point cloud.
    knn: int
        Number of neighbors around each point in 'points'. This parameter
        sets each local neighborhood that will be used to generate the
        triangulated mesh.
    dist_thresh: float
        Maximum valid neighbors distance to use in triangulation.
    smoothing_iterations: int
        Number of iterations to smooth the triangulation vertices. The higher
        the smoother (caution advised, recommended between 1 and 3).
        
    Returns
    -------
    area: float
        Total leaf area in the same unit as the input coordinates (squared).
    
    """
    
    # Removing duplicate points (just in case) and generating a filter mask
    # based on mean neighbors distance.
    points = remove_duplicates(points[:, :3])
    dist_mask = neighbors_dist(points, knn, dist_thresh)
    
    # Initializing centroids from filtered points and smoothing it.
    centroids = points[dist_mask]
    centroids = triangulation_centroids(centroids, smoothing_iterations)
            
    # Triangulating smoothed centroids.
    vertices, tri = triangulate_cloud(centroids, 20, 0.1, 0.01)
    
    # Calculating triangulation area.
    tri_area = triangulation_area(vertices, tri)
    
    # Sums up all triangle areas.
    return np.nansum(tri_area)
    

def triangulation_area(points, tri):
    
    """
    Calculates triangle area from a triangular mesh.
    
    Parameters
    ----------
    points: array
        3D coordinates of point cloud.
    tri: array
        Triangular mesh indices.
        
    Returns
    -------
    area: array
        Area of each triangle in the mesh.
    
    """
    
    # Initializes area list and loop over each triangle. Uses 'triangle_area'
    # to calculate each triangle's area.
    area = []
    for t in tri:
        area.append(triangle_area(points[t].astype(float)))
        
    return area

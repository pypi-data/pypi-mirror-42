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
__version__ = "0.2.3"
__maintainer__ = "Matheus Boni Vicari"
__email__ = "matheus.boni.vicari@gmail.com"
__status__ = "Development"


import numpy as np
from utility.nnsearch import set_nbrs_knn
from utility.point_utils import remove_duplicates
from utility.normals import point_normals
from scipy.spatial import Delaunay
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist


def edge_length(t):
    
    """
    Calculates the lenght of edges in a triangle.
    
    Parameters
    ----------
    t: array
        Vertices coordinates of a 3D triangle. 
    
    Returns
    -------
    length: array
        Length of the three edges in the input triangle. Edges are returned
        in the following order of vertices pairs: 0-1, 2-0 and 2-1.
        
    
    """
    
    # Calculate pairwise distance between each vertices.
    d = cdist(t, t)

    return np.array([d[1, 0], d[2, 0], d[2, 1]])


def triangulate_cloud(points, knn, max_eval, max_edge_len):
    
    
    """
    Triangulates a point cloud in a series of local neighborhood planes.
    
    Parameters
    ----------
    points: array
        3D point coordinates of the cloud to triangulate.
    knn: int
        Number of neighbors to use in order to define local neighborhoods of
        points.
    max_eval: float
        Maximum valid value for the third eigenvalue of a local neighborhood.
        The third eigenvalue represents the flatness of a set of points. Which
        means that a value of 0 represents a completely flat set of points.
    max_edge_len: float
        Maximum length of a valid edge in the triangulation. Triangles with
        any edge larger than 'max_edge_len' will not be added to the final
        triangulation.
        
    Returns
    -------
    final_vertices: array
        Set of vertices coordinates of the final triangulation.
    final_triangulation: array
        Set of vertices indices of the final triangulation.
        
    """
       
    # Using 'point_normals' to calculate eigenvalues (other outputs ignored)
    # of all local neighborhoods in the point cloud.
    _, _, ss = point_normals(points, knn)
    
    # Calculating eigenvalues ratio for each neighborhood.
    evals = np.array([(i/np.sum(i)) for i in ss])
    
    # Creating mask based maximum valid value for the third eigenvalue.
    evals_mask = evals[:, 2] <= max_eval
    # Obtaining valid indices (mask == True).
    valid_ids = np.where(evals_mask)[0]
    
    # Running a k nearest neighbor to find all 'knn' valid neighbors around
    # each valid point. These points will become the initial vertices of the
    # triangulation.
    dist, indices = set_nbrs_knn(points[valid_ids], points[valid_ids], knn,
                                 return_dist=True)
    tri_vertices = points[valid_ids]
    
    # Initializing triangles list. This variable will store the triangulation
    # indices.
    triangles = []
    
    # Looping over an enumerated list of valid_ids. 'i' represents the
    # enumeration index of the loop and 'v' is the current valid index.
    for i, v in enumerate(valid_ids):
        # Obtain indices and distances for current neighborhood set.
        nbr_ids = indices[i]
        nbr_dist = dist[i]
        # Filtering possible valid neighboring vertices.
        tri_ids = nbr_ids[nbr_dist <= max_edge_len].astype(int)

        try:
            # Running a dimensional reduction on the current vertices
            # subset (X). This process yields a 2D point set (Y).
            X = tri_vertices[tri_ids]
            pca = PCA(2).fit(X)
            Y = pca.transform(X)
            # Triangulate the 2D vertices array and obtains the list of
            # triangulation simplices.
            tri = Delaunay(Y)
            simp = tri.simplices
    
            # Looping over each simplex.
            for s in simp:
                # Checking if the center of the neighborhood set is part
                # of the current trio of indices.
                if 0 in s:
                    # Calculating edge lengths for the current triangle.
                    vd = edge_length(tri_vertices[tri_ids[s]])
                    # Check if current triangle has all edges with length
                    # smaller than 'max_edge_len'. If so, append to triangles.
                    if np.max(vd) <= max_edge_len:
                        triangles.append(tri_ids[s])
        except:
            pass                  
    # Sorting triangulation indices over axis 1 and removing duplicates.
    # This is done to detect duplicated triangles that have a different
    # vertices ordering.
    tri_sorted = np.array([np.sort(i) for i in triangles])
    tri_sorted = remove_duplicates(tri_sorted)
    
    # Just setting proper variable names.
    final_vertices = tri_vertices
    final_triangulation = tri_sorted.astype(int)
    
    return final_vertices, final_triangulation


def triangulation_centroids(vertices, iterations=1):
    
    """
    Calculates the centroid of each triangle.in the triangulation generated
    from a set of input vertices. A variable number of iterations can be used
    to generate further centroids from previous iterations.
    
    Parameters
    ----------
    vertices: arr
        3D vertices coordinates to triangulate.
    iterations: int
        Number of iterations to run the centroid calculation.
        
    Returns
    -------
    centroids: arr
        3D centroids coordinates.
        
    
    """
    
    # Initializing the centroids variable and looping over n iterations.
    centroids = vertices
    for n in range(iterations):
        # Triangulating current set of centroids.
        vertices, tri = triangulate_cloud(centroids, 20, 0.1, 0.01)
        
        # Initializing resulting centroids variable.
        centroids = np.zeros([tri.shape[0], 3])
        for i, t in enumerate(tri):
            # Calculating centroids and assigning to current ith index.
            centroids[i] = np.mean(vertices[t], axis=0)
            
    return centroids


def expand_triangulation(tri):
    
    """
    Expands the triangulation in order to plot using Mayavi.
    
    Parameters
    ----------
    tri: arr
        Triangulation indices.
        
    Returns
    -------
    expand_tri: arr
        Expanded triangulation indices.
        
    """

    # Initializing variable expand_tri.
    expand_tri = np.zeros([len(tri) * 3, 3], dtype=int)
    # Looping over each set of triangulation indices and expanding it by
    # replicating its indices in 2 other different orders.
    for j, t in enumerate(tri):
        base_id = 3 * j
        expand_tri[base_id, :] = [t[0], t[1], t[2]]
        expand_tri[base_id + 1, :] = [t[1], t[2], t[0]]
        expand_tri[base_id + 2, :] = [t[2], t[0], t[1]]

    return expand_tri

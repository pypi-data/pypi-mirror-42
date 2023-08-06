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


def shift_list(sequence, n):
    
    """
    Shifts over a sequence a number of times.
    
    Parameters
    ----------
    sequence : list
        List sequence to shift.
    n : int
        Number of iterations to shift.
        
    Returns
    -------
    sequence : list
        Shifted sequence.

    """
    
    # Checking if input 'seq' is a list.
    if type(sequence) != list:
        raise TypeError('Input parameter "seq" should be of type "list".')
    
    # Calculating the number of shifts as functionf of the length of seq.
    # This is done to handle 'n' values larger than the length of seq.
    n = n % len(sequence)
    # Shifts and returns.
    return sequence[n:] + sequence[:n]


def tri_to_adjacency(tri):
    
    """
    Creates a dictionary to store adjacency information from a 2D
    triangular mesh (3 vertices per triangle).
    The function will loop over an array of indices and walk over adjacent
    indices (nodes in common) until no new index can be added.
    
    Parameters
    ----------
    tri : array
        2D trianguation indices.
        
    Returns
    -------
    adj_dict : dictionary
        Ajacency dictionary generated from walking over indices in tri.
    
    """
    
    # Initializing adj_dict and setting base column order (axis = 1).
    adj_dict = {}
    columns = [0, 1, 2]
    # Looping over column indices.
    for c in columns:
        # Shifting colum based on column index 'c'. If c = 0, no shifting
        # happens.
        ci = shift_list(columns, c)
        # Looping over set of indices for triangle vertices.
        for t in tri:
            # Checks if current shifted base vertex (ci[0]) is already on
            # adj_dict. If it is, append the other two vertices to it, if
            # not, create a list with the second vertex under ci[0] as key
            # and append the third to it.
            if t[ci[0]] in adj_dict:
                adj_dict[t[ci[0]]].append(t[ci[1]])
            else:
                adj_dict[t[ci[0]]] = [t[ci[1]]]
            adj_dict[t[ci[0]]].append(t[ci[2]])
        
    return adj_dict


def cluster_triangulation(tri):
    
    """
    Clusters a triangular mesh by walking over each connected vertex. If
    the mesh is closed, then it will be in a single cluster.
    
    Parameters
    ----------
    tri : array
        2D trianguation indices.
        
    Returns
    -------
    clusters : array
        1D array containing cluster indices for the triangulation. Output
        will have the shape [0:(max(tri) + 1)].
        
    """
    
    # Generating the adjacency dictionary from triangulation indices.
    adj_dict = tri_to_adjacency(tri)
    
    # Initializing clusters and cluster_id variables.
    clusters = np.zeros(np.max(tri) + 1, dtype=int)
    cluster_id = 0
    # Initializing set of triangulation indices to process. When a index is
    # processed (i.e. added a given cluster_id), it's set to 0 in the
    # to_process array to avoid re-processing it unnecessarily.
    to_process = np.ones(np.max(tri) + 1, dtype=int)

    # Looping over unique triangulation indices.
    for i in np.unique(tri):
        # Setting current index as a list to initialize the current set of
        # adjacent indices.
        p = [i]
        # Checks if current index is set to process (== 1) and if so.
        if to_process[i] == 1:
            # Initialize change and e variables that will be used to keep
            # track of the size change in p. When p stops increasing (no new
            # indices added) the iteration jumps to next ith value.
            change = np.inf
            e = len(p)
            while change > 0:
                # If change is still larger than 0, loops over items in p
                # and add their respective adjacent items to p. This unpacks
                # the adjacency dictionary into p.
                for pi in p:
                    p = p + list(adj_dict[pi])
                    p = list(np.unique(p))
                change = len(p) - e
                e = len(p)
                # Set cluster_id to current set of adjacent indices (p) and
                # set these items to processed (to_process = 0).
                parr = np.array(p)
                clusters[parr] = cluster_id
                to_process[parr] = 0
                # Creates new cluster_id for the next cluster.
                cluster_id += 1

    return clusters




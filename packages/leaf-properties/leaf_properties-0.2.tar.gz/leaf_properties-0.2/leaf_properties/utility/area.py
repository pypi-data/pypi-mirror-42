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
from distance import euclidean_distance as dist


def triangle_area(vertices):
    
    """
    Calculates the area of a triangle.
    
    Parameters
    ----------
    vertices: array
        Coordinates of the 3 triangle vertices.
        
    Returns
    -------
    area: float
        Area of the triangle.
        
    """
    
    side_a = dist(vertices[0], vertices[1])
    side_b = dist(vertices[1], vertices[2])
    side_c = dist(vertices[2], vertices[0])
    s = 0.5 * ( side_a + side_b + side_c)
    
    return np.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Agent utils for rotating the agent on the map

License_info:
# ==============================================================================
# Copyright 2021 Alexander Wendt. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# The following is a slightly modified version from the following script
# Source:

"""

# Futures
# from __future__ import print_function

# Built-in/Generic Imports

# Libs
import math
import numpy as np

# Own modules


__author__ = 'Alexander Wendt'
__copyright__ = 'Copyright 2021'
__credits__ = ['']
__license__ = 'ISC'
__version__ = '0.1.0'
__maintainer__ = 'Alexander Wendt'
__email__ = 'alexander.wendt@gmx.at'
__status__ = 'Experimental'


def rotate_to_relative_coordinates(coordinate, direction):
    '''
    Rotate a certain absolute coordinate from absolute map coordinates to relative agent
    coordinates by using a rotation matrix.

    :param coordinate:
    :return:
    '''

    # Turn view
    # matrix:   cosa -sina
    #            sina cosa
    degree = direction / 360 * 2 * math.pi
    turn_matrix = np.array([[math.cos(degree), -math.sin(degree)],
                            [math.sin(degree), math.cos(degree)]])

    rotated_pos = np.round(np.dot(turn_matrix, np.array(coordinate)), 0).astype(int)

    return rotated_pos


def rotate_to_absolute_coordinates(coordinate, direction):
    '''
    Rotate a certain relative agent coordinate from agent coordinates to absolute map
    coordinates by using a rotation matrix.

    :param coordinate:
    :param direction:
    :return:
    '''

    # Turn view
    # matrix inverse:   cosa sina
    #            -sina cosa
    degree = direction / 360 * 2 * math.pi
    turn_matrix = np.array([[math.cos(degree), math.sin(degree)],
                            [-math.sin(degree), math.cos(degree)]])

    rotated_pos = np.round(np.dot(turn_matrix, np.array(coordinate)), 0).astype(int)

    return rotated_pos


def rotate_centered_matrix_to_relative_coordinates(matrix, direction: int, to_absolute: bool = False):
    '''
    Rotate a perception matrix of the map, 3x3-matrix with agent's position in the center at [1, 1], to agent
    coordinates. Consider that direction=0 degress is pointing down and not up.

    :param to_absolute: Default. From absolute to relative coordinates
    :param matrix:
    :param direction:
    :return:
    '''

    rotated_pos = np.empty(matrix.shape, dtype=object)

    offset = int(matrix.shape[0] / 2)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if to_absolute:
                new_coord = rotate_to_absolute_coordinates([i - offset, j - offset], direction)
            else:
                new_coord = rotate_to_relative_coordinates([i - offset, j - offset], direction)
            rotated_pos[i][j] = matrix[new_coord[0] + offset, new_coord[1] + offset]

    return rotated_pos

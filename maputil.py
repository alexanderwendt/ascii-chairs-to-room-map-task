#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Map and acsii file handling

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
import logging

# Libs

import numpy as np
import pandas as pd

# Own modules


__author__ = 'Alexander Wendt'
__copyright__ = 'Copyright 2021'
__credits__ = ['']
__license__ = 'ISC'
__version__ = '0.1.0'
__maintainer__ = 'Alexander Wendt'
__email__ = 'alexander.wendt@gmx.at'
__status__ = 'Experimental'

log = logging.getLogger()
log.setLevel(logging.DEBUG)


# log.addHandler(logging.StreamHandler())

def load_map(map_path):
    '''
    Load room map int0

    :param map_path:
    :return:
    '''
    maplist = []

    # with open(map_path) as f:
    #    content = f.readline() #f.read()
    #    maplist.append(content) # np.loadtxt(map_path, dtype=str)

    f = open(map_path, 'r')
    for line in f.readlines():
        maplist.append((list(line.strip('\n'))))
    f.close()

    maparray = np.array(maplist, dtype=object)
    print(maparray)

    log.debug("Main Map: \n{}".format(print_map(maparray)))

    room_map = create_room_layer(maparray)
    log.debug("Room Map: \n{}".format(print_map(room_map)))

    chair_map, chair_list = create_chair_layer(maparray)
    log.debug("Chair Map: \n{}".format(print_map(chair_map)))

    name_map, room_name_list = create_name_layer(maparray)
    log.debug("Name Map: \n{}".format(print_map(name_map)))

    return maparray, room_map, chair_map, chair_list, name_map, room_name_list


def print_map(maparray):
    '''

    :param maparray:
    :return:
    '''
    s = ""
    for i in range(maparray.shape[0]):
        s = s + (''.join([str(elem) for elem in maparray[i]])) + '\n'

    return s


def create_room_layer(maparray):
    '''

    :param maparray:
    :return:
    '''

    room_map = np.empty(maparray.shape, dtype=object)

    for i in range(maparray.shape[0]):
        for j in range(maparray.shape[1]):
            wall_chars = ['|', '\"\"', '+', '-', '/']
            if any(x in maparray[i][j] for x in wall_chars):
                room_map[i][j] = '+'
            else:
                room_map[i][j] = ' '

    return room_map


def create_chair_layer(maparray):
    '''

    FIXME: If CPWS is within a word with capital letters, it will be interpreted as a chair

    :param maparray:
    :return:
    '''

    # Create chair list
    chair_list = pd.DataFrame(columns=['ChairType', 'Coordinate', 'RoomId', 'RoomName'])

    chair_map = np.empty(maparray.shape, dtype=object)

    for i in range(maparray.shape[0]):
        for j in range(maparray.shape[1]):
            chair_chars = ['C', 'S', 'P', 'W']
            if any(x in maparray[i][j] for x in chair_chars):
                chair_map[i][j] = maparray[i][j]
                chair_list = chair_list.append(pd.DataFrame(
                    {'ChairType': maparray[i][j], 'Coordinate': [np.array([i, j])], 'RoomId': "", 'RoomName': ""}),
                                               ignore_index=True)
            else:
                chair_map[i][j] = ' '

    return chair_map, chair_list


def create_name_layer(maparray):
    '''


    :param maparray:
    :return:
    '''

    room_name_list = pd.DataFrame(columns=['RoomName', 'Coordinate', 'RoomId'])

    name_map = np.empty(maparray.shape, dtype=object)

    paranthesis_open = False

    word_string = ""
    word_position = None
    for i in range(maparray.shape[0]):
        for j in range(maparray.shape[1]):
            if maparray[i][j] == '(':
                paranthesis_open = True
                word_position = np.array([i, j])
                name_map[i][j] = ' '
            elif maparray[i][j] == ')':
                name_map[i][j] = ' '
                paranthesis_open = False
                room_name_list = room_name_list.append(
                    {'RoomName': word_string, 'Coordinate': word_position, 'RoomId': ""}, ignore_index=True)
                word_string = ""
            elif paranthesis_open == False:
                name_map[i][j] = ' '
            elif paranthesis_open == True:
                name_map[i][j] = maparray[i][j]
                word_string = word_string + name_map[i][j]
            else:
                name_map[i][j] = ' '

    return name_map, room_name_list

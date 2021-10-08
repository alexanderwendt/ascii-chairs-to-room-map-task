#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Agent class

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
import agentutils

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


class Agent:
    '''
    Agent that classifies each coordinate of the room to a room coordinate.
    '''

    # Static variables
    perception = np.empty([3, 3], dtype=object)
    task = ""

    # max_room_id = 0

    def __init__(self, name="Room_Search_Agent", pos=[0, 0], direction=90, room_map="", room_list=None):
        '''
        Init the agent with a position on the map, a direction, the complete map and a list of room names

        Room map and room names are global knowledge.

        pos as [x, y]

        '''

        self.name = name
        self.pos = pos
        self.direction = direction
        self.room_map = room_map
        self.room_list = room_list

        log.debug("Created agent {}. Position {}, direction {}".format(self.name, self.pos, self.direction))
        self.perceive()

    def perceive(self):
        '''
        From current position, get all fields around itself from the own perspective
        Coordinates: Angle 0 is with direction to the bottom, [2, 1] (y, x). First is the y coordinate

        Directions: Degree 0=to the bottom

        :param room_map:
        :return:
        '''

        abs_perception = np.empty([3, 3], dtype=object)

        for i in range(3):
            for j in range(3):
                abs_pos = np.array([self.pos[0] + i - 1, self.pos[1] + j - 1])

                # [x_perception, y_perception], self.direction)  # np.round(np.dot(turn_matrix, np.array([x_perception, y_perception])), 0).astype(np.int)

                if abs_pos[0] >= 0 and \
                        abs_pos[1] >= 0 and \
                        abs_pos[0] <= self.room_map.shape[0] - 1 and \
                        abs_pos[1] <= self.room_map.shape[1] - 1:
                    abs_perception[i][j] = self.room_map[abs_pos[0]][abs_pos[1]]
                else:
                    abs_perception[i][j] = 'X'

        self.perception = agentutils.rotate_centered_matrix_to_relative_coordinates(abs_perception, self.direction,
                                                                                    to_absolute=False)

        log.debug("Current absolute position: {}, direction: {}, perception:\n {}".format(self.pos, self.direction,
                                                                                          self.perception))

    def move_forward(self):
        '''
        Action move forward

        :return:
        '''

        # Convert movement to absolute coordinates
        movement_coordinate = agentutils.rotate_to_relative_coordinates(np.array([1, 0]),
                                                                        self.direction)  # agentutils.rotate_to_absolute_coordinates(np.array([1, 0]), self.direction)
        new_pos = self.pos + movement_coordinate

        log.debug("Move forward: Old abs pos: {}. New pos: {}".format(self.pos, new_pos))

        self.pos = new_pos
        self.perceive()

    def turn_left(self):
        '''
        Turn +90°, left

        :return:
        '''

        log.debug("Turn left: Old direction {}: ".format(self.direction))
        self.direction = self.direction + 90
        if abs(self.direction) == 360:
            self.direction = 0
        log.debug("New direction: {}".format(self.direction))
        self.perceive()

    def turn_right(self):
        '''
        Turn -90°, right

        :return:
        '''

        log.debug("Turn right: Old direction: {}".format(self.direction))
        self.direction = self.direction - 90
        if abs(self.direction) == 360:
            self.direction = 0
        log.debug("New direction: {}".format(self.direction))
        self.perceive()

    def execute_task(self, taskname: str):
        '''
        Agent tasks are collected in a dictionary of functions. Execute a certain task by providing the
        function id string as task name

        :param taskname: function id string
        :return:
        '''

        options = {"map_room": self.task_map_room}

        # Execute task
        self.task = taskname
        log.info("Execute task: {}".format(self.task))
        options[taskname]()

    def task_map_room(self):
        '''
        Task to map a room. First, go to the next wall to the right or the next room id. If found,
        start mapping the room with either a new room id or the previously found id

        :return:
        '''

        # 1. Go left until a wall is found
        # Set new id for room assignment to id
        self.find_reference_at_wall_or_number()
        # 2. Implement right hand rule to go around the room and assign each field the new room coordinate
        # Map room 1
        self.map_room_from_wall_or_id_position()

    def get_new_room_id(self, room_list: pd.DataFrame):
        '''
        Generate a new room id from a list

        :param room_list:
        :return:
        '''

        column_names = ["id", "name"]

        if len(room_list.index) == 0:
            current_index = str(0)
        else:
            # Get last index
            current_index = str(np.max((room_list.index.values.astype(int)) + 1))

        room_list = room_list.append(
            pd.DataFrame({"id": [current_index], "name": ["Room" + str(current_index)]}).set_index("id"))
        return current_index, room_list

    def find_reference_at_wall_or_number(self):
        """
        Move to the wall and if wall or other reference found, return either new reference if wall
        or found reference

        FIXME: Move from any target direction, not just from 0

        :return:
        """

        if self.direction != 0:
            log.warning("Direction is not 0 as it should be at the start of the agent")

        self.turn_left()
        while self.perception[2][1] != "+" and not str.isdigit(self.perception[2][1]) and self.perception[2][1] != "X":
            self.move_forward()
        log.debug("Wall or room id found: {} at position {}".format(self.perception[2][1], self.pos))

        current_room_id = -1

        if str.isdigit(self.perception[2][1]):
            current_room_id = self.perception[2][1]
            log.debug("Room is already identified. Room id: {}".format(current_room_id))
        else:
            # New room_id
            current_room_id, self.room_list = self.get_new_room_id(self.room_list)
            # self.max_room_id = current_room_id + 1
            log.debug("New room id created: {}".format(current_room_id))

        log.info("Room id is {}".format(current_room_id))

        self.room_id = current_room_id

        return current_room_id

    def map_room_from_wall_or_id_position(self):
        '''
        Do as an autonomous vacuum cleaner, use the right rule to always go around the room to the right if
        possible.

        :return:
        '''

        # . From position [0, 1] is wall or id, mark position, turn left and move forward
        # Mark position
        mapping_finished = False

        wall_id_list = ['+', str(self.room_id), 'X']

        while not mapping_finished:
            self.room_map[self.pos[0]][self.pos[1]] = str(self.room_id)
            if any(x in self.perception[2][1] for x in wall_id_list) and \
                    any(x in self.perception[1][2] for x in wall_id_list) and \
                    any(x in self.perception[1][0] for x in wall_id_list):
                log.debug("No more possibility to map. Return method")
                mapping_finished = True
            elif self.perception[2][1] == " " and any(
                    x in self.perception[1][0] for x in wall_id_list):  # Forward free, right wall
                self.move_forward()
            elif any(x in self.perception[2][1] for x in wall_id_list):
                self.turn_left()
            elif self.perception[1][0] == " ":  # Right free
                self.turn_right()
            else:
                raise Exception("Uncovered case: Perception {}".format(self.perception))

        log.debug("Mapping of room finished. Return")

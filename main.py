#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The following program has been written to solve an exercise in text handling. The task is to get a room plan as ascii
text and assign chairs to a certain room based on the ascii map with rooms
and postions for chairs. The room structure looks like this:

+-----------+------------------------------------+
|           |                                    |
| (closet)  |         (kitchen)                  |
|         P |                            S       |
+--------------------------+---------------------+
                           |  (balcony)          |
                           |                 P   |
                           +---------------------+

The result is a list returns the number of different chair types for the appartment,
the number of different chair types per room. The output should look like this, sorted in alphabethically order:
total:
W: 4, P: 0, S: 2, C: 1
living room:
W: 3, P: 0, S: 2, C: 1
office:
W: 1, P: 0, S: 0, C: 0

Usage: python main.py --map_path=rooms.txt --output=result.txt

parser.add_argument("-p", '--map_path', default='task_map/rooms_test.txt',
                    help='Input rooms file', required=False)
parser.add_argument("-o", '--output', default='result.txt',
                   help='Save output file path', required=False)

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
import argparse
import copy
import logging

# Libs
import pandas as pd

# Own modules
import maputil
from agent import Agent

__author__ = 'Alexander Wendt'
__copyright__ = 'Copyright 2021'
__credits__ = ['']
__license__ = 'ISC'
__version__ = '0.1.0'
__maintainer__ = 'Alexander Wendt'
__email__ = 'alexander.wendt@gmx.at'
__status__ = 'Experimental'

parser = argparse.ArgumentParser(description='Room Assignment Task')
parser.add_argument("-p", '--map_path', default='task_map/rooms_test.txt',
                    help='Input rooms file', required=False)
parser.add_argument("-o", '--output', default='result.txt',
                    help='Save output file path', required=False)

args = parser.parse_args()

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Set handler only once
log.addHandler(logging.StreamHandler())

log.info(args)

room_list = pd.DataFrame(columns=["id", "name"]).set_index("id")


def assign_field_to_room(room_map):
    '''
    Assign each field in the ASCII to a room id. Use an agent to do that.

    :param room_map: Room map
    :return:
    '''

    room_list = pd.DataFrame(columns=["id", "name"]).set_index("id")
    filledout_room_map = copy.deepcopy(room_map)

    # myAgent = Agent(log, name="Room1", pos=[1,1], direction=0, room_map=room_map)

    # Start with first field with sign " " and execute agent task map room:
    all_fields_covered = False
    while not all_fields_covered:
        new_room_found = False
        for i in range(filledout_room_map.shape[0]):
            for j in range(filledout_room_map.shape[1]):
                if filledout_room_map[i][j] == " ":
                    # On the first free field, execute mapping task
                    myAgent1 = Agent(name="Room1", pos=[i, j], direction=0, room_map=filledout_room_map,
                                     room_list=room_list)
                    myAgent1.execute_task("map_room")
                    log.debug("Room Map: \n{}".format(maputil.print_map(myAgent1.room_map)))

                    # Get current room list from agent
                    room_list = myAgent1.room_list
                    new_room_found = True
                    break

            if new_room_found:
                break

        if new_room_found == False:
            all_fields_covered = True

    return filledout_room_map


def assign_chairs_to_rooms(map_path, output_path):
    '''
    The main task is to assign chairs to rooms. First, the map, chairs and rooms names are read. Then, an agent
    system is used to go through each room and assign it a room number. Finally, the chair positions are assinged a
    room. The output string is created and saved into a file.

    :param map_path:
    :return:
    '''
    log.debug("Room path: {}".format(map_path))

    # Load room file to array, array size max rows, max col
    ## Layer 1
    ### Add array with dim
    ### Put signs in array
    ### Replace +|-/\ with +
    # Layer 2: Add all chairs: S, W, P on the map
    # Layer 3: Add all names. Start with ( and end with )
    maparray, room_map, chair_map, chair_list, name_map, room_name_list = maputil.load_map(map_path)

    # Define the rooms
    filledout_room_map = assign_field_to_room(room_map)
    log.debug("Final room map: \n{}".format(maputil.print_map(filledout_room_map)))

    # Connect chairs with rooms
    chair_room_map = merge_chairs_rooms(filledout_room_map, chair_list, room_name_list)

    # Create results
    result = generate_output(chair_room_map, room_name_list)

    # Save results to file
    text_file = open(output_path, "w")
    text_file.write(result)
    text_file.close()
    log.debug("Writing to {}".format(output_path))

    log.info("Program finished.")


def generate_output(chair_room_map, room_name_list):
    '''
    Generate output string

    :param chair_room_map:
    :return:
    '''

    output_string = ""

    # Get total number of chairs
    output_string = output_string + "total:\n"
    chair_stats_string = get_chair_stats(chair_room_map)
    output_string = output_string + chair_stats_string

    # Go through each room in alphabethic order
    sorted_room_list = room_name_list.sort_values(by='RoomName')['RoomName'].values
    for room_name in sorted_room_list:
        chairs_in_room = chair_room_map[chair_room_map['RoomName'] == room_name]
        chair_stats_string = get_chair_stats(chairs_in_room)
        output_string = output_string + '\n' + room_name + ":\n"
        output_string = output_string + chair_stats_string

    log.info("Output string: \n{}".format(output_string))
    return output_string


def get_chair_stats(chair_room_map):
    '''
    Get number of chairs per chair name from the map

    :param chair_room_map:
    :param output_string:
    :return:
    '''
    output_string = ""
    for chairtype in ['W', 'P', 'S', 'C']:
        chair_amount = chair_room_map[chair_room_map['ChairType'] == chairtype].shape[0]
        output_string = output_string + chairtype + ": " + str(chair_amount)
        if chairtype != 'C':
            output_string = output_string + ", "

    return output_string


def merge_chairs_rooms(filledout_room_map, chair_list, room_name_list):
    '''
    Connect chairs with rooms

    :param filledout_room_map:
    :param chair_list:
    :param room_name_list:
    :return:
    '''

    # Map coordinate to room names
    for index, row in room_name_list.iterrows():
        room_id = filledout_room_map[row.Coordinate[0]][row.Coordinate[1]]
        row.RoomId = room_id

    room_name_list.set_index('RoomId', inplace=True)
    log.debug("Room list: \n{}".format(room_name_list[['RoomName']]))

    # Map chairs to room id
    for index, row in chair_list.iterrows():
        room_id = filledout_room_map[row.Coordinate[0]][row.Coordinate[1]]
        row.RoomId = room_id
        row.RoomName = room_name_list.loc[room_id].RoomName

    log.debug("Chair list: \n{}".format(chair_list[['ChairType', 'RoomName']]))

    chair_room_map = chair_list[['ChairType', 'RoomName']]

    return chair_room_map


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    assign_chairs_to_rooms(args.map_path, args.output)

    log.info("=== Program end ===")

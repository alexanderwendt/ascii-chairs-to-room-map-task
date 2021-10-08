import logging
import unittest

import pandas as pd

import maputil
from agent import Agent

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

class AgentTest(unittest.TestCase):
    '''

    '''

    room_map=None
    name_map=None
    chair_map=None
    myAgent=None

    def setUp(self): #Run before each test
        '''

        :return:
        '''

        maparray, self.room_map, self.chair_map, _, self.name_map, _ = maputil.load_map("agenttest_multiple_rooms.txt")
        #self.myAgent = Agent(name="RoomName", pos=[1, 1], direction=0, room_map=self.room_map)

    def test_map_multiple_rooms(self):
        '''
        Map multiple rooms

        :return:
        '''

        column_names = ["id", "name"]
        room_list = pd.DataFrame(columns = column_names).set_index("id")

        #Map room 1
        myAgent1 = Agent(name="Room1", pos=[1, 1], direction=0, room_map=self.room_map, room_list=room_list)
        myAgent1.execute_task("map_room")
        #myAgent1.find_reference_at_wall_or_number()
        #myAgent1.map_room_from_wall_or_id_position()

        updated_room_list = myAgent1.room_list

        log.debug("Room_map: {}. Room id: {}".format(myAgent1.room_map, myAgent1.room_id))
        #Map room 2
        myAgent2 = Agent(name="Room2", pos=[1, 12], direction=0, room_map=self.room_map, room_list=updated_room_list)
        myAgent2.execute_task("map_room")
        #myAgent2.find_reference_at_wall_or_number()
        #myAgent2.map_room_from_wall_or_id_position()

        log.debug("Room Map: \n{}".format(maputil.print_map(myAgent2.room_map)))

        self.assertEqual(str(myAgent2.room_map[2][16]), '1')
        self.assertEqual(myAgent2.room_id, '1')


    def tearDown(self): #Run after each test
        '''

        :return:
        '''

if __name__ == '__main__':
    #unittest.main()
    #AgentTest.test_perception_angle_0()
    #AgentTest.test_perception_turn_left
    #AgentTest.test_perception_turn_right()
    #AgentTest.test_perception_move_forward()
    #AgentTest.test_perception_turn_right_move_forward()
    #AgentTest.test_move_to_next_wall()
    #AgentTest.test_move_to_next_known_id()
    AgentTest.test_define_room_id

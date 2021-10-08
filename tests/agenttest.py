import logging
import unittest

import maputil
from agent import Agent

import pandas as pd

log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

class AgentTest(unittest.TestCase):
    '''

    '''

    room_map=None
    myAgent=None

    def setUp(self): #Run before each test
        '''

        :return:
        '''

        room_list = pd.DataFrame(columns=["id", "name"]).set_index("id")
        maparray, self.room_map, chair_map, _, name_map, _ = maputil.load_map("agenttest_rooms.txt")
        self.myAgent = Agent(name="Room1", pos=[1, 1], direction=0, room_map=self.room_map, room_list=room_list)

    def test_perception_angle_0(self):
        '''

        :return:
        '''

        #perceive world
        self.myAgent.perceive()

        self.assertEqual(self.myAgent.perception[1][1], " ")
        self.assertEqual(self.myAgent.perception[0][0], "+")
        self.assertEqual(self.myAgent.perception[0][2], "+")

    def test_perception_turn_left(self):
        '''

        :return:
        '''

        #perceive world
        #self.myAgent.perceive()
        self.myAgent.turn_left()
        self.myAgent.turn_left()
        self.myAgent.turn_left()
        self.myAgent.turn_left()
        #self.myAgent.perceive()

        self.assertEqual(self.myAgent.perception[1][1], " ")
        self.assertEqual(self.myAgent.perception[0][0], "+")
        self.assertEqual(self.myAgent.perception[2][2], " ")

    def test_perception_turn_right(self):
        '''

        :return:
        '''

        #perceive world
        #self.myAgent.perceive()
        self.myAgent.turn_right()
        self.myAgent.turn_right()
        self.myAgent.turn_right()
        self.myAgent.turn_right()
        #self.myAgent.perceive()



        self.assertEqual(self.myAgent.perception[1][1], " ")
        self.assertEqual(self.myAgent.perception[0][0], "+")
        self.assertEqual(self.myAgent.perception[0][2], "+")

    def test_perception_move_forward(self):
        '''

        :return:
        '''

        #Direction 0 is down to higher map rows, not up

        #perceive world
        self.myAgent.move_forward()

        self.assertEqual(self.myAgent.perception[1][1], " ")
        self.assertEqual(self.myAgent.perception[0][0], "+")
        self.assertEqual(self.myAgent.perception[2][2], " ")

    def test_perception_turn_right_move_forward(self):
        '''

        :return:
        '''

        #perceive world
        #self.myAgent.perceive()
        self.myAgent.turn_left()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()
        self.myAgent.move_forward()
        #self.myAgent.perceive()

        self.assertEqual(self.myAgent.perception[1][1], "+")
        self.assertEqual(self.myAgent.perception[0][0], " ")
        self.assertEqual(self.myAgent.perception[2][2], "X")

    def test_move_to_next_wall(self):
        '''
        Move left (in coordinate system) until a wall is reached and stop there

        :return:
        '''
        current_room_id = self.myAgent.find_reference_at_wall_or_number()
        self.assertEqual(self.myAgent.perception[2][1], "+")
        self.assertEqual(current_room_id, '0')

    def test_move_to_next_known_id(self):
        '''
        Move left (in coordinate system) until a wall is reached and stop there

        :return:
        '''

        self.myAgent.room_map[1,11] = '2'

        current_room_id = self.myAgent.find_reference_at_wall_or_number()
        self.assertEqual(self.myAgent.perception[2][1], '2')
        self.assertEqual(current_room_id, '2')


    def test_define_room_id(self):
        '''
        Find wall. Assign a room a coordinate

        :return:
        '''

        current_room_id = self.myAgent.find_reference_at_wall_or_number()
        self.myAgent.room_id = str(current_room_id)
        self.myAgent.map_room_from_wall_or_id_position()


        self.assertEqual(self.myAgent.room_map[2][5], '0')
        self.assertEqual(self.myAgent.room_id, '0')


    def tearDown(self): #Run after each test
        '''

        :return:
        '''

if __name__ == '__main__':
    #unittest.main()
    AgentTest.test_perception_angle_0()
    AgentTest.test_perception_turn_left
    AgentTest.test_perception_turn_right()
    AgentTest.test_perception_move_forward()
    AgentTest.test_perception_turn_right_move_forward()
    AgentTest.test_move_to_next_wall()
    AgentTest.test_move_to_next_known_id()
    AgentTest.test_define_room_id

import unittest

import numpy as np
import agentutils


class RotationTest(unittest.TestCase):
    abs_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_rotation_angle_0(self):
        rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(self.abs_matrix, 0)

        print("Absolute matrix: \n{}. \nRotated matrix:\n{}".format(self.abs_matrix, rotated_matrix))
        self.assertEqual(rotated_matrix[0,0], self.abs_matrix[0,0])  # add assertion here
        self.assertEqual(rotated_matrix[0, 2], self.abs_matrix[0, 2])  # add assertion here

    def test_rotation_angle_180(self):
        rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(self.abs_matrix, 180)

        print("Absolute matrix: \n{}. \nRotated matrix:\n{}".format(self.abs_matrix, rotated_matrix))
        self.assertEqual(rotated_matrix[0,0], self.abs_matrix[2,2])
        self.assertEqual(rotated_matrix[1, 1], self.abs_matrix[1, 1])
        self.assertEqual(rotated_matrix[0, 1], self.abs_matrix[2, 1])

    def test_rotation_angle_270(self):
        '''
        Turn right=270 degrees

        :return:
        '''
        rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(self.abs_matrix, 270)

        print("Absolute matrix: \n{}. \nRotated matrix:\n{}".format(self.abs_matrix, rotated_matrix))
        self.assertEqual(rotated_matrix[0,2], self.abs_matrix[2,2])
        self.assertEqual(rotated_matrix[1, 1], self.abs_matrix[1, 1])
        self.assertEqual(rotated_matrix[2, 0], self.abs_matrix[0, 0])

    def test_rotation_angle_90(self):
        '''
        Turn left=90 degrees

        :return:
        '''
        rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(self.abs_matrix, 90)

        print("Absolute matrix: \n{}. \nRotated matrix:\n{}".format(self.abs_matrix, rotated_matrix))
        self.assertEqual(rotated_matrix[2,0], self.abs_matrix[2,2])
        self.assertEqual(rotated_matrix[1, 1], self.abs_matrix[1, 1])
        self.assertEqual(rotated_matrix[0, 0], self.abs_matrix[2, 0])

    def test_rotation_rel_to_abs_coordinates(self):
        '''
        Turn left=90 degrees

        :return:
        '''
        rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(self.abs_matrix, 90)
        abs_from_rotated_matrix = agentutils.rotate_centered_matrix_to_relative_coordinates(rotated_matrix, 90, to_absolute=True)

        print("Absolute matrix: \n{}. \nAbsolute back rotated matrix:\n{}".format(self.abs_matrix, abs_from_rotated_matrix))
        self.assertEqual(abs_from_rotated_matrix[2,2], self.abs_matrix[2,2])
        self.assertEqual(abs_from_rotated_matrix[1, 1], self.abs_matrix[1, 1])
        self.assertEqual(abs_from_rotated_matrix[0, 0], self.abs_matrix[0, 0])


if __name__ == '__main__':
    unittest.main()
    #RotationTest.test_rotation_angle_0()
    #RotationTest.test_rotation_angle_180()
    #RotationTest.test_rotation_angle_270()
    #RotationTest.test_rotation_angle_90()
    #RotationTest.test_rotation_rel_to_abs_coordinates()

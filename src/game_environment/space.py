from enum import Enum
from cube import Cube
from src.utils.gui import print_cube_list
import numpy as np
from src.utils import math_utils


class Orientation(Enum):
    x_axis = 0
    y_axis = 1
    z_axis = 2
    unknown = 3


class Space3D:
    def __init__(self):
        self.cube_list = []

    def add_cube(self, cube):
        self.cube_list.append(cube)

    def get_cube_list(self):
        return self.cube_list

    def rotate_cubes_after_index(self, cube_index, orientation, angle):
        cube_list_ref = self.cube_list[cube_index:]
        Space3D.rotate_cubes(
            cube_list_ref,
            cube_list_ref[0],
            orientation,
            angle
        )

    def rotate_cubes_before_index(self, cube_index, orientation, angle):
        cube_list_ref = self.cube_list[:cube_index + 1]
        Space3D.rotate_cubes(
            cube_list_ref,
            cube_list_ref[len(cube_list_ref) - 1],
            orientation,
            angle
        )

    def print(self):
        print_cube_list(self.cube_list)

    @staticmethod
    def rotate_cubes(cube_list, ref_cube, orientation, angle):
        ref_cube_copy = Cube(ref_cube.x, ref_cube.y, ref_cube.z)

        math_utils.transform_to_coordinate(cube_list, ref_cube_copy)

        Space3D.rotate(cube_list, orientation, angle)

        # moving the cube_list to it`s original position
        math_utils.transform_to_coordinate(
            cube_list,
            Cube(
                ref_cube_copy.x * -1,
                ref_cube_copy.y * -1,
                ref_cube_copy.z * -1,
            )
        )

    @staticmethod
    def rotate(cube_list, orientation, angle):
        rotation_matrix = Space3D.rotation_matrix_func(orientation)
        for cube in cube_list:
            point = [cube.x, cube.y, cube.z]
            result_matrix = np.dot(rotation_matrix(angle), point)
            rotated_point = np.ravel(result_matrix)
            cube.set_x(math_utils.round_close(rotated_point[0]))
            cube.set_y(math_utils.round_close(rotated_point[1]))
            cube.set_z(math_utils.round_close(rotated_point[2]))

    @staticmethod
    def rotation_matrix_func(orientation):
        if orientation == Orientation.x_axis:
            return math_utils.rotation_matrix_x
        if orientation == Orientation.y_axis:
            return math_utils.rotation_matrix_y
        if orientation == Orientation.z_axis:
            return math_utils.rotation_matrix_z

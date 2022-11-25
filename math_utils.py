import numpy as np
from math import cos, sin, ceil, floor


def rotation_matrix_x(theta):
    return np.matrix([
        [1, 0, 0],
        [0, cos(theta), -sin(theta)],
        [0, sin(theta), cos(theta)]
    ])


def rotation_matrix_y(theta):
    return np.matrix([
        [cos(theta), 0, sin(theta)],
        [0, 1, 0],
        [-sin(theta), 0, cos(theta)]
    ])


def rotation_matrix_z(theta):
    return np.matrix([
        [cos(theta), -sin(theta), 0],
        [sin(theta), cos(theta), 0],
        [0, 0, 1]
    ])


def transform_to_coordinate(cube_list, ref_cube):
    for cube in cube_list:
        delta_x = cube.x - ref_cube.x
        delta_y = cube.y - ref_cube.y
        delta_z = cube.z - ref_cube.z
        cube.update_coordinates(delta_x, delta_y, delta_z)


def round_close(num):
    abs_num = abs(num)
    decimal_place = abs_num - int(abs_num)
    if decimal_place > 0.5:
        if num < 0:
            return ceil(abs_num) * -1
        return ceil(abs_num)

    if num < 0:
        return floor(abs_num) * -1
    return floor(abs_num)

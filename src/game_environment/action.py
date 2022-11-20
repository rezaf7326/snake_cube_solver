from enum import Enum
from math import pi


class Direction(Enum):
    backward = 0
    forward = 1


class RotateAction:
    def __init__(self, direction, orientation, angle):
        self.orientation = orientation
        self.angle = angle
        # to rotate from cube_index to end (forward) or from 0 to cube_index (backward)
        self.direction = direction

    @staticmethod
    def valid_angles():
        return [pi / 2, pi, 3 * (pi / 2)]

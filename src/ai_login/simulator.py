from src.game_environment.space import Space3D
from src.game_environment.cube import Cube
from src.game_environment.action import Direction


class Simulator:
    def __init__(self, coordinates, sticky_cubes):
        self.space = Space3D()
        self.coordinates = coordinates
        self.sticky_cubes = sticky_cubes
        self.head_index = 0
        self.taken_actions_list = []

    def build_space(self):
        for coord in self.coordinates:
            self.space.add_cube(Cube(coord[0], coord[1], coord[2]))

    def get_space(self):
        return self.space

    def get_taken_actions_list(self):
        return self.taken_actions_list

    def set_taken_actions_list(self, taken_actions_list):
        self.taken_actions_list = taken_actions_list

    def add_taken_action(self, taken_action):
        self.taken_actions_list.append(taken_action)

    def get_stickies(self):
        return self.sticky_cubes

    def get_coordinates(self):
        return self.coordinates

    def print_space(self):
        self.space.print()

    def take_action(self, action):
        if action.direction == Direction.backward:
            self.space.rotate_cubes_before_index(
                self.get_head(),
                action.orientation,
                action.angle
            )
        else:
            self.space.rotate_cubes_after_index(
                self.get_head(),
                action.orientation,
                action.angle
            )

    def move_to_next_head(self):
        self.head_index += 1

    def set_head(self, head_index):
        self.head_index = head_index

    def get_head(self):
        return self.head_index

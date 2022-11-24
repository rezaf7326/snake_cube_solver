from space import Space3D
from cube import Cube
from action import Direction
from space import Orientation

class Simulator:
    def __init__(self, coordinates, sticky_cubes, taken_actions_list):
        self.space = Space3D()
        self.coordinates = coordinates
        self.sticky_cubes = sticky_cubes
        self.head_index = 0
        self.taken_actions_list = taken_actions_list

    def build_space(self):
        for coord in self.coordinates:
            self.space.add_cube(Cube(coord[0], coord[1], coord[2]))

    def get_space(self):
        return self.space

    def get_stickies(self):
        return self.sticky_cubes

    def get_taken_actions_list(self):
        return self.taken_actions_list

    def get_coordinates(self):
        return self.coordinates

    def print_space(self):
        for cube in self.space.get_cube_list():  # TODO REMOVE this for loop
            print([cube.x, cube.y, cube.z])
        self.space.print()

    def taken_actions(self, action):
        takenAction = []
        takenAction.append(self.get_head())
        match action.orientation:
            case Orientation.x_axis:
                takenAction.append(0)
            case Orientation.y_axis:
                takenAction.append(1)
            case Orientation.z_axis:
                takenAction.append(2)
        match action.angle:
            case 3.141592653589793:
                takenAction.append(-2)
            case 1.5707963267948966:
                takenAction.append(1)
            case 4.71238898038469:
                takenAction.append(-1)
        self.taken_actions_list.append(takenAction) 

    def take_action(self, action):
        if action.direction == Direction.backward:
            self.space.rotate_cubes_before_index(
                self.get_head(),
                action.orientation,
                action.angle
            )
            self.taken_actions(action)
        else:
            self.space.rotate_cubes_after_index(
                self.get_head(),
                action.orientation,
                action.angle
            )
            self.taken_actions(action)

    def move_to_next_head(self):
        self.head_index += 1

    def set_head(self, head_index):
        self.head_index = head_index

    def get_head(self):
        return self.head_index

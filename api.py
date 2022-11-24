from space import Orientation
from action import RotateAction, Direction
from cube import Cube
from simulator import Simulator


class API:
    def __init__(self):
        pass

    """ The "game" parameter of the API methods is an instance of the Simulator class """

    @staticmethod
    def evolve(game, action):
        game.take_action(action)

    @staticmethod
    def valid_actions(game):
        # returns an array of RotationAction
        game.move_to_next_head()

        while API.is_rotation_redundant(game):
            game.move_to_next_head()

        return API.get_corner_actions(game)

    @staticmethod
    def copy_game(game):
        coordinates_copy = []
        taken_actions_copy = []
        for taken_action in game.get_taken_actions_list():
            taken_actions_copy.append([*taken_action])
        for coord in game.get_coordinates():
            coordinates_copy.append([*coord])

        game_copy = Simulator(coordinates_copy, game.get_stickies(), taken_actions_copy)
        game_copy.build_space()
        game_copy.set_head(game.get_head())

        return game_copy

    @staticmethod
    def is_victory(game):  # TODO refactor
        cube_list = game.get_space().get_cube_list()
        # I've chosen z axis(makes no difference to chose x or y) for goal-test operation
        min_z = 1_000_000_000
        for cube in cube_list:
            if cube.z < min_z:
                min_z = cube.z

        min_z_cube_list = [cube for cube in cube_list if cube.z == min_z]
        if len(min_z_cube_list) != 9:
            return False
        min_z_cube_list_compliment_1 = [cube for cube in cube_list if cube.z == min_z + 1]
        if len(min_z_cube_list_compliment_1) != 9:
            return False
        min_z_cube_list_compliment_2 = [cube for cube in cube_list if cube.z == min_z + 2]
        if len(min_z_cube_list_compliment_2) != 9:
            return False

        for cube in min_z_cube_list:
            x = cube.x
            y = cube.y
            if not (
                    API.includes_cube(Cube(x, y, cube.z + 1), min_z_cube_list_compliment_1) or
                    API.includes_cube(Cube(x, y, cube.z + 2), min_z_cube_list_compliment_2)
            ):
                return False

        return True

    @staticmethod
    def is_cube_match(cube_1, cube_2):
        return cube_1.x == cube_2.x and cube_1.y == cube_2.y and cube_1.z == cube_2.z

    @staticmethod
    def includes_cube(cube, cube_list):
        for c in cube_list:
            if API.is_cube_match(c, cube):
                return True
        return False

    @staticmethod
    def is_rotation_redundant(game):
        if game.get_head() == 0 or game.get_head() == 26:
            return True

        redundant_case_1 = not API.is_corner(game) and not API.is_stick_to_next(game, game.get_head())
        redundant_case_2 = False
        if API.is_stick_to_next(game, game.get_head()):
            last_sticky = API.last_sticky_in_chain(game)
            game.set_head(last_sticky)  # todo refactor: set_head should not be here!
            redundant_case_2 = not API.is_corner(game)

        return redundant_case_1 or redundant_case_2

    # TODO review method (commented repetitive actions)
    @staticmethod
    def get_corner_actions(game):
        direction = API.get_shorter_direction(game)
        next_orient = API.get_orientation(game, game.get_head(), game.get_head() + 1)
        # prev_orient = API.get_orientation(game, game.get_head() - 1, game.get_head())

        action_list = []
        for angle in RotateAction.valid_angles():
            action_list.append(RotateAction(direction, next_orient, angle))
            # action_list.append(RotateAction(direction, prev_orient, angle))

        return action_list

    @staticmethod
    def get_orientation(game, cube_1_index, cube_2_index):
        if cube_1_index < 0:
            cube_1_index = 0
        if cube_2_index > 26:
            cube_2_index = 26
        cube_list = game.get_space().get_cube_list()
        cube_1 = cube_list[cube_1_index]
        cube_2 = cube_list[cube_2_index]
        for cube_tuple in cube_1.__dict__.items():
            if cube_tuple[0] == "x" and cube_2.x != cube_tuple[1]:
                return Orientation.x_axis
            if cube_tuple[0] == "y" and cube_2.y != cube_tuple[1]:
                return Orientation.y_axis
            if cube_tuple[0] == "z" and cube_2.z != cube_tuple[1]:
                return Orientation.z_axis

    @staticmethod
    def are_same_orientation(game, from_cube_index, to_cube_index):
        prev_orient = Orientation.unknown
        for cube_index in range(from_cube_index, to_cube_index):
            next_orient = API.get_orientation(game, cube_index, cube_index + 1)
            if prev_orient != Orientation.unknown and prev_orient != next_orient:
                return False
            prev_orient = next_orient
        return True

    @staticmethod
    def is_stick_to_next(game, cube_index):
        for sticky_chain in game.get_stickies():
            if sticky_chain.count(cube_index) > 0:
                return sticky_chain[len(sticky_chain) - 1] != cube_index
        return False

    @staticmethod
    def last_sticky_in_chain(game):
        cube_index = game.get_head()
        while API.is_stick_to_next(game, cube_index):
            cube_index += 1
        return cube_index

    @staticmethod
    def is_corner(game):
        return not API.are_same_orientation(game, game.get_head() - 1, game.get_head() + 1)

    @staticmethod
    def get_shorter_direction(game):
        cube_list = game.get_space().get_cube_list()
        if (len(cube_list) - 1) - game.get_head() > game.get_head():
            return Direction.backward
        return Direction.forward

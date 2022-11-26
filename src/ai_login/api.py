from src.game_environment.space import Orientation
from src.game_environment.action import RotateAction, Direction
from src.game_environment.cube import Cube
from src.ai_login.simulator import Simulator


class API:
    def __init__(self):
        pass

    """ The "game" parameter of the API methods is an instance of the Simulator class """

    @staticmethod
    def evolve(game, action):
        game.take_action(action)
        game.add_taken_action(
            TestOnlyAPI.as_taken_action(game, action)
        )

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

        game_copy = Simulator(coordinates_copy, game.get_stickies())
        game_copy.set_taken_actions_list(taken_actions_copy)
        game_copy.set_head(game.get_head())
        game_copy.build_space()

        return game_copy

    @staticmethod
    def is_victory(game):
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
            if (
                not API.includes_cube(Cube(x, y, cube.z + 1), min_z_cube_list_compliment_1) or
                not API.includes_cube(Cube(x, y, cube.z + 2), min_z_cube_list_compliment_2)
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

    @staticmethod
    def get_corner_actions(game):
        direction = API.get_shorter_direction(game)
        next_orient = API.get_orientation(game, game.get_head(), game.get_head() + 1)

        action_list = []
        for angle in RotateAction.valid_angles():
            action_list.append(RotateAction(direction, next_orient, angle))

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


class TestOnlyAPI:
    @staticmethod
    def as_taken_action(game, action):
        # taken_action is an array of
        #   [
        #       cube_index,
        #       orientation_enum {0: x_axis, 1: y_axis, 2: z_axis},
        #       angle_enum {-2: 180/-180deg, -1: 270/-90deg, 1: 90deg}
        #   ]
        return [
            game.get_head(),
            TestOnlyAPI.parse_orientation(action.orientation),
            TestOnlyAPI.parse_angle(action.angle)
        ]

    @staticmethod
    def parse_orientation(orientation):
        if orientation == Orientation.x_axis:
            return 0
        if orientation == Orientation.y_axis:
            return 1
        if orientation == Orientation.z_axis:
            return 2

    @staticmethod
    def parse_angle(angle):
        deg_90 = RotateAction.valid_angles()[0]
        deg_180 = RotateAction.valid_angles()[1]
        deg_270 = RotateAction.valid_angles()[2]
        if angle == deg_90:
            return 1
        if angle == deg_180:
            return -2
        if angle == deg_270:
            return -1

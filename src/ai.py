import json
from src.ai_login.simulator import Simulator
from src.ai_login.algorithm import BFS


class Agent:
    def __init__(self):
        pass

    # the act function takes a json string as input and outputs a list of actions.
    # action example: [1,2,-2]
    # the first number is the cube index (0: the first cube)
    # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
    # the third number is the degree (1: 90 degree, -2: -180/180 degree, -1: -90/270 degree)
    def act(self, percept):
        sensor_data = json.loads(percept)

        game = Simulator(sensor_data["coordinates"], sensor_data["sticky_cubes"])

        algorithm = BFS()
        resolved_game = algorithm.search(game)

        return resolved_game.get_taken_actions_list()

import json
from src.ai_logic.simulator import Simulator
from src.ai_logic.algorithm import BFS


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the act function takes a json string as input
    # and outputs an action string
    # action example: [1,2,-2]
    # the first number is the joint number (1: the first joint)
    # the second number is the axis number (0: x-axis, 1: y-axis, 2: z-axis)
    # the third number is the degree (1: 90 degree, -2: -180 degree, -1000: -90000 degree)
    def act(self, percept):  # TODO integrate with the new input/output
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        game = Simulator(sensor_data["coordinates"], sensor_data["sticky_cubes"])

        game.print_space() # TODO REMOVE

        algorithm = BFS()
        updated_coordinates = algorithm.search(game)

        game.print_space() # TODO REMOVE

        return updated_coordinates

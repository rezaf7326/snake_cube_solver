from simulator import Simulator
from algorithm import BFS

json = {
    "coordinates": [[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 2], [-1, 1, 2], [-1, 0, 2], [0, 0, 2], [0, -1, 2], [0, -1, 1], [0, -1, 0], [-1, -1, 0], [-2, -1, 0], [-2, -1, 1], [-1, -1, 1], [-1, -1, 2], [-2, -1, 2], [-2, 0, 2], [-2, 0, 1], [-1, 0, 1], [-1, 0, 0], [-2, 0, 0], [-2, 1, 0], [-2, 1, 1], [-2, 1, 2]],
    "stick_together": [[0, 1], [1, 2], [2, 3], [5, 6], [6, 7], [9, 10], [10, 11], [11, 12], [17, 18], [20, 21], [25, 26]]
}

json2 = {
    "coordinates": [[0, 0, -1], [0, 0, 0], [-1, 0, 0], [-1, 0, -1], [-2, 0, -1], [-2, -1, -1], [-2, -1, 0], [-2, 0, 0], [-2, 0, 1], [-2, -1, 1], [-2, -2, 1], [-1, -2, 1], [-1, -2, 0], [-2, -2, 0], [-2, -2, -1], [-1, -2, -1], [-1, -1, -1], [0, -1, -1], [0, -2, -1], [0, -2, 0], [0, -2, 1], [0, -1, 1], [-1, -1, 1], [-1, -1, 2], [0, -1, 2], [0, 0, 2], [0, 0, 1]],
    "stick_together": [[1, 2], [4, 5], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [18, 19]]
}


selected_json = json2

game = Simulator(
    selected_json.get("coordinates"),
    selected_json.get("stick_together")
)
game.build_space()

bfs = BFS()
bfs.search(game)

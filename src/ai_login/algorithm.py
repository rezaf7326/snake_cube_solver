from src.ai_login.api import API
import random


class BFS:
    def __init__(self):
        self.queue = []
        self.visited = []
        self.api = API()

    def search(self, game):
        self.queue.append(game)

        while self.queue:
            node = self.queue.pop(0)

            valid_actions = self.api.valid_actions(node)

            random.shuffle(valid_actions)

            for action in valid_actions:
                child_node = self.api.copy_game(node)
                self.api.evolve(child_node, action)

                self.queue.append(child_node)

                if self.api.is_victory(child_node):
                    print("BFS search successful.")
                    return child_node

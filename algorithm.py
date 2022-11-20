from api import API
import random


class BFS:
    def __init__(self):
        self.queue = []
        self.visited = []
        self.api = API()

    def search(self, game):
        # queue is a list of pair of "game instance" & "action list"
        self.queue.append(game)

        # TODO remove
        prev_head = 0

        while self.queue:
            node = self.queue.pop(0)

            # TODO REMOVE
            print(node.get_head())
            if prev_head != node.get_head():
                prev_head = node.get_head()
                node.print_space()

            valid_actions = self.api.valid_actions(node)

            random.shuffle(valid_actions)

            for action in valid_actions:
                child_node = self.api.copy_game(node)
                self.api.evolve(child_node, action)

                # if self.is_visited(child_node):
                #     continue

                self.queue.append(child_node)

                if self.api.is_victory(child_node):
                    print("BFS search successful.")

    # def is_visited(self, node):
    #     # implement
    #     for visited_node in self.visited:
    #         if self.api.is_space_match(visited_node, node):
    #             return True
    #     return False

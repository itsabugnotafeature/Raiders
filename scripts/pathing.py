import random


class PathManager:

    def __init__(self, grid):

        self.grid = grid

        # Each monster that has a path is keyed to the index of their progress along their path
        self.path_index_dict = {}

        # All paths stored as lists of two dimensional tuples keyed to their respective monsters
        self.master_path_dict = {}

    def add_monster(self, monster, path=None):
        if path is not None:
            self.path_index_dict[monster] = 0
            self.master_path_dict[monster] = path
        else:
            self.generate_random_path(monster)

    def generate_path(self, monster, length=6, repetitions=0):

        pos = monster.pos
        final_path = [pos]
        num_repetitions = 0
        for i in range(length-1):
            neighbors = self.grid.neighbors(pos)
            for j in range(len(neighbors)):
                r = random.randint(0, len(neighbors)-1)
                if neighbors[r] in final_path:
                    if num_repetitions < repetitions or len(neighbors) == 1:
                        num_repetitions += 1
                        final_path.append(neighbors[r])
                        break
                    else:
                        neighbors.remove(neighbors[r])
                else:
                    final_path.append(neighbors[r])
                    break
            pos = final_path[-1]

        self.path_index_dict[monster] = 0
        self.master_path_dict[monster] = final_path
        return final_path

    def generate_random_path(self, monster, length=6):

        keep_running = 1
        pos = monster.pos
        path = [pos]
        while keep_running or len(path) < 2:
            neighbors = self.grid.neighbors(pos)
            r = random.randint(0, len(neighbors)-1)
            new_pos = neighbors[r]
            path.append(new_pos)
            pos = new_pos
            keep_running = random.randint(0, length-2)

        self.path_index_dict[monster] = 0
        self.master_path_dict[monster] = path
        return path

    def get_next_step(self, monster):
        try:
            if monster.pos == self.master_path_dict[monster][self.path_index_dict[monster]]:
                # Has it reached the end of the path
                if monster.pos == self.master_path_dict[monster][-1]:
                    self.path_index_dict[monster] = 1
                    self.master_path_dict[monster].reverse()
                else:
                    self.path_index_dict[monster] += 1
        except KeyError:
            print("Error in PathManager: {} not found".format(str(monster)))
            return False
        return self.master_path_dict[monster][self.path_index_dict[monster]]

    def contains_sprite(self, sprite):
        if self.master_path_dict.get(sprite):
            return True
        return False

    def set_index(self, sprite, index):
        self.path_index_dict[sprite] = min(len(self.master_path_dict[sprite])-1, index)

    def reverse_path(self, monster):
        self.path_index_dict[monster] = len(self.master_path_dict[monster]) + 1 - self.path_index_dict[monster]
        self.master_path_dict[monster].reverse()

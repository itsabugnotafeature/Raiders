import queue
from math import sqrt


class grid:

    def __init__(self, cols, rows, walls):
        self.cols = cols
        self.rows = rows
        self.walls = walls
        self.sprites = []

    def neighbors(self, spot):
        neighbors = []
        removal = []
        neighbors.append((spot[0] - 1, spot[1]))  # Left
        neighbors.append((spot[0] + 1, spot[1]))  # Right
        neighbors.append((spot[0], spot[1] - 1))  # Up
        neighbors.append((spot[0], spot[1] + 1))  # Down
        #        neighbors.append((spot[0]-1, spot[1]+1)) #Left Down
        #       neighbors.append((spot[0]-1, spot[1]-1)) #Left Up             Uncomment this for diagonals
        #        neighbors.append((spot[0]+1, spot[1]+1)) #Right Down
        #        neighbors.append((spot[0]+1, spot[1]-1)) #Right Up

        for spot in neighbors:
            if not (0 <= spot[0] < self.cols) or not (0 <= spot[1] < self.rows):
                removal.append(spot)
            if spot in self.walls:
                if spot not in removal:
                    removal.append(spot)
        for spot in removal:
            neighbors.remove(spot)
        return neighbors

    def inbounds(self, spot):
        if not (0 <= spot[0] < self.cols) or not (0 <= spot[1] < self.rows):
            return False
        else:
            return True

    def wpush(self, wall):
        self.walls.append(wall)

    def wpop(self, wall):
        self.walls.remove(wall)

    def pureneighbors(self, spot):
        neighbors = [(spot[0] - 1, spot[1]), (spot[0] + 1, spot[1]), (spot[0], spot[1] - 1), (spot[0], spot[1] + 1)]
        return neighbors

    def pureaoe(self, spot):
        neighbors = [(spot[0] - 1, spot[1]), (spot[0] + 1, spot[1]), (spot[0], spot[1] - 1), (spot[0], spot[1] + 1),
                     (spot[0] - 1, spot[1] + 1), (spot[0] - 1, spot[1] - 1), (spot[0] + 1, spot[1] + 1),
                     (spot[0] + 1, spot[1] - 1)]
        return neighbors

    def print(self):
        string_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if (j, i) not in self.walls:
                    string_list.append("+ ")
                else:
                    string_list.append("[]")
        for i in range(self.rows):
            print(string_list[i*8:(i+1)*8])


def heuristic(spot, goal, pathing_type="euc"):
    if pathing_type == "man":
        h = abs(spot[0] - goal[0]) + abs(spot[1] - goal[1])
    else:
        h = sqrt((abs(spot[0] - goal[0]) ** 2) + (abs(spot[1] - goal[1]) ** 2))
    return h


def a_star(start, goal, grid):
    if not grid.inbounds(start) or not grid.inbounds(goal):
        raise Exception("Bad inputs to the astar grid.")

    frontier = queue.PriorityQueue()
    frontier.put((heuristic(start, goal), start))

    came_from = {start: None}

    distance = {start: 0}

    current = None
    best_path = [start]

    while not frontier.empty():
        temp_path = []
        current = frontier.get()
        path_step = current[1]
        temp_path.insert(0, path_step)

        for next_spot in grid.neighbors(current[1]):
            if next_spot not in came_from:
                frontier.put((heuristic(next_spot, goal), next_spot))
                came_from[next_spot] = current[1]
                distance[next_spot] = distance[current[1]] + 1
        while not path_step == start:
            temp_path.insert(0, came_from[path_step])
            path_step = came_from[path_step]
        if heuristic(temp_path[-1], goal) < heuristic(best_path[-1], goal):
            best_path = temp_path[:]

        if current[1] == goal:
            return best_path

    if not current[1] == goal:
        return best_path

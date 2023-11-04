import uuid
import heapq
import time

class Enemy:
    def __init__(self, world):
        self.last_moved = 0
        self.id = uuid.uuid4()
        self.world = world
        self.speed = 1 # actions per second
        self.x = 0
        self.y = 0
        self.current_path = None
        self.steps_since_updated = 0

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if self.__can_move(direction[0],direction[1]):
            self.set_location(direction[0],direction[1])


    def __can_move(self, x, y):
        # Check if the enemy can move to the position (x, y)
        return 0 <= x < self.world.width and 0 <= y < self.world.height and self.world.tiles[x][y].tile_type == 'air'

    def __find_path(self, start, goal):
        if self.world.is_wall(*goal):
            return []  # Early exit if goal is a wall

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        neighbors = lambda x, y: [(x+dx, y+dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                                  if not self.world.is_wall(x+dx, y+dy)]

        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        open_set = []
        heapq.heappush(open_set, (f_score[start], start))
        came_from = {}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Reverse path

            for neighbor in neighbors(*current):
                tentative_g_score = g_score[current] + 1  # Assuming cost of 1 for each step
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        a = 1235
        return []  # Return empty path if no path is found

    def act(self):
        time_since_last_move = time.time() - self.last_moved
        if time_since_last_move < 1 / self.speed:
            return
        if self.current_path is not None:
            if len(self.current_path) == 0:
                self.current_path = None
                return
            next_step = self.current_path.pop(0)

            self.move(next_step)

        self.last_moved = time.time()

    def goto_location(self, x, y):
        # Determine what the enemy does on its turn
        if self.steps_since_updated > 1 or self.current_path is None:
            self.current_path = self.__find_path((self.x, self.y), (x, y))
            self.steps_since_updated = 0
        self.steps_since_updated += 1


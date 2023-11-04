import random
from opensimplex import OpenSimplex
import numpy as np
from enemy import Enemy

class DungeonMaster:
    def __init__(self, seed=None):
        self.noise_gen = OpenSimplex(seed=seed if seed is not None else random.randint(0, 1000))
        self.noise_scale = 10
        self.world = None

    def create(self, world):
        noise_map = self.generate_noise_map(world)
        self.create_walls(world, noise_map)
        self.world = world

    def generate_noise_map(self, world):
        noise_map = np.zeros((world.width, world.height))
        center_x, center_y = world.width // 2, world.height // 2
        for x in range(world.width):
            for y in range(world.height):
                noise_map[x][y] = self.calculate_scaled_noise_value(x, y, center_x, center_y, world)
        return noise_map

    def calculate_scaled_noise_value(self, x, y, center_x, center_y, world):
        dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        amplitude = max(0.1, 1 - (dist / max(center_x, center_y)) ** 2)
        nx = x / world.width
        ny = y / world.height
        return self.noise_gen.noise2(nx * self.noise_scale, ny * self.noise_scale) * amplitude

    def create_walls(self, world, noise_map):
        threshold = np.percentile(noise_map, 99)  # top 1% values

        for x in range(world.width):
            for y in range(world.height):
                if noise_map[x][y] >= threshold:
                    self.create_wall(world, x, y)

    def create_wall(self, world, x, y):
        length = random.randint(3, 10)  # Wall length of 3-10 tiles
        com = self.get_center_of_mass(world)
        last_x, last_y = None, None  # To keep track of the last wall location

        for _ in range(length):
            if 0 <= x < world.width and 0 <= y < world.height and world.tiles[x][y].tile_type == 'air':
                if not self.has_adjacent_walls(world, x, y, last_x, last_y):
                    world.tiles[x][y].tile_type = 'wall'
                    last_x, last_y = x, y
                    direction = self.get_direction_away_from_com(x, y, com) if com else random.choice(['up', 'down', 'left', 'right'])

                    if direction == 'up': y -= 1
                    elif direction == 'down': y += 1
                    elif direction == 'left': x -= 1
                    elif direction == 'right': x += 1
                else:
                    break
            else:
                break

    def get_center_of_mass(self, world):
        total_x, total_y, count = 0, 0, 0
        for x in range(world.width):
            for y in range(world.height):
                if world.tiles[x][y].tile_type == 'wall':
                    total_x += x
                    total_y += y
                    count += 1
        if count > 0:
            return total_x / count, total_y / count
        return None

    def has_adjacent_walls(self, world, x, y, last_x, last_y):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions: left, right, up, down
        for dx, dy in directions:
            adj_x, adj_y = x + dx, y + dy
            if (adj_x, adj_y) == (last_x, last_y):
                continue  # Ignore the last wall location
            if 0 <= adj_x < world.width and 0 <= adj_y < world.height:
                if world.tiles[adj_x][adj_y].tile_type == 'wall':
                    return True
        return False

    def get_direction_away_from_com(self, x, y, com):
        if not com:
            return random.choice(['up', 'down', 'left', 'right'])

        vector_to_com = (com[0] - x, com[1] - y)
        possible_directions = []

        if vector_to_com[0] > 0:
            possible_directions.append('left')
        elif vector_to_com[0] < 0:
            possible_directions.append('right')

        if vector_to_com[1] > 0:
            possible_directions.append('up')
        elif vector_to_com[1] < 0:
            possible_directions.append('down')

        return random.choice(possible_directions) if possible_directions else 'up'

    def create_enemy_at_edge_of_map(self):
        # List to store potential spawn locations
        potential_spawns = []

        # Check top and bottom edges
        for x in range(self.world.width):
            if self.world.tiles[x][0].tile_type == 'air':  # Top edge
                potential_spawns.append((x, 0))
            if self.world.tiles[x][self.world.height - 1].tile_type == 'air':  # Bottom edge
                potential_spawns.append((x, self.world.height - 1))

        # Check left and right edges
        for y in range(self.world.height):
            if self.world.tiles[0][y].tile_type == 'air':  # Left edge
                potential_spawns.append((0, y))
            if self.world.tiles[self.world.width - 1][y].tile_type == 'air':  # Right edge
                potential_spawns.append((self.world.width - 1, y))

        # Ensure there is at least one potential spawn
        if not potential_spawns:
            raise Exception("No available spawn locations on the map edges.")

        # Randomly choose a spawn location
        spawn_location = random.choice(potential_spawns)

        if len(spawn_location) > 0:
            newEnemy = Enemy(self.world)
            newEnemy.set_location(spawn_location[0], spawn_location[1])
            self.world.enemies.append(newEnemy)  # Assuming the World class has a list of enemies




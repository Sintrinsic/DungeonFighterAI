# world.py
import random
import pygame
import math
from opensimplex import OpenSimplex
import numpy as np
class Tile:
    def __init__(self, x, y, size=50, tile_type='air'):
        self.x = x
        self.y = y
        self.size = size
        self.tile_type = tile_type
        self.rect = pygame.Rect(x * size, y * size, size, size)

class World:
    def __init__(self, width, height, tile_size):
        self.width = width // tile_size
        self.height = height // tile_size
        self.tile_size = tile_size
        self.tiles = [[Tile(x, y, tile_size) for y in range(self.height)] for x in range(self.width)]


        self.total_tiles = self.width * self.height
        self.noise_gen = OpenSimplex(0)
        self.noise_scale = 10
        self.wall_tiles = 0
        self.noise_map = self.generate_noise_map()
        self.create_walls()

    def generate_noise_map(self):
        noise_map = np.zeros((self.width, self.height))
        center_x, center_y = self.width // 2, self.height // 2
        for x in range(self.width):
            for y in range(self.height):
                # Calculate the distance from the center to reduce noise amplitude with distance
                dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                amplitude = max(0.1, 1 - (dist / max(center_x, center_y)) ** 2)

                # Generate the noise value
                nx = x / self.width
                ny = y / self.height
                noise_value = self.noise_gen.noise2(nx * self.noise_scale, ny * self.noise_scale)

                noise_map[x][y] = noise_value * amplitude
        return noise_map


    def create_walls(self):
        # Set a threshold for the top noise values that will become walls
        threshold = np.percentile(self.noise_map, 99)  # top 5% values

        for x in range(self.width):
            for y in range(self.height):
                if self.noise_map[x][y] >= threshold:
                    self.create_wall(x, y)

    def get_center_of_mass(self):
        total_x, total_y, count = 0, 0, 0
        for row in self.tiles:
            for tile in row:
                if tile.tile_type == 'wall':
                    total_x += tile.x
                    total_y += tile.y
                    count += 1
        if count > 0:
            return total_x / count, total_y / count
        return None

    def get_direction_away_from_com(self, x, y, com):
        # Calculate vector from current position to center of mass
        vector_to_com = (com[0] - x, com[1] - y)
        possible_directions = []

        if vector_to_com[0] > 0: possible_directions.append('left')
        elif vector_to_com[0] < 0: possible_directions.append('right')

        if vector_to_com[1] > 0: possible_directions.append('up')
        elif vector_to_com[1] < 0: possible_directions.append('down')

        if possible_directions:
            return random.choice(possible_directions)
        return random.choice(['up', 'down', 'left', 'right'])

    def has_adjacent_walls(self, x, y, last_x, last_y):
        # Check for adjacent walls, ignoring the last wall location
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions: left, right, up, down
            adj_x, adj_y = x + dx, y + dy
            if (adj_x, adj_y) == (last_x, last_y):
                continue  # Ignore the last wall location
            if 0 <= adj_x < self.width and 0 <= adj_y < self.height:
                if self.tiles[adj_x][adj_y].tile_type == 'wall':
                    return True
        return False

    def create_wall(self, x, y):
        length = random.randint(3, 10)  # Wall length of 3-5 tiles
        com = self.get_center_of_mass()
        last_x, last_y = None, None  # To keep track of the last wall location

        for _ in range(length):
            if 0 <= x < self.width and 0 <= y < self.height and self.tiles[x][y].tile_type == 'air':
                if not self.has_adjacent_walls(x, y, last_x, last_y):
                    self.tiles[x][y].tile_type = 'wall'
                    # Record the current position as the last wall location
                    last_x, last_y = x, y
                    # Decide the direction for the next tile in the wall
                    direction = self.get_direction_away_from_com(x, y, com) if com else random.choice(['up', 'down', 'left', 'right'])

                    if direction == 'up': y -= 1
                    elif direction == 'down': y += 1
                    elif direction == 'left': x -= 1
                    elif direction == 'right': x += 1
                else:
                    break  # Stop if adjacent to another wall not counting the last wall position
            else:
                break  # Stop if out of bounds or at a wall


    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                color = (128, 128, 128) if self.tiles[x][y].tile_type == 'wall' else (255, 255, 255)
                pygame.draw.rect(screen, color, self.tiles[x][y].rect)


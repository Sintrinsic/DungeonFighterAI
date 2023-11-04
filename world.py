import pygame
from player import Player
import random

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
        self.enemies = []
        self.player = None
        self.total_tiles = self.width * self.height
        self.noise_scale = 10
        self.wall_tiles = 0


    def spawn_player(self, player):
        self.player = player
        if player.world != self:
            player.world = self
        while True:
            # Generate random coordinates within the world bounds
            random_x = random.randint(0, self.width - 1)
            random_y = random.randint(0, self.height - 1)

            # Check if the randomly chosen tile is not a wall
            if self.tiles[random_x][random_y].tile_type != 'wall':
                # Set player's location to these coordinates
                player.set_location(random_x, random_y)
                break

    def is_wall(self,x,y):
        try:
            return self.tiles[x][y].tile_type == 'wall'
        except:
            return False

    def is_enemy(self,x,y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return True
        return False

    def is_player(self,x,y):
        return self.player.x == x and self.player.y == y

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.is_player(x,y):
                    color = (0, 128, 128)
                elif self.is_enemy(x,y):
                    color = (190, 0, 0)
                elif self.is_wall(x,y):
                    color = (128, 128, 128)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, self.tiles[x][y].rect)


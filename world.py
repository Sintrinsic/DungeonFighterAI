import pygame
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
        self.noise_scale = 10
        self.wall_tiles = 0

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                color = (128, 128, 128) if self.tiles[x][y].tile_type == 'wall' else (255, 255, 255)
                pygame.draw.rect(screen, color, self.tiles[x][y].rect)


import pygame

class Player:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
        self.direction = 'up'  # Initial direction is 'up'
        self.alive = True

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def move(self, input_key):
        if input_key == 'w' and self.can_move(self.x, self.y - 1):
            self.y -= 1
            self.direction = 'up'
        elif input_key == 's' and self.can_move(self.x, self.y + 1):
            self.y += 1
            self.direction = 'down'
        elif input_key == 'a' and self.can_move(self.x - 1, self.y):
            self.x -= 1
            self.direction = 'left'
        elif input_key == 'd' and self.can_move(self.x + 1, self.y):
            self.x += 1
            self.direction = 'right'
        self.check_for_enemies()

    def can_move(self, x, y):
        # Check if the player can move to the position (x, y)
        return 0 <= x < self.world.width and 0 <= y < self.world.height and self.world.tiles[x][y].tile_type != 'wall'

    def check_for_enemies(self):
        # Placeholder for enemy interaction logic
        # Here you would iterate over enemies and determine if any are in the 'front' of the player
        # If an enemy is in front of the player and moving towards the player, it would be 'killed'
        pass



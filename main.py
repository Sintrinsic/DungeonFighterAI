# main.py
import pygame
import sys
from world import World
from dungeon_master import DungeonMaster
import time
from player import Player

# Initialize the world and dungeon master


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

last_spawn_time = 0
spawn_interval = 3  # seconds

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame 2D Game")
clock = pygame.time.Clock()

# Create a World instance
world = World(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
player = Player(world)

dungeon_master = DungeonMaster()
# Populate the world with walls
dungeon_master.create(world)

def main():
    last_spawn_time = 0
    spawn_interval = 3  # seconds
    world.spawn_player(player)

    dungeon_master.create_enemy_at_edge_of_map()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Determine which key was pressed
                if event.key == pygame.K_w:
                    player.move('w')
                elif event.key == pygame.K_s:
                    player.move('s')
                elif event.key == pygame.K_a:
                    player.move('a')
                elif event.key == pygame.K_d:
                    player.move('d')

        # Game logic goes here
        current_time = time.time()

        for enemy in world.enemies:
            enemy.goto_location(player.x, player.y)
            enemy.act()

        if current_time - last_spawn_time >= spawn_interval:
            # It's time to spawn a new enemy
            last_spawn_time = current_time




        # Render
        screen.fill((255, 255, 255))  # Fill the screen with white background
        world.draw(screen)  # Draw the world map with walls

        # After drawing everything, flip the display
        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

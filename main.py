# main.py
import pygame
import sys
from world import World

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame 2D Game")
clock = pygame.time.Clock()

# Create a World instance
world = World(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic goes here

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

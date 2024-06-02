import pygame
import json

pygame.init()

# Define constants
TILE_SIZE = 25
GRID_WIDTH = 97
GRID_HEIGHT = 20

# Define screen size
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Level Editor')

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define initial world data with all zeros
world_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Function to draw the grid and tiles
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if world_data[row][col] == 1:
                pygame.draw.rect(screen, GREEN, rect)
            elif world_data[row][col] == 2:
                pygame.draw.rect(screen, BLUE, rect)
            elif world_data[row][col] == 3:
                pygame.draw.rect(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Main loop
running = True
current_tile = 1

while running:
    screen.fill(WHITE)
    draw_grid()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tile = 1
            elif event.key == pygame.K_2:
                current_tile = 2
            elif event.key == pygame.K_3:
                current_tile = 3
            elif event.key == pygame.K_s:
                # Save the world data to a file
                with open('world_data.json', 'w') as f:
                    json.dump(world_data, f)
            elif event.key == pygame.K_l:
                # Load the world data from a file
                with open('world_data.json', 'r') as f:
                    world_data = json.load(f)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            col = pos[0] // TILE_SIZE
            row = pos[1] // TILE_SIZE
            if col < GRID_WIDTH and row < GRID_HEIGHT:
                world_data[row][col] = current_tile

        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            col = pos[0] // TILE_SIZE
            row = pos[1] // TILE_SIZE
            if col < GRID_WIDTH and row < GRID_HEIGHT:
                world_data[row][col] = 0

    pygame.display.update()

pygame.quit()
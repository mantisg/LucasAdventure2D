import pygame
import json

pygame.init()

# Define constants
TILE_SIZE = 25
GRID_WIDTH = 100
GRID_HEIGHT = 30

# Define screen size
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600

#Define starting views
view_x = 0
view_y = 0
mouse_x, mouse_y = pygame.mouse.get_pos()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Level Editor')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load sprites
dirt_img = pygame.image.load('assets/luca_dirt.png')
grass_img = pygame.image.load('assets/luca_grass.png')
cloud1_img = pygame.image.load('assets/cloud1.png')
blob_img = pygame.image.load('assets/kenney_platformer-art-deluxe/Extra animations and enemies/Enemy sprites/spider.png')
platform_x_img = pygame.image.load('assets/kenney_platformer-art-deluxe/Base pack/Tiles/grassHalf.png')
coin_img = pygame.image.load('assets/kenney_platformer-art-deluxe/Base pack/Items/coinGold.png')

sprites = [None, dirt_img, grass_img, cloud1_img, blob_img, platform_x_img, coin_img]

# Define initial world data with all zeros
world_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Define zoom variables
zoom = 1.0
zoom_step = 0.1
min_zoom = 0.6
max_zoom = 2.0

# Function to draw the grid and tiles
def draw_grid():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            # Calculate the position and size of each tile based on the zoom level
            tile_size_zoomed = TILE_SIZE * zoom
            x = col * tile_size_zoomed
            y = row * tile_size_zoomed
            rect = pygame.Rect(x, y, tile_size_zoomed, tile_size_zoomed)
            tile_value = world_data[row][col]
            if tile_value > 0:
                sprite = pygame.transform.scale(sprites[tile_value], (tile_size_zoomed, tile_size_zoomed))
                screen.blit(sprite, (x, y))
            pygame.draw.rect(screen, WHITE, rect, 1)

# Function to draw sprite selection
def draw_sprite_selection():
    y_offset = SCREEN_HEIGHT - TILE_SIZE
    for i, sprite in enumerate(sprites[1:], start=1):
        x = (i - 1) * TILE_SIZE
        screen.blit(pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE)), (x, y_offset))
        pygame.draw.rect(screen, BLACK, (x, y_offset, TILE_SIZE, TILE_SIZE), 1)

# Main loop
running = True
current_tile = 1

while running:
    screen.fill(BLACK)
    draw_grid()
    draw_sprite_selection()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # Save the world data to a file
                with open('world_data.json', 'w') as f:
                    json.dump(world_data, f)
            elif event.key == pygame.K_l:
                # Load the world data from a file
                with open('world_data.json', 'r') as f:
                    world_data = json.load(f)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Update mouse position here
            world_x = (mouse_x - view_x) / zoom
            world_y = (mouse_y - view_y) / zoom

            if event.button == 4:  # Scroll up
                prev_zoom = zoom
                zoom = min(max_zoom, zoom + zoom_step)
                # Adjust view to keep cursor position fixed
                view_x += (mouse_x - view_x) * (prev_zoom / zoom - 1)
                view_y += (mouse_y - view_y) * (prev_zoom / zoom - 1)
            elif event.button == 5:  # Scroll down
                prev_zoom = zoom
                zoom = max(min_zoom, zoom - zoom_step)
                # Adjust view to keep cursor position fixed
                view_x += (mouse_x - view_x) * (prev_zoom / zoom - 1)
                view_y += (mouse_y - view_y) * (prev_zoom / zoom - 1)
            elif event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                if pos[1] >= SCREEN_HEIGHT - TILE_SIZE:
                    # Clicked on sprite selection
                    selected_sprite_index = pos[0] // TILE_SIZE + 1
                    if 1 <= selected_sprite_index < len(sprites):
                        current_tile = selected_sprite_index
                else:
                    # Clicked on grid
                    col = int(pos[0] / (TILE_SIZE * zoom))
                    row = int(pos[1] / (TILE_SIZE * zoom))
                    if col < GRID_WIDTH and row < GRID_HEIGHT:
                        world_data[row][col] = current_tile
            elif event.button == 3:  # Right click
                pos = pygame.mouse.get_pos()
                col = int(pos[0] / (TILE_SIZE * zoom))
                row = int(pos[1] / (TILE_SIZE * zoom))
                if col < GRID_WIDTH and row < GRID_HEIGHT:
                    world_data[row][col] = 0

    pygame.display.update()

pygame.quit()
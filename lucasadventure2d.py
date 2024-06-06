import pygame as pg
from pygame.locals import *
from world import World
from player import Player
from camera import Camera
from level_select import LevelSelect
import map

pg.init()

clock = pg.time.Clock()
fps = 60

screen_width = 900
screen_height = 800

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Luca's Adventure")

# Game Vars
tile_size = 100

# Images
sun_img_og = pg.image.load('assets/luca_sun.png')
sun_img = pg.transform.rotozoom(sun_img_og, 0, 0.3)
bg_img = pg.image.load('assets/luca_sky.png')

level_select = LevelSelect(screen)
player = None
world = None
camera = None

# Game Runtime
run = True
in_level = False
scroll = 0
while run:
    clock.tick(fps)

    if not in_level:
        level_select.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                selected_level = level_select.get_level_at_pos(pg.mouse.get_pos())
                if selected_level:
                    world_data = map.load_level(f'levels/{selected_level}')
                    world = World(world_data)
                    player = Player(200, 1800)
                    camera = Camera(screen_width, screen_height)
                    in_level = True

    else:
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 25))

        world.draw_world(screen, camera)
        player.update(world)
        camera.update(player)
        player.draw(screen, camera)
                
        world.coin_collision(player.rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

    pg.display.update()

pg.quit()

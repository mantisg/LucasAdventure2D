import pygame as pg
from pygame.locals import *
from world import World
from player import Player
from map import world_data
from camera import Camera

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

player = Player(200, 1800)
world = World(world_data)
camera = Camera(screen_width, screen_height)

# Game Runtime
run = True
scroll = 0
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 25))

    world.draw_world(screen, camera)
    player.update(world)
    camera.update(player)
    player.draw(screen, camera)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.update()

pg.quit()

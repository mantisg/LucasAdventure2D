import pygame as pg
import random

class World:
    def __init__(self, data):
        self.tile_list = []
        self.tile_size = 100

        dirt_img = pg.image.load('assets/luca_dirt.png')
        grass_img = pg.image.load('assets/luca_grass.png')
        cloud_imgs = [
            pg.image.load('assets/cloud1.png'),
            pg.image.load('assets/cloud2.png'),
            pg.image.load('assets/cloud3.png'),
            pg.image.load('assets/cloud4.png')
        ]
        blob_img = pg.image.load('assets/kenney_platformer-art-deluxe/Extra animations and enemies/Enemy sprites/spider.png')
        platform_x_img = pg.image.load('assets/kenney_platformer-art-deluxe/Base pack/Tiles/grassHalf.png')
        coin_img = pg.image.load('assets/kenney_platformer-art-deluxe/Base pack/Items/coinGold.png')

        row_count = 0
        for row in data:
            column_count = 0
            for tile in row:
                if tile == 0:
                    tile = (None, None, 0)
                    self.tile_list.append(tile)
                if tile == 1:
                    dirt = pg.transform.scale(dirt_img, (self.tile_size, self.tile_size))
                    dirt_rect = dirt.get_rect()
                    dirt_rect.x = column_count * self.tile_size
                    dirt_rect.y = row_count * self.tile_size
                    dirt_rect.inflate_ip(-20, -10)
                    tile = (dirt, dirt_rect, 1)  # Include tile type
                    self.tile_list.append(tile)
                if tile == 2:
                    grass = pg.transform.scale(grass_img, (self.tile_size, self.tile_size))
                    grass_rect = grass.get_rect()
                    grass_rect.x = column_count * self.tile_size
                    grass_rect.y = row_count * self.tile_size
                    grass_rect.inflate_ip(-20, -10)
                    tile = (grass, grass_rect, 2)  # Include tile type
                    self.tile_list.append(tile)
                if tile == 3:
                    cloud = random.choice(cloud_imgs)
                    cloud_rect = cloud.get_rect()
                    cloud_rect.x = column_count * self.tile_size
                    cloud_rect.y = row_count * self.tile_size
                    tile = (cloud, cloud_rect, 3)  # Include tile type
                    self.tile_list.append(tile)
                if tile == 4:
                    spider = pg.transform.scale(blob_img, (self.tile_size, self.tile_size))
                    spider_rect = spider.get_rect()
                    spider_rect.x = column_count * self.tile_size
                    spider_rect.y = row_count * self.tile_size
                    spider_rect.inflate_ip(-20, -10)
                    tile = (spider, spider_rect, 4)
                    self.tile_list.append(tile)
                if tile == 5:
                    platform = pg.transform.scale(platform_x_img, (self.tile_size, self.tile_size))
                    platform_rect = platform.get_rect()
                    platform_rect.x = column_count * self.tile_size
                    platform_rect.y = row_count * self.tile_size
                    platform_rect.inflate_ip(-20, -10)
                    tile = (platform, platform_rect, 5)
                    self.tile_list.append(tile)
                if tile == 6:
                    coin = pg.transform.scale(coin_img, (self.tile_size, self.tile_size))
                    coin_rect = coin.get_rect()
                    coin_rect.x = column_count * self.tile_size
                    coin_rect.y = row_count * self.tile_size
                    coin_rect.inflate_ip(-20, -10)
                    tile = (coin, coin_rect, 6)
                    self.tile_list.append(tile)
                column_count += 1
            row_count += 1

    def draw_world(self, screen, camera):
        for tile in self.tile_list:
            if tile[2] != 0:
                screen.blit(tile[0], camera.apply(tile[1]))
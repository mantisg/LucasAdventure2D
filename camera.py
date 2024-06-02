import pygame as pg

class Camera:
    def __init__(self, screen_width, screen_height):
        self.camera_rect = pg.Rect(0, 0, screen_width, screen_height)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, rect):
        return rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + self.screen_width // 2
        y = -target.rect.centery + self.screen_height // 2

        self.camera_rect = pg.Rect(x, y, self.screen_width, self.screen_height)
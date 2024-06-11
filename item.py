from cmath import rect
import pygame as pg

class Item():
    def __init__(self, img, img_rect, x, y, item_id):
        self.img = img
        self.img_rect = img_rect
        self.img_rect.x = x
        self.img_rect.y = y
        self.id = item_id
        
    def collect_coin(self, player_rect):
        return self.img_rect.colliderect(player_rect)
    
    def box_collision(self, player_rect):
        return self.img_rect.colliderect(player_rect)
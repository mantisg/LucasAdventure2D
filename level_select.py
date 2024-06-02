import pygame as pg
import os

class LevelSelect:
    def __init__(self, screen):
        self.screen = screen
        self.levels = []
        self.load_levels()
        self.font = pg.font.SysFont('Arial', 30)

    def load_levels(self):
        self.levels = [f for f in os.listdir('levels') if f.endswith('.json')]

    def draw(self):
        self.screen.fill((0, 0, 0))
        for i, level in enumerate(self.levels):
            text = self.font.render(f'Level {i + 1}: {level}', True, (255, 255, 255))
            self.screen.blit(text, (50, 50 + i * 40))

    def get_level_at_pos(self, pos):
        for i, level in enumerate(self.levels):
            text_rect = pg.Rect(50, 50 + i * 40, 200, 40)
            if text_rect.collidepoint(pos):
                return level
        return None
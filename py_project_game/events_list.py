import time
from typing import Any

import pygame
from sprites_group import event_group, player_shot_group
from load_image import load_image


class BoomCrash(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, *groups: event_group):
        super().__init__(*groups)
        self.screen = screen
        self.image = load_image('sprites/boom.png', -1)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time = time.time()
        self.life_time = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.time + self.life_time < time.time():
            event_group.remove(self)


class LiteShotBoom(BoomCrash):
    def __init__(self, screen, x, y, *groups: (event_group, player_shot_group)):
        super().__init__(screen, x, y, *groups)
        self.image = load_image('sprites/liteshotboom.png', -1)
        self.life_time = 0.2


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, screen,  x, y, columns=5, rows=3):
        super().__init__(event_group)
        self.sheet = load_image('sprites_animated/boom_ship.png')
        self.screen = screen
        self.frames = []
        self.cut_sheet(self.sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.time = time.time()
        self.life_time = 1
        self.time_fps = time.time()
        self.time_step = 0.1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.time_fps + self.time_step < time.time():
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.time_fps = time.time()
        if self.time + self.life_time < time.time():
            event_group.remove(self)


crash_ship = []
crash_shot = []
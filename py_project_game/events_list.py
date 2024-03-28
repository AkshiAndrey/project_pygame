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


crash_ship = []
crash_shot = []
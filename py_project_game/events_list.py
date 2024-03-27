import time
from typing import Any

import pygame
from sprites_group import event_group
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


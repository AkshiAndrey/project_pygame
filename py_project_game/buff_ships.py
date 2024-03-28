import random
import time
from typing import Any

import pygame
from load_image import load_image
from sprites_group import all_sprites, neutral_group, player_group, enemy_group, event_group, player_shot_group
import events_list


class Ship(pygame.sprite.Sprite):

    def __init__(self, screen, game, *groups: neutral_group):
        """Инициализация корабля"""
        super().__init__(*groups)
        self.screen = screen
        self.game = game
        self.image = load_image('sprites/ship.png', -1)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.score_point = 10
        self.hit_point = 1
        self.damage = 0

    def render(self):
        """Рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update(self, x, y):
        """Смещение центра корабля в координаты"""
        self.rect.centerx = x
        self.rect.centery = y

    def score_up(self):
        self.game.game_score += self.score_point


class HpBonus(Ship):
    def __init__(self, screen, game):
        super().__init__(screen, game, neutral_group)
        self.image = load_image('sprites/ship_e.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centery += 1
        pass


class RapidFire(Ship):
    def __init__(self, screen, game):
        super().__init__(screen, game, neutral_group)
        self.image = load_image('sprites/ship_e.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centery += 1
        pass

buff_ships = {'HpBonus': 20, "RapidFire": 0.2}
buff_ships_class_list = [HpBonus, RapidFire, RapidFire, RapidFire]
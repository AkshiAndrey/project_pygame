import random
import time
from typing import Any

import pygame
from load_image import load_image
from sprites_group import all_sprites, neutral_group, player_group, enemy_group, event_group
import events_list


class Ship(pygame.sprite.Sprite):

    def __init__(self, screen, *groups: all_sprites):
        """Инициализация корабля"""
        super().__init__(*groups)
        self.screen = screen
        self.image = load_image('sprites/ship.png', -1)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def render(self):
        """Рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update(self, x, y):
        """Смещение центра корабля в координаты"""
        self.rect.centerx = x
        self.rect.centery = y


class PlayerShip(Ship):

    def __init__(self, screen):
        """Инициализация корабля"""
        super().__init__(screen, player_group)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - self.rect.height // 2 + 1
        self.speed = 22
        self.time = time.time()
        self.timer = time.time()

    def render(self):
        """Рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update(self, x, y):
        self.timer += 0.1
        if self.timer - self.time > 5:
            self.speed += 1
            self.time += 5
        """Смещение центра корабля в координаты"""
        shiftx = self.rect.centerx - x
        shifty = self.rect.centery - y
        if shifty or shiftx:
            if shiftx == 0:
                pass
            elif abs(shiftx) > self.speed:
                if shiftx > 0:
                    self.rect.centerx -= self.speed
                else:
                    self.rect.centerx += self.speed
            else:
                self.rect.centerx = x

            if abs(shifty) > self.speed:
                if shifty > 0:
                    self.rect.centery -= self.speed
                else:
                    self.rect.centery += self.speed
            else:
                self.rect.centery = y
        crash = pygame.sprite.spritecollide(self, enemy_group, True)
        if crash:
            event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))


class EnemyShip(Ship):
    def __init__(self, screen):
        super().__init__(screen, enemy_group)
        self.image = load_image('sprites/ship_e.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centerx -= random.choice([1, 2, 3, 4, -1, - 2, -3, -4, 0])
        self.rect.centery += 1
        pass



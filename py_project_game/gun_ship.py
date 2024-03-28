import random
import time
from typing import Any

import pygame
from load_image import load_image
from sprites_group import all_sprites, neutral_group, player_group, enemy_group, event_group, player_shot_group
import buff_ships
import events_list


class Ship(pygame.sprite.Sprite):

    def __init__(self, screen, game, *groups: all_sprites):
        """Инициализация корабля"""
        super().__init__(*groups)
        self.screen = screen
        self.game = game
        self.image = load_image('sprites/ship.png', -1)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.score_point = 1
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


class PlayerShip(Ship):

    def __init__(self, screen, game):
        """Инициализация корабля"""
        super().__init__(screen, player_group)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - self.rect.height // 2 + 1
        self.game = game
        self.speed = 10
        self.rapid_fire = 1
        self.time_shot = time.time()
        self.timer_shot = time.time()
        self.hit_point = 50


    def render(self):
        """Рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update(self, x, y):
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
            crash[0].score_up()
            self.hit_point -= crash[0].damage
            if crash[0].__class__ in ship_list:
                event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
            elif crash[0].__class__ in shot_list:
                event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
        crash = pygame.sprite.spritecollide(self, neutral_group, True)
        if crash:
            for ship in crash:
                self.upgrade_ship(ship)
        self.game.hit_point = self.hit_point

    def shot_event(self):
        if self.timer_shot - self.time_shot > self.rapid_fire:
            LitePlayerShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()

    def upgrade_ship(self, ship):
        if 'Hp' in ship.__class__.__name__:
            self.hit_point += buff_ships.buff_ships[ship.__class__.__name__]
        if 'Fire' in ship.__class__.__name__:
            self.rapid_fire = max(self.rapid_fire - buff_ships.buff_ships[ship.__class__.__name__], 0.1)
            self.game.rapid_fire = self.rapid_fire
        pass

    def upgrade_stats(self):
        pass


class EnemyShip(Ship):
    def __init__(self, screen, game):
        super().__init__(screen, game, enemy_group)
        self.image = load_image('sprites/ship_e.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5
        self.score_point = 5
        self.time_shot = time.time() - 2
        self.timer_shot = time.time()
        self.rapid_fire = 5
        self.hit_point = 5
        self.damage = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centerx -= random.choice([1, 2, 3, 4, -1, - 2, -3, -4, 0])
        self.rect.centery += 1
        self.shot_event()
        pass

    def shot_event(self):
        if self.timer_shot - self.time_shot > self.rapid_fire:
            LiteEnemyShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()


class LitePlayerShot(Ship):
    """Легкий выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_1.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 2
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centery -= 10
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0] in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])
        pass


class LiteEnemyShot(Ship):
    """Легкий выстрел противника"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, enemy_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_2.png')
        self.rect.centerx = self.player_ship.rect.centerx
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 1

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.centery += 3
        if self.rect.centery >= self.screen.get_height():
            event_group.remove(self)
            return


class MediumEnemyShot(LiteEnemyShot):
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, pl_ship)
        self.damage = 5


class HardEnemyShot(LiteEnemyShot):
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, pl_ship)
        self.damage = 15

ship_list = [EnemyShip]
shot_list = [LiteEnemyShot, HardEnemyShot, MediumEnemyShot]
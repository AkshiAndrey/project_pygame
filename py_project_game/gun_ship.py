import random
import time
from typing import Any

import pygame
from load_image import load_image
from sprites_group import all_sprites, neutral_group, player_group, enemy_group, event_group, player_shot_group
import buff_ships
import events_list


class Ship(pygame.sprite.Sprite):
    """Базовый класс корабля"""

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
    """Класс корабля персонажа"""

    def __init__(self, screen, game):
        """Инициализация корабля"""
        super().__init__(screen, player_group)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - self.rect.height // 2 + 1
        self.game = game
        self.speed = 5
        self.rapid_fire = 1
        self.time_shot = time.time()
        self.timer_shot = time.time()
        self.hit_point = 50
        self.guns = 9



    def render(self):
        """Рисование корабля"""
        self.screen.blit(self.image, self.rect)

    def update(self, x, y):
        """Обновления статуса """
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
        # Столкновения с врагами
        crash = pygame.sprite.spritecollide(self, enemy_group, True)
        if crash:
            crash[0].score_up()
            self.hit_point -= crash[0].damage
            if crash[0].__class__.__name__ in ship_list:
                event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
            elif crash[0].__class__.__name__ in shot_list:
                event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
        # Столкновения с бафами
        crash = pygame.sprite.spritecollide(self, neutral_group, True)
        if crash:
            for ship in crash:
                self.upgrade_ship(ship)
        self.game.hit_point = self.hit_point

    def shot_event(self):
        """Выстрел"""
        if self.timer_shot - self.time_shot > self.rapid_fire:
            print(self.guns)
            if 4 > self.guns >= 1:
                LitePlayerShot(self.screen, self.game, self)
            if 5 > self.guns >= 2:
                LitePlayerShot2(self.screen, self.game, self)
            if 6 > self.guns >= 3:
                LitePlayerShot3(self.screen, self.game, self)
                LitePlayerShot4(self.screen, self.game, self)
            if 7 > self.guns >= 4:
                MediumPlayerShot(self.screen, self.game, self)
            if 7 > self.guns >= 5:
                MediumPlayerShot2(self.screen, self.game, self)
            if 8 > self.guns >= 6:
                MediumPlayerShot3(self.screen, self.game, self)
                MediumPlayerShot4(self.screen, self.game, self)
            if self.guns >= 7:
                HardPlayerShot(self.screen, self.game, self)
            if self.guns >= 8:
                HardPlayerShot2(self.screen, self.game, self)
                HardPlayerShot3(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()

    def upgrade_ship(self, ship):
        """Поднятие бафа"""
        if 'Hp' in ship.__class__.__name__:
            self.hit_point += buff_ships.buff_ships[ship.__class__.__name__]
        if 'Fire' in ship.__class__.__name__:
            # прокачка орудий
            if self.guns < 8:
                if self.rapid_fire == 0.1:
                    self.guns += 1
                    self.rapid_fire = 0.6
                    self.game.rapid_fire = self.rapid_fire
                    return
                else:
                    self.rapid_fire = max(self.rapid_fire - buff_ships.buff_ships[ship.__class__.__name__], 0.1)
                    self.game.rapid_fire = self.rapid_fire
            elif self.rapid_fire > 0.1 and self.guns == 9:
                self.rapid_fire = max(self.rapid_fire - buff_ships.buff_ships[ship.__class__.__name__], 0.1)
                self.game.rapid_fire = self.rapid_fire
            else:
                self.guns += 0.5

        if 'Sp' in ship.__class__.__name__:
            self.speed += buff_ships.buff_ships[ship.__class__.__name__]
        pass


# Классы выстрелов игрока
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
        """Логика базового выстрела игрока"""
        self.rect.centery -= 10
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])
        pass


class LitePlayerShot2(Ship):
    """Второе орудиe"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_1.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 4
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 10
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])


class LitePlayerShot3(Ship):
    """Второе орудиe"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_1.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 4
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 10
        self.rect.centerx += 10
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])


class LitePlayerShot4(Ship):
    """Второе орудиe"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_1.png')
        self.rect.centerx = self.player_ship.rect.centerx
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 10
        self.rect.centerx -= 10
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])


class MediumPlayerShot(Ship):
    """Средний выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_3.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 2
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика среднего выстрела игрока"""
        self.rect.centery -= 15
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


class MediumPlayerShot2(Ship):
    """Средний выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_3.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 4
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика среднего выстрела игрока"""
        self.rect.centery -= 15
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


class MediumPlayerShot3(Ship):
    """Средний выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_3.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 4
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика среднего выстрела игрока"""
        self.rect.centery -= 15
        self.rect.centerx += 15
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


class MediumPlayerShot4(Ship):
    """Средний выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_3.png')
        self.rect.centerx = self.player_ship.rect.centerx
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика среднего выстрела игрока"""
        self.rect.centery -= 15
        self.rect.centerx -= 15
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


class HardPlayerShot(Ship):
    """Легкий выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_5.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 3
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 1 + self.player_ship.guns

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 15
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            # event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            # player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])
        pass

class HardPlayerShot2(Ship):
    """Легкий выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_5.png')
        self.rect.centerx = self.player_ship.rect.centerx + self.player_ship.rect.w // 4
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5 + self.player_ship.guns

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 15
        self.rect.centerx += 15
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            # event_group.add(events_list.LiteShotBoom(self.screen, self.rect.centerx, self.rect.top))
            # player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])
        pass


class HardPlayerShot3(Ship):
    """Легкий выстрел игрока"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, player_shot_group)
        self.player_ship = pl_ship
        self.image = load_image('sprites/shot_5.png')
        self.rect.centerx = self.player_ship.rect.centerx
        self.rect.centery = self.player_ship.rect.centery + 20
        self.damage = 5 + self.player_ship.guns

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Логика базового выстрела игрока"""
        self.rect.centery -= 15
        self.rect.centerx -= 15
        crash = pygame.sprite.spritecollide(self, enemy_group, False)
        if crash:
            # player_shot_group.remove(self)
            crash[0].hit_point -= self.damage
            if crash[0].hit_point <= 0:
                crash[0].score_up()
                if crash[0].__class__.__name__ in ship_list:
                    event_group.add(events_list.BoomCrash(self.screen, *crash[0].rect.center))
                enemy_group.remove(crash[0])
        pass


# Классы вражеских кораблей
class EnemyShip(Ship):
    """Простейший корабль противника"""
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
        """Обновление"""
        self.rect.centerx -= random.choice([1, 2, 3, 4, -1, - 2, -3, -4, 0])
        self.rect.centery += 1
        self.shot_event()
        pass

    def shot_event(self):
        """Стрельба корабля"""
        if self.timer_shot - self.time_shot > self.rapid_fire:
            LiteEnemyShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()


class EnemyShip1(Ship):
    """Простейший корабль противника"""
    def __init__(self, screen, game):
        super().__init__(screen, game, enemy_group)
        self.image = load_image('sprites/ship_e1.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5
        self.score_point = 15
        self.time_shot = time.time() - 2
        self.timer_shot = time.time()
        self.rapid_fire = 2.5
        self.hit_point = 10
        self.damage = 8

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Обновление"""
        self.rect.centery += 2
        self.shot_event()
        pass

    def shot_event(self):
        """Стрельба корабля"""
        if self.timer_shot - self.time_shot > self.rapid_fire:
            MediumEnemyShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()


class EnemyShip2(Ship):
    """Простейший корабль противника"""
    def __init__(self, screen, game):
        super().__init__(screen, game, enemy_group)
        self.image = load_image('sprites/fire_ship.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5
        self.score_point = 5
        self.time_shot = time.time() - 2
        self.timer_shot = time.time()
        self.rapid_fire = 0.5
        self.hit_point = 20
        self.damage = 10

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Обновление"""
        self.rect.centery += 1
        self.shot_event()
        pass

    def shot_event(self):
        """Стрельба корабля"""
        if self.timer_shot - self.time_shot > self.rapid_fire:
            MediumEnemyShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()

class EnemyShip3(Ship):
    """Простейший корабль противника"""
    def __init__(self, screen, game):
        super().__init__(screen, game, enemy_group)
        self.image = load_image('sprites/kamikaze.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5
        self.score_point = 5
        self.time_shot = time.time() - 2
        self.timer_shot = time.time()
        self.rapid_fire = 5
        self.hit_point = 5
        self.damage = 20

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Обновление"""
        self.rect.centery += 20
        pass


class EnemyShip4(Ship):
    """Простейший корабль противника"""
    def __init__(self, screen, game):
        super().__init__(screen, game, enemy_group)
        self.image = load_image('sprites/base_boss1.png', -1)
        self.rect.centerx = random.randint(0, self.screen_rect.w)
        self.rect.top = self.screen_rect.top + 5
        self.score_point = 2000
        self.time_shot = time.time() - 2
        self.timer_shot = time.time()
        self.rapid_fire = 2
        self.hit_point = 5000
        self.damage = 5000

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Обновление"""
        self.rect.centery += 1
        self.shot_event()
        pass

    def shot_event(self):
        """Стрельба корабля"""
        if self.timer_shot - self.time_shot > self.rapid_fire:
            MediumEnemyShot(self.screen, self.game, self)
            self.time_shot = time.time()
        self.timer_shot = time.time()



# Классы выстрелов противника
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
        """Логика стрельбы противника, базовый снаряд"""
        self.rect.centery += 3
        if self.rect.centery >= self.screen.get_height():
            event_group.remove(self)
            return


class MediumEnemyShot(LiteEnemyShot):
    """улучшенный снаряд противника"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, pl_ship)
        self.damage = 5


class HardEnemyShot(LiteEnemyShot):
    """Топовый снаряд противника"""
    def __init__(self, screen, game, pl_ship):
        super().__init__(screen, game, pl_ship)
        self.hit_point = 20000
        self.damage = 10


ship_list = ['EnemyShip', 'EnemyShip', 'EnemyShip', 'EnemyShip', 'EnemyShip', 'EnemyShip']
shot_list = ['LiteEnemyShot', 'HardEnemyShot', 'MediumEnemyShot']
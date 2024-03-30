import random
import sys
import time

import pygame
from sprites_group import list_all, enemy_group
from gun_ship import EnemyShip, EnemyShip1, EnemyShip2, EnemyShip3, EnemyShip4

import buff_ships


class Game:
    def __init__(self, screen):
        self.pl_name = ''
        self.status = True
        self.sprites_group = list_all
        self.hard_lvl = 0
        self.hard_lvl_list = [i for i in range(1, 1000000)]
        self.enemy_speed_spawn = 95
        self.screen = screen
        self.game_score = 0
        self.hit_point = 50
        self.time_bonus = time.time()
        self.timer_bonus = time.time()
        self.bonus_time = 6
        self.rapid_fire = 1
        self.speed = 5
        self.enemy_pool = [EnemyShip] * 10
        self.enemy_pool += [EnemyShip1] * 3
        self.enemy_pool += [EnemyShip1, EnemyShip1, EnemyShip] * 3
        self.enemy_pool += [EnemyShip1, EnemyShip2] * 3
        self.enemy_pool += [EnemyShip1, EnemyShip2, EnemyShip1, EnemyShip3] * 4
        self.enemy_pool += [EnemyShip2, EnemyShip1, EnemyShip2, EnemyShip3] * 4
        self.enemy_pool += [EnemyShip2, EnemyShip4, EnemyShip3, EnemyShip3] * 2

    def update(self):
        """Обновление сложности и спавн врагов"""
        self.hard_lvl = self.hard_lvl_list.index(1 + self.game_score // 300)
        for i in range(1 + 1 * self.hard_lvl):
            self.enemy_spawn()
        if self.timer_bonus - self.time_bonus > self.bonus_time:
            random.choice(buff_ships.buff_ships_class_list)(self.screen, self)
            self.time_bonus = time.time()
        self.timer_bonus = time.time()

        # print(self.game_score)
        if self.hit_point <= 0:
            self.end_game()

    def enemy_spawn(self):
        '''Спавн врагов от скорости'''
        if self.enemy_speed_spawn == 200:
            self.enemy_speed_spawn = 0
            start = min(5, self.hard_lvl)
            stop = min(self.hard_lvl + 10, 68)
            index = random.choice(range(start, stop))
            if len(enemy_group) < 400:
                self.enemy_pool[index](self.screen, self)
        elif self.enemy_speed_spawn < 200:
            self.enemy_speed_spawn += 2 + min(self.hard_lvl // 50, 50)
        else:
            self.enemy_speed_spawn = 200

    def render_score(self):
        font_color = (200, 10, 10)
        font = pygame.font.Font(None, 20)
        text = font.render(f'SCORE ({self.game_score})', 1, font_color)
        self.screen.blit(text, (30, 30))

    def render_hit(self):
        font_color = (10, 200, 10)
        font = pygame.font.Font(None, 20)
        text = font.render(f'HP ({self.hit_point})', 1, font_color)
        self.screen.blit(text, (30, 60))

    def render_rapid(self):
        font_color = (10, 10, 200)
        font = pygame.font.Font(None, 20)
        text = font.render(f'attack speed ({round(1 / self.rapid_fire, 1)})', 1, font_color)
        self.screen.blit(text, (30, 90))

    def render_speed(self):
        font_color = (10, 200, 200)
        font = pygame.font.Font(None, 20)
        text = font.render(f'speed ({self.speed})', 1, font_color)
        self.screen.blit(text, (30, 120))

    def render(self):
        self.render_rapid()
        self.render_hit()
        self.render_score()
        self.render_speed()

    def end_game(self):
        self.status = False

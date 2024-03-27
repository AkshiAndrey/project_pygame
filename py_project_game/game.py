import pygame
from sprites_group import list_all
from gun_ship import EnemyShip, PlayerShip


class Game:
    def __init__(self, screen):
        self.sprites_group = list_all
        self.hard_lvl = 0
        self.hard_lvl_list = [i for i in range(1, 1000000)]
        self.enemy_speed_spawn = 95
        self.screen = screen
        self.game_score = 5

    def update(self):
        """Обновление счета и сложности"""
        self.game_score += len(self.sprites_group[0])
        self.hard_lvl = self.hard_lvl_list.index(1 + self.game_score // 100)
        print(self.hard_lvl)
        self.enemy_spawn()

    def enemy_spawn(self):
        '''Спавн врагов'''
        if self.enemy_speed_spawn == 100:
            self.enemy_speed_spawn = 0
            EnemyShip(self.screen)
        elif self.enemy_speed_spawn < 100:
            self.enemy_speed_spawn += 2
        else:
            self.enemy_speed_spawn = 100

    def render_score(self):
        font_color = (50, 50, 50)
        font = pygame.font.Font(None, 20)
        text = font.render(f'SCORE ({self.game_score})', 1, font_color)
        self.screen.blit(text, (30, 30))


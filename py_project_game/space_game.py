
import pygame
import sys
import sprites_group
from game import Game
from start_screen import start_screen
from final_screen import final_screen
from load_image import load_image
from gun_ship import PlayerShip


list_all = sprites_group.list_all


def clear_sprite_scrap(wind_height):
    global list_all
    for group in list_all[:-1]:
        for sprite in group:
            if 0 > sprite.rect.centery or sprite.rect.centery > wind_height:
                group.remove(sprite)


def main():
    WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
    FPS = 60

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('data/main_track.mp3')
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    window_rect = pygame.Rect((0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    fon = pygame.transform.scale(load_image('data/sprites/main_fon.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    fon_y = 0
    pygame.display.set_caption("HellCosmoBattle")
    clock = pygame.time.Clock()

    game = Game(screen)
    while True:
        game.status = True
        start_screen(screen, game=game)

        player_gun_ship = PlayerShip(screen, game)
        prev_mouse_pos = player_gun_ship.rect.center

        while game.status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()

            mx, my = pygame.mouse.get_pos()
            if not window_rect.collidepoint(mx, my):
                mx = min(max(window_rect.left, mx), window_rect.right - 1)
                my = min(max(window_rect.top, my), window_rect.bottom - 1)
                pygame.mouse.set_pos((mx, my))

            # Стрельба игрока
            if pygame.mouse.get_pressed()[0]:
                player_gun_ship.shot_event()

            # Обновление позиции игрока
            current_mouse_pos = pygame.mouse.get_pos()
            if current_mouse_pos != prev_mouse_pos:
                prev_mouse_pos = current_mouse_pos
            player_gun_ship.update(*current_mouse_pos)

            #Анимация фона
            fon_y += 2
            if fon_y > WINDOW_HEIGHT:
                fon_y = 0

            # Отрисовка фона
            screen.blit(fon, (0, fon_y))
            screen.blit(fon, (0, fon_y - WINDOW_HEIGHT))

            # Обновление и отрисовка спрайтов
            sprites_group.event_group.update()
            sprites_group.enemy_group.update()
            sprites_group.player_shot_group.update()
            sprites_group.neutral_group.update()
            sprites_group.event_group.draw(screen)
            sprites_group.enemy_group.draw(screen)
            sprites_group.player_shot_group.draw(screen)
            sprites_group.neutral_group.draw(screen)
            player_gun_ship.render()
            game.render()
            clear_sprite_scrap(WINDOW_HEIGHT)
            # Обновление статуса игры
            game.update()

            pygame.display.flip()
            clock.tick(FPS)
        final_screen(screen, game=game)


if __name__ == "__main__":
    main()

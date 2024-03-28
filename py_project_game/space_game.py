import pygame
import sys
import sprites_group
from game import Game

from gun_ship import PlayerShip


def main():
    WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
    FPS = 60

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Косможуки")
    clock = pygame.time.Clock()

    game = Game(screen)
    player_gan_ship = PlayerShip(screen, game)
    prev_mouse_pos = player_gan_ship.rect.center

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Стрельба игрока
        if pygame.mouse.get_pressed()[0]:
            player_gan_ship.shot_event()

        # Обновление статуса игры
        game.update()

        # Обновление позиции спрайта
        current_mouse_pos = pygame.mouse.get_pos()
        if current_mouse_pos != prev_mouse_pos:
            prev_mouse_pos = current_mouse_pos
        player_gan_ship.update(*current_mouse_pos)
        screen.fill((0, 0, 0))

        # Обновление и отрисовка спрайтов
        sprites_group.event_group.update()
        sprites_group.enemy_group.update()
        sprites_group.player_shot_group.update()
        sprites_group.neutral_group.update()
        sprites_group.event_group.draw(screen)
        sprites_group.enemy_group.draw(screen)
        sprites_group.player_shot_group.draw(screen)
        sprites_group.neutral_group.draw(screen)
        player_gan_ship.render()
        game.render_score()
        game.render_live()
        game.render_rapid()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.quit()
    sys.exit()


if __name__ == "__main__":
    main()

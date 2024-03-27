import pygame
import sys
import os
import sprites_group

from gun_ship import PlayerShip, EnemyShip
# from load_image import load_image

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
FPS = 60



def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Косможуки")
    clock = pygame.time.Clock()
    gun = PlayerShip(screen)
    prev_mouse_pos = gun.rect.center
    e_gan = EnemyShip(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_mouse_pos = pygame.mouse.get_pos()
        if current_mouse_pos != prev_mouse_pos:
            prev_mouse_pos = current_mouse_pos

        # Обновление позиции спрайта
        gun.update(*current_mouse_pos)
        screen.fill((0, 0, 0))
        gun.render()
        sprites_group.enemy_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.display.quit()
    sys.exit()


if __name__ == "__main__":
    main()


import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

prev_mouse_pos = (0, 0)

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Проверяем изменение позиции мыши
    current_mouse_pos = pygame.mouse.get_pos()
    if current_mouse_pos != prev_mouse_pos:
        prev_mouse_pos = current_mouse_pos
    print("Mouse position:", current_mouse_pos)

    # Другие операции цикла игры
    screen.fill((255, 255, 255))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
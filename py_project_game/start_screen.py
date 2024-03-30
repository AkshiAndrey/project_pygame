import sys

import pygame

from load_image import load_image


def start_screen(screen, width=1200, height=800, clock=pygame.time.Clock(), fps=60, game=None):
    BLACK = (0, 0, 0)
    input_text = ''
    input_rect = pygame.Rect(700, 235, 300, 50)
    with open('table_score.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()
    text = [i.strip().split() for i in text]

    while True:
        intro_text = ["СПАСАЙ ПЛАНЕТУ",
                      "МОЧИ СУПОСТАТОВ",
                      "Спасай беженцев и получай усиления корабля,",
                      "Твой подвиг не будет забыт"]

        fon = pygame.transform.scale(load_image('sprites/start_fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('fonts/Donpoligrafbum-Bold.otf', 20)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('#28343E'))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 150
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            string_rendered = font.render('Введи свое имя боец!', 1, pygame.Color(BLACK))
            intro_rect = string_rendered.get_rect()
            text_coord += 5
            intro_rect.top = text_coord
            intro_rect.x = 200
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            string_rendered = font.render('Лучшие имперские штурмовики', 1, pygame.Color('#7d2826'))
            intro_rect = string_rendered.get_rect()
            text_coord += 30
            intro_rect.top = text_coord
            intro_rect.x = 300
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font('fonts/SAIBA-45-Regular-(v1.1).otf', 40)
        for line in text:
            string_rendered = font.render(' : '.join(line), 1, pygame.Color('#7d2826'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 400
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text:
                        game.pl_name = input_text
                        return
                    else:
                        input_text = 'SuperHero'
                        game.pl_name = input_text
                        return
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if input_text:
                    game.pl_name = input_text
                    return
                else:
                    input_text = 'SuperHero'
                    game.pl_name = input_text
                    return


        pygame.draw.rect(screen, pygame.Color(BLACK), input_rect, 3)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 1200))
    pygame.display.set_caption("Косможуки")
    start_screen(screen)

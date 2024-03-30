import sys

import pygame

from load_image import load_image


def final_screen(screen, width=1200, height=800, clock=pygame.time.Clock(), fps=60, game=None):
    with open('table_score.txt', 'r', encoding='utf-8') as file:
        text = file.readlines()
    text = [i.strip().split() for i in text]
    text = [[i[0], int(i[1])] for i in text]
    while True:
        intro_text = ["Истребив полчища врагов",
                      "Ты приблизил империю к победе",
                      ' '.join(('Обратив врагов в', str(game.game_score), 'тон')), 'обломков и космического мусора',
                      "Твой подвиг не будет забыт"]

        fon = pygame.transform.scale(load_image('data/sprites/final_fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font('data/fonts/Donpoligrafbum-Bold.otf', 20)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('red'))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 100
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        else:
            font = pygame.font.Font('data/fonts/Donpoligrafbum-Bold.otf', 20)
            string_rendered = font.render('  :  '.join(('Итоговый счет:', str(game.game_score))), 1,
                                          pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 200
            screen.blit(string_rendered, intro_rect)

            font = pygame.font.Font('data/fonts/Donpoligrafbum-Bold.otf', 20)
            string_rendered = font.render('Лучшие имперские штурмовики', 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 50
            intro_rect.top = text_coord
            intro_rect.x = 300
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font('data/fonts/SAIBA-45-Regular-(v1.1).otf', 40)
        for line in text:
            string_rendered = font.render(' : '.join((line[0], str(line[1]))), 1, pygame.Color('#7d2826'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 400
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                text[-1] = [game.pl_name, game.game_score]
                text.sort(key=lambda x: x[1], reverse=True)
                with open('table_score.txt', 'w', encoding='utf-8') as file:
                    for score in text:
                        file.writelines(' '.join((score[0], str(score[1]) + '\n')))
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    text[-1] = [game.pl_name, game.game_score]
                    text.sort(key=lambda x: x[1], reverse=True)
                    with open('table_score.txt', 'w', encoding='utf-8') as file:
                        for score in text:
                            file.writelines(' '.join((score[0], str(score[1]) + '\n')))
                    game.game_score = 0
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                text[-1] = [game.pl_name, game.game_score]
                text.sort(key=lambda x: x[1], reverse=True)
                with open('table_score.txt', 'w', encoding='utf-8') as file:
                    for score in text:
                        file.writelines(' '.join((score[0], str(score[1]) + '\n')))
                game.game_score = 0
                return

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 1200))
    pygame.display.set_caption("Косможуки")
    final_screen(screen)

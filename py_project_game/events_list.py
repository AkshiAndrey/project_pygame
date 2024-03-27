import pygame
from sprites_group import event_group


class BoomCrash(pygame.sprite.Sprite):
    def __init__(self, *groups: event_group):
        super().__init__(*groups)

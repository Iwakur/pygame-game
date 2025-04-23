import pygame


class Item(pygame.sprite.Sprite):

    def __init__(self, surface, x, y):
        """
        Simple Sprite class for on-screen things
        """
        super().__init__()
        self.image = surface
        self.rect = surface.get_rect()
        self.rect.x = x
        self.rect.y = y

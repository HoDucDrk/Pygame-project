import pygame
from load_image import *


class Weapon(pygame.sprite.Sprite):

    def __init__(self, player, groups, type_weapon):
        super().__init__(groups)
        direction = player.status.split('_')[-1]
        self.type_weapon = type_weapon
        self.load_animations_weapon(direction)
        self.index_weapon = 0
        self.image = self.aniamtions_weapon[0]
        if direction == 'right' or direction == 'left':
            if direction == 'right':
                x, y = player.rect.midright
                self.rect = self.image.get_rect(midright=(x, y))
            else:
                x, y = player.rect.midleft
                self.rect = self.image.get_rect(midleft=(x, y))
        else:
            if direction == 'up':
                x, y = player.rect.midtop
                self.rect = self.image.get_rect(midtop=(x, y))
            else:
                x, y = player.rect.midbottom
                self.rect = self.image.get_rect(midbottom=(x, y))

    def load_animations_weapon(self, direction):
        path = f'../Assets/Player/weapons/Frame/{self.type_weapon}/{direction}/'
        images = [pygame.image.load(
            f'../Assets/Player/weapons/Frame/{self.type_weapon}/{direction}/{img}').convert_alpha() for img in load_image(path)]
        self.aniamtions_weapon = [
            pygame.transform.scale2x(img) for img in images]

    def set_delay(self):
        self.index_weapon += 0.15
        if self.index_weapon > len(self.aniamtions_weapon):
            self.index_weapon = 0

    def animate_weapon(self):
        self.image = self.aniamtions_weapon[int(self.index_weapon)]

    def update(self):
        self.set_delay()
        self.animate_weapon()

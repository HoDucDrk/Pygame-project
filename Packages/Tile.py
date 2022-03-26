import pygame
from Setting import *

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, sprite_type, surface=False):
        super().__init__(groups)
        self.sprite_type = sprite_type
        if surface == False:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        else:
            self.image = pygame.image.load(f'../Assets/Tileset/Frame/tile_{surface}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
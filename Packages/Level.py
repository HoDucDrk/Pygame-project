from distutils import debug
from turtle import st
import pygame
from Setting import * 
from Tile import Tile
from Player import Player
from debug import debug
import numpy as np 

class Level:
    
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.create_map()
    
    def create_map(self):
        under_layouts = {
            'blockLayer': load_map('../Assets/Map/data/Map_block_wall.csv'),
            'grass': load_map('../Assets/Map/data/Map_grass.csv'),
            'door': load_map('../Assets/Map/data/Map_door.csv')
        }

        up_layouts = {
            'leaf': load_map('../Assets/Map/data/Map_Leaf.csv'),
        }
        for style, layout in under_layouts.items():
            for i in range(30):
                for j in range(30):
                    if layout[i, j] != -1:
                        x = j * TILESIZE
                        y = i * TILESIZE
                        if style == 'blockLayer':
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if style == 'grass':
                            Tile((x, y), [self.visible_sprites], 'grass', layout[i, j])
                        if style == 'door':
                            Tile((x, y), [self.visible_sprites], 'door', layout[i, j])
                            
        x = 1000
        y = 500
        self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
        
        for style, layout in up_layouts.items():
            for i in range(30):
                for j in range(30):
                    if layout[i, j] != -1:
                        x = j * TILESIZE
                        y = i * TILESIZE
                        if style == 'leaf':
                            Tile((x, y), [self.visible_sprites], 'leaf', layout[i, j])

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #Tạo nền
        self.floor_surf = pygame.image.load('../Assets/Map/Map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #Hiển thị nền 
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
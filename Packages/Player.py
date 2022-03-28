from debug import debug
import pygame
from load_image import load_image
from Setting import *


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacles_sprites, create_attack, destroy_weapon):
        super().__init__(groups)
        self.load_image()
        self.frame_index = 0
        self.status = 'idle_down'
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-216, -204)
        self.fancy = 'down'
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        self.attacking = False 
        self.attack_cooldown = 500
        self.attack_time = None
        self.create_attack = create_attack
        
        self.destroy_weapon = destroy_weapon
        
        self.casting_spell = False
        self.magic_cooldown = 2000
        self.magic_time = None
        
        
        self.obstacles_sprites = obstacles_sprites

        self.weapon_index = 1
        self.weapon = list(weapons_data.keys())[self.weapon_index]
        self.switch_weapon = True
        self.weapon_switch_time = None
        self.switch_weapon_cooldown = 200
        
        #Chỉ số nhân vật 
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 56
        self.speed = self.stats['speed']
        
    def load_image(self):
        path = '../Assets/Player/frame/'
        self.animations = {
            'idle_left': [],
            'idle_up': [],
            'idle_right': [],
            'idle_down': [],
            'walk_left': [],
            'walk_up': [],
            'walk_down': [],
            'walk_right': [],
            'spear_left': [],
            'spear_right': [],
            'spear_up': [],
            'spear_down': [],
            'bow_down': [],
            'bow_left': [],
            'bow_right': [],
            'bow_up': [],
            'cast_spell_left': [],
            'cast_spell_down': [],
            'cast_spell_right': [],
            'cast_spell_up': []
        }
        for animation in self.animations:
            load_animations = [pygame.image.load(
                f'{path}{animation}/{name}').convert_alpha() for name in load_image(f'{path}{animation}')]
            self.animations[animation] = [pygame.transform.scale2x(
                load_animation) for load_animation in load_animations]

    def input(self):
        self.delay = 0.15
        keys = pygame.key.get_pressed()
        
        if not self.attacking and not self.casting_spell:
            # Nhân vật di chuyển theo trục Ox
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.fancy = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.fancy = 'right'
            else:
                self.direction.x = 0
                
        
            # Nhân vật di chuyển theo trục Oy
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.fancy = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.fancy = 'down'
            else:
                self.direction.y = 0
        
        if self.direction == (0, 0): 
            # Nhân vật tấn công
            if keys[pygame.K_q] and not self.attacking:
                self.delay = 0.15
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            #Nhân vật cast spell
            if keys[pygame.K_e] and not self.casting_spell:
                self.delay = 0.5
                self.casting_spell = True
                self.magic_time = pygame.time.get_ticks()
                print('magic')
        
        if keys[pygame.K_TAB] and self.switch_weapon:
            self.switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index += 1 
            if self.weapon_index > 1:
                self.weapon_index = 0
            self.weapon = list(weapons_data.keys())[self.weapon_index]
    
    def get_status(self):
        if self.direction == (0, 0):
            self.status = 'idle_' + self.fancy 
        else:
            self.status = 'walk_' + self.fancy
        
        if self.attacking and self.weapon_index == 0:
            self.status = 'spear_' + self.fancy     
        elif self.attacking and self.weapon_index ==1:
            self.status = 'bow_' + self.fancy   
        if self.casting_spell:
            self.status = 'cast_spell_' + self.fancy
            
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_weapon()
        
        if self.casting_spell:
            if current_time - self.magic_time >= self.magic_cooldown:
                self.casting_spell = False
        
        if not self.switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_weapon_cooldown:
                self.switch_weapon = True
    def set_delay(self):
        self.frame_index += self.delay
        if self.frame_index > len(self.animations[self.status]):
            self.frame_index = 0

    def animate(self, status):
        self.set_delay()
        self.image = self.animations[status][int(self.frame_index)]
        self.status = status
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def move(self, speed):
        if self.direction.magnitude() != 0:  # Trả về độ lớn Euclid của vector
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.cooldowns()
        debug(self.status)
        self.get_status()
        self.animate(self.status)
        self.move(self.speed)

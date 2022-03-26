from debug import debug
import pygame
from load_image import load_image


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacles_sprites):
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
        
        self.obstacles_sprites = obstacles_sprites

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
            'attack_left': [],
            'attack_right': [],
            'attack_up': [],
            'attack_down': [],
            'cast_spell': []
        }
        for animation in self.animations:
            load_animations = [pygame.image.load(
                f'{path}{animation}/{name}').convert_alpha() for name in load_image(f'{path}{animation}')]
            self.animations[animation] = [pygame.transform.scale2x(
                load_animation) for load_animation in load_animations]

    def input(self):
        self.delay = 0.15
        keys = pygame.key.get_pressed()
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
            
        # Nhân vật tấn công
        if keys[pygame.K_SPACE] and not self.attacking:
            self.delay = 1.5
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')
        
        #Nhân vật cast spell
        if keys[pygame.K_q] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack_animation('cast_spell')
            print('attack')
    
    def get_status(self):
        if self.direction == (0, 0):
            self.status = 'idle_' + self.fancy 
        else:
            self.status = 'walk_' + self.fancy
        
        if self.attacking:
            self.status = 'attack_' + self.fancy
            
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                
    def set_delay(self, status):
        print(self.delay)
        self.frame_index += self.delay
        if self.frame_index > len(self.animations[status]):
            self.frame_index = 0
            
    def attack_animation(self):
        if 'attack' in self.status:
            for animation in (self.animations[self.status]):
                print(animation)
            # self.image = animation
        # self.character_direction()

    def animate(self, status):
        self.set_delay(status)
        self.image = self.animations[status][int(self.frame_index)]
        self.status = status
        # self.character_direction()

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
        debug(self.rect)
        self.get_status()
        self.attack_animation()
        self.animate(self.status)
        self.move(self.speed)

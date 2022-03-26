import sys
import pygame
import Setting as Set
from debug import debug
from Level import Level

class Game:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Set.WIDTH, Set.HEIGH))
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.BLACK = (0, 0, 0)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
            
            self.screen.fill(self.BLACK)
            debug('')
            self.level.run()
            self.clock.tick(Set.FPS)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
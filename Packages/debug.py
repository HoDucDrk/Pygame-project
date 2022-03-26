import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(infor, y=10, x=10):
    display_surface = pygame.display.get_surface() #Nhận tham chiếu đến bề mặt hiển thị hiện được thiết lập
    debug_surf = font.render(str(infor), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)
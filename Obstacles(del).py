import pygame
#XDDD, Git and GitHub desktop are kinda good.

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, obsWidth=40, obsHeight=40):
        super().__init__()
        self.image = pygame.Surface((obsWidth, obsHeight))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))

        #bruh
    
    

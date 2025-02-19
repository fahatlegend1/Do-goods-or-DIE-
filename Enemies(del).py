import pygame
import random
import Main
from pyvidplayer2 import Video
enemy_ani1 = Video('player.mp4')
enemy_ani1.set_size(40, 40)

#wWidth, wHeight = 1200, 750


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40, height=40, speed=3):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    
    def move(self, obstacles):
        original_x, original_y = self.rect.x, self.rect.y

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        if pygame.sprite.spritecollide(self, obstacles, False):
            print('Collided!')
            self.rect.x, self.rect.y = original_x, original_y
            self.change_direction()

    def change_direction(self):
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def update(self, obstacles):
        self.move(obstacles)

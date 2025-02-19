import pygame
import Obstacles
import math
import Players
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,target,owner, width=20, height=20, speed=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 100, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.target_x = target[0] + (20)
        self.target_y = target[1] + (20)
        self.angle = Players.Find_angle(x,y,self.target_x,self.target_y)
        self.x = self.rect.x
        self.y = self.rect.y
        self.time = (pygame.time.get_ticks())
        self.dele = self.time + (4000)
        self.owner = owner

        #all_sprites.add(self)
        #bullets.add(self)


    def move(self, obstacles, player, enemies):
        self.x += self.speed * (math.cos(self.angle))
        self.y += self.speed * (math.sin(self.angle))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.remove()
        if self.owner == 'mob':
            if pygame.sprite.spritecollide(self,[player],False):
                self.remove()
                player.hp -=10
        else:
            if pygame.sprite.spritecollide(self,enemies,True):
                self.remove()
        
    def time_out(self):
        if pygame.time.get_ticks() > self.dele:
            self.remove()

    def remove(self):
        #bullets.remove(self)
        #all_sprites.remove(self)
        pass

    def update(self):
        self.move()
        self.time_out()
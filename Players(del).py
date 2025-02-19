import pygame
import math
import Main
import Bullets
from pyvidplayer2 import Video
player_ani = Video('player.mp4')
player_ani.set_size(40, 40)
#wWidth, wHeight = 1200, 750

def MinMax(minNumber, maxNumber, number):
    return min(minNumber, max(maxNumber, number))

def Find_angle(x,y,t_x,t_y):
    angle = math.atan2(t_y-y, t_x-x) #get angle to target in radians
    #print(angle)
    #print('Angle in degrees:', int(angle*180/math.pi))
    #angle_degrees = math.degrees(angle)

    return angle


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width=40, height=40):
        super().__init__()
        self.video = player_ani
        self.video.set_size((width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.hp = 100

    def move(self, keys, obstacles):
        original_x, original_y = self.rect.x, self.rect.y
        #X Dircetion
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if pygame.sprite.spritecollide(self, obstacles, False):
            print('Collided!')
            self.rect.x = original_x

        #Y Direction
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if pygame.sprite.spritecollide(self, obstacles, False):
            print('Collided!')
            self.rect.y = original_y

    
        #Wait to be initialized
        self.rect.x = MinMax(Main.wWidth - self.width , 0, self.rect.x)
        self.rect.y = MinMax(Main.wHeight-self.height, 0, self.rect.y)

    def attack(self):
        if pygame.mouse.get_pressed(3)[0]:
            xy = pygame.mouse.get_pos()
            Bullets.Bullet(self.rect.x, self.rect.y, xy, 'player')    
        
    '''def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)'''
    
    def update(self, keys, obstacles):
        self.move(keys, obstacles)

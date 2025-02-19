import pygame
from pyvidplayer2 import Video
from Players import Player
from Obstacles import Obstacle
from Enemies import Enemy

wWidth, wHeight = 1200, 750
pygame.init()
screen = pygame.display.set_mode((wWidth, wHeight))
pygame.display.set_caption('Do goods or DIE!')

pWidth, pHeight = wWidth // 4, wHeight // 4
player = Player(pWidth, pHeight)

#Obstacles
obstacle1 = Obstacle(600, 375)
obstacle2 = Obstacle(400, 200)

#Enemies
enemy1 = Enemy(800, 500)
enemy2 = Enemy(200, 300)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(obstacle1, obstacle2, enemy1, enemy2)

obstacles = pygame.sprite.Group()
obstacles.add(obstacle1, obstacle2)

enemies = pygame.sprite.Group()
enemies.add(enemy1, enemy2)


running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    #old_x, old_y = player.rect.x, player.rect.y
    '''player.move(keys)
    player.draw(screen)'''
    player.update(keys, obstacles)
    enemies.update(obstacles)

    '''if pygame.sprite.spritecollide(player, obstacles, False):
        print('Collided!')
        player.rect.x, player.rect.y = old_x, old_y'''

    all_sprites.draw(screen)

    pygame.display.flip()
    
pygame.quit()
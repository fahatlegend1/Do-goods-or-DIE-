import pygame as pg
from Load_texture import *
pg.init()

screen = pg.display.set_mode((1200, 600))
pg.display.set_caption('Do Good or DIE!')
clock = pg.time.Clock()
running = True
keys = pg.key.get_pressed()
scene = 0



while running:
          # Cap at 60 FPS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((100,1,1))
        screen.blit(pg.transform.flip(boss_image_group[1],True,False),(300,300))
        
        pg.display.flip()
          
       

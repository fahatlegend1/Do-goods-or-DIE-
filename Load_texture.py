

import pygame as pg
pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\1000_F_489114227_4piH63TD1SsMlOgwH8kr88LirtrueZsc.jpg').convert_alpha()
#back_ground = pg.image.load(r'./placeholder.png').convert_alpha()

background = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

import pygame as pg
pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\background1.jpg').convert_alpha()
background = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\placeholder.png').convert_alpha()
Placholder_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\barrel.jpg').convert_alpha()
Barrel_img = pg.transform.scale(back_ground,(40,40))
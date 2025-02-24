import pygame as pg

from PIL import Image,ImageSequence


pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720
screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))




def loadGIF(filename):
    pilImage = Image.open(r'Assets/Animate'+'/'+filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pg.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
    return frames

def ResizeGIF(frames):
    b = []
    for i in range(len(frames)):
        a = pg.transform.scale(frames[i],(240,240))
        b.append(a)
    return b



boss_image_group = loadGIF('boss.gif')
boss_image_group = ResizeGIF(boss_image_group)


back_ground = pg.image.load(r'Assets\Texture\background1.jpg').convert_alpha()
background = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\placeholder.png').convert_alpha()
Placholder_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\barrel.jpg').convert_alpha()
Barrel_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\bedrock.png').convert_alpha()
bedrock_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\stonebrick.png').convert_alpha()
stonebrick_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\skeleton.jpg').convert_alpha()
skeleton_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\steve.jpg').convert_alpha()
steve_img = pg.transform.scale(back_ground,(35,35))

back_ground = pg.image.load(r'Assets\Texture\Fire_Charge.jpg').convert_alpha()
Fire_Charge_img = pg.transform.scale(back_ground,(25,25))

back_ground = pg.image.load(r'Assets\Texture\game_clear.jpg').convert_alpha()
game_clear_img = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\hp bar\pixil-frame-5.png').convert_alpha()
health_frame_img = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))


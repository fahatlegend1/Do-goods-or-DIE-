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

def ResizeGIF(frames,x,y):
    b = []
    for i in range(len(frames)):
        a = pg.transform.scale(frames[i],(x,y))
        b.append(a)
    return b

def TakeOnly(frames,a):
    b= []
    for i in range(a):
        a = frames[i]
        b.append(a)
    return b


#load gif


boss_image_group = loadGIF('boss_1.gif')
boss_image_group = ResizeGIF(boss_image_group,120,120)
boss_image_group = TakeOnly(boss_image_group,24)



penguin_image_group = loadGIF('penguin.gif')
penguin_image_group = ResizeGIF(penguin_image_group,80,80)

enemy_atk_imahe_group = loadGIF('real_enemy_1.gif')
enemy_atk_imahe_group = ResizeGIF(enemy_atk_imahe_group,40,40)


main_image_group = loadGIF('main_character_3.gif')
main_image_group = ResizeGIF(main_image_group,37,37)

portal_image_group = loadGIF('portal.gif')
portal_image_group = ResizeGIF(portal_image_group,40,40)

drop_image_group = loadGIF('Drop.gif')
drop_image_group = ResizeGIF(drop_image_group,20,20)

#load image


back_ground = pg.image.load(r'Assets\Texture\background1.jpg').convert_alpha()
background = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\placeholder.png').convert_alpha()
Placholder_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\barrel.jpg').convert_alpha()
Barrel_img = pg.transform.scale(back_ground,(40,40))

back_ground = pg.image.load(r'Assets\Texture\IMG_4407.png').convert_alpha()
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

back_ground = pg.image.load(r'Assets\Texture\hp bar\hp bar.png').convert_alpha()
health_frame_img = pg.transform.scale(back_ground,(SCREEN_WIDTH/5.3,SCREEN_HEIGHT/12))

back_ground = pg.image.load(r'Assets\Texture\Story\IMG_1.png').convert_alpha()
story_img_1 = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\Story\IMG_2.png').convert_alpha()
story_img_2 = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\Story\IMG_3.png').convert_alpha()
story_img_3 = pg.transform.scale(back_ground,(SCREEN_WIDTH,SCREEN_HEIGHT))

back_ground = pg.image.load(r'Assets\Texture\photo.png').convert_alpha()
PHOTO = pg.transform.scale(back_ground,(SCREEN_WIDTH/4,SCREEN_HEIGHT/4))



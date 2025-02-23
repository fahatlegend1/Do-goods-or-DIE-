import pygame as pg
import random,math
import sys, subprocess
from Load_texture import *
from General import entity_grid,draw_grid,TILE_SIZE

#change directory to this project file first
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

BULLET_SPEED = 6
BULLET_COOLDOWN = 1500

all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()


def Find_angle(x,y,t_x,t_y):
    angle = math.atan2(t_y-y, t_x-x) #get angle to target in radians
    #print(angle)
    #print('Angle in degrees:', int(angle*180/math.pi))
    #angle_degrees = math.degrees(angle)
    return angle


# Base Sprite class
class BaseSprite(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color,image = Placholder_img):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_shot_time = 0
        self.image.blit(image,(0,0))



class Bullet(BaseSprite):
    def __init__(self, x, y, target, owner, width=15, height=15, speed=BULLET_SPEED, color=(0, 100, 255)):
        super().__init__(x, y, width, height, color)
        
        self.speed = speed
        self.angle = Find_angle(x, y, target[0], target[1])
        self.x = x
        self.y = y
        self.time = pg.time.get_ticks()
        self.dele = self.time + 4000
        self.owner = owner

        # Velocity calculations
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        all_sprites.add(self)
        bullets.add(self)

    def update(self):
        # Move bullet in the calculated direction
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Remove bullets after a certain time
        if pg.time.get_ticks() > self.dele:
            self.kill()
            bullets.remove(self)
        #if (pg.sprite.spritecollideany(self,game.obstacles)) == False:
        if pg.sprite.spritecollide(self,game.obstacles,False):
            t =(pg.sprite.spritecollideany(self,game.obstacles))
            if t.indestructible == True:
                pass
            else:
                pg.sprite.spritecollide(self,game.obstacles,True)
            self.kill()
            bullets.remove(self)
        if pg.sprite.spritecollide(self,[game.player],False): # all player take damage
            if self.owner != game.player:
                self.kill()
                bullets.remove(self)
                game.player.hp -= 10
        if pg.sprite.spritecollide(self,game.enemies,False):
            if self.owner == game.player:
                a =pg.sprite.spritecollideany(self,game.enemies)
                a.kill()
                game.enemies.remove(a)
                self.kill()
                bullets.remove(self)



class Player(BaseSprite):
    def __init__(self, x, y, width=35, height=35,image = Placholder_img):
        super().__init__(x, y, width, height, RED,image)
        self.speed = 3
        self.hp = 100
        self.alive = True
        self.image.blit(image,(0,0))
        

    def move(self, keys, obstacles, screen_width, screen_height):
        if self.alive:
        
            original_x, original_y = self.rect.x, self.rect.y

            # X Direction
            if keys[pg.K_a]:
                self.rect.x -= self.speed
            if keys[pg.K_d]:
                self.rect.x += self.speed

            # Y Direction
            if keys[pg.K_w]:
                self.rect.y -= self.speed
            if keys[pg.K_s]:
                self.rect.y += self.speed

            # Prevent moving outside boundaries or colliding with obstacles
            if (self.rect.left < 0 or self.rect.right > screen_width or
                    self.rect.top < 0 or self.rect.bottom > screen_height or
                    pg.sprite.spritecollide(self, obstacles, False)):
                self.rect.x, self.rect.y = original_x, original_y  # Undo movement

    def attack(self, enemies):
        # Check for collisions with enemies
        collided_enemies = pg.sprite.spritecollide(self, enemies, True)  # True means the will be removed
        if collided_enemies:
            print(f"Attacked and removed {len(collided_enemies)} enemies!")

    def shoot(self):
        if pg.mouse.get_pressed(3)[0] == True:
            current_time = pg.time.get_ticks()
            if current_time - self.last_shot_time > BULLET_COOLDOWN / 2:
                # Create a bullet
                bullet = Bullet(
                    x=self.rect.centerx,
                    y=self.rect.centery,
                    target=pg.mouse.get_pos(),
                    owner=self,
                    speed=BULLET_SPEED*1.15,
                    color=(255, 100, 255)  # Red bullets for enemies
                )
                self.last_shot_time = current_time

    def c_alive(self):
        if self.hp <= 0 :
            self.alive = False
            print('player dead')       

    def update(self, keys, obstacles, enemies, screen_width, screen_height):
        if self.alive:
            self.move(keys, obstacles, screen_width, screen_height)
            self.attack(enemies)  # Check for attacks
            self.c_alive()
            self.shoot()


class Obstacle(BaseSprite):
    def __init__(self, x, y, width=40, height=40,image= Placholder_img,indestructible = False):
        super().__init__(x, y, width, height, GREEN, image)
        self.pos = (x,y)
        self.indestructible = indestructible



class Enemy(BaseSprite):
    def __init__(self, x, y, width=40, height=40, speed=2,bullet_speed = 5,image = Placholder_img):
        super().__init__(x, y, width, height,(0,0,255),image )
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.last_shot_time = 0  # Track the last time the enemy shot a bullet
        self.bullet_speed = bullet_speed
        self.image.blit(image,(0,0))


    def move(self, obstacles, screen_width, screen_height):
        original_x, original_y = self.rect.x, self.rect.y

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Collision with obstacles or screen boundaries
        if (pg.sprite.spritecollide(self, obstacles, False) or
                self.rect.left < 0 or self.rect.right > screen_width or
                self.rect.top < 0 or self.rect.bottom > screen_height):
            self.rect.x, self.rect.y = original_x, original_y
            self.change_direction()

    def change_direction(self):
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def shoot(self, target):
        """Shoot a bullet towards the target."""
        current_time = pg.time.get_ticks()
        if current_time - self.last_shot_time > BULLET_COOLDOWN:
            # Calculate the angle to the target
            angle = Find_angle(self.rect.centerx, self.rect.centery, target[0], target[1])
            # Create a bullet
            bullet = Bullet(
                x=self.rect.centerx,
                y=self.rect.centery,
                target=target,
                owner=self,
                speed=self.bullet_speed,
                color=(255, 0, 0)  # Red bullets for enemies
            )
            self.last_shot_time = current_time

    def update(self, obstacles, screen_width, screen_height, target):
        """Update the enemy's position and handle shooting."""
        self.move(obstacles, screen_width, screen_height)
        self.shoot(target)


num_scene = 0

# Main Game class
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('Do Good or DIE!')
        self.clock = pg.time.Clock()
        self.running = False
        self.keys = pg.key.get_pressed()

        # Initialize sprites
        self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4,image= steve_img)
        self.obstacles = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        

        for i in range(len(entity_grid)):
            if i == 0:
                self.player.rect.x , self.player.rect.y = entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE
                print(i)
            else:
                a =Enemy(entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE,image= skeleton_img)
                self.enemies.add(a)

                

            
        draw_grid(self.screen,Obstacle,self.obstacles,BaseSprite,self.background) #all obstacle

        self.all_sprites = pg.sprite.Group(self.player, *self.obstacles, *self.enemies)

    def run(self):
        self.running = True
        aaa = 0
        while self.running:
            self.clock.tick(60)  # Cap at 60 FPS
            self.handle_events()
            if aaa == 0 :
                self.update()
                self.draw()
            

        pg.quit()
        sys.exit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if self.keys[pg.K_b]:
                back_to_menu()

    def update(self):
        self.keys = pg.key.get_pressed()
        self.player.update(self.keys, self.obstacles, self.enemies, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.enemies.update(self.obstacles, SCREEN_WIDTH, SCREEN_HEIGHT, self.player.rect.center)
        bullets.update()


    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(background,(0,0))
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        bullets.draw(self.screen)  # <- Draw bullets
        self.UI()
        pg.display.flip()
    
    def UI(self):
        pg.draw.rect(self.screen,(255,0,0),pg.Rect(10,10,200,40))
        pg.draw.rect(self.screen,(0,255,0),pg.Rect(10,10,self.player.hp *2,40))

# To Non-san, pls make a button for this function
def back_to_menu():
    subprocess.Popen(['python', 'game_opening.py'])
    pg.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()

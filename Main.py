import pygame as pg
import random,math
import sys, subprocess
from Load_texture import *
from General import *


#change directory to this project file first
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)  
EMPTY = pg.Color(0,0,0,0)

BULLET_SPEED = 6
BULLET_COOLDOWN = 1500
SKILL_COOLDOWN = 4000

all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
SCORE = 0

def Find_angle(x,y,t_x,t_y):
    angle = math.atan2(t_y-y, t_x-x) #get angle to target in radians
    #print(angle)
    #print('Angle in degrees:', int(angle*180/math.pi))
    #angle_degrees = math.degrees(angle)
    return angle


# Base Sprite class
class BaseSprite(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color,image = Placholder_img,gif = False):
        super().__init__()
        self.image = pg.Surface((width, height),pygame.SRCALPHA) # del srcalpha if u wanna see hit box or enable next line of code
        #self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_shot_time = 0
        self.image.blit(image,(0,0))
        self.gif_index = 0
        self.gif = gif
        self.width = width
        self.height = height
        self.fff = 1
        

    def animate(self):
        if self.gif != False:
            self.image.fill(EMPTY)  #change back to empty       #idk what this function d0 anymore
            if self.fff ==0:
                self.gif_index += 1
                self.fff=1
            else:
                self.fff = 0
            if self.gif_index >= len(self.gif):
                self.gif_index = 0
            if game.player.rect.centerx - self.rect.centerx <0:
                self.image.blit(pg.transform.flip(self.gif[self.gif_index],True,False),(-self.width/2,-self.width+40)) 
            else:
                self.image.blit(self.gif[self.gif_index],(-self.width/2 ,-self.width+40)) 

    def animate_real(self):
        if self.gif != False:
            self.image.fill(EMPTY)  #change back to empty
            if self.fff== 0:
                self.gif_index += 1
                self.fff=3
            else:
                self.fff -=1
            if self.gif_index >= len(self.gif):
                self.gif_index = 0
            if game.player.rect.centerx - self.rect.centerx <0:
                self.image.blit(pg.transform.flip(self.gif[self.gif_index],True,False),(0,0)) 
            else:
                self.image.blit(self.gif[self.gif_index],(0 ,0))   
    
    def update(self):
        self.animate_real()
          
            
        


class Bullet(BaseSprite):
    def __init__(self, x, y, target, owner, width=TILE_SIZE/2.5, height=TILE_SIZE/2.5, speed=BULLET_SPEED, color=(0, 100, 255),image = Fire_Charge_img):
        super().__init__(x, y, width, height, color,image)
        self.B_image = pg.transform.scale(image,(width*1.5,height*1.5))
        self.image.blit(image,(-(((width*1.5)-width)),-(((height*1.5)-height))))
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
                #random loot herer
            self.kill()
            bullets.remove(self)
        if pg.sprite.spritecollide(self,[game.player],False): # all player take damage
            if self.owner != game.player:
                self.kill()
                bullets.remove(self)
                game.player.hp -= 10
                game.player.score -=1
        if pg.sprite.spritecollide(self,game.enemies,False):
            if self.owner == game.player:
                a =pg.sprite.spritecollideany(self,game.enemies)
                if a.indestructible == False:
                    a.kill()
                    game.enemies.remove(a)
                    game.player.score +=5
                else:
                    a.hp -=10
                    game.player.score +=5
                self.kill()
                bullets.remove(self)



class Player(BaseSprite):
    def __init__(self, x, y, width=TILE_SIZE-5, height=TILE_SIZE-5,image = Placholder_img):
        super().__init__(x, y, width, height, RED,image)
        self.speed = 3
        self.hp = 100
        self.alive = True
        self.image.blit(image,(0,0))
        self.score =0
        

    def move(self, keys, obstacles, screen_width, screen_height):
        if self.alive:
        
            original_x, original_y = self.rect.x, self.rect.y

            # X Direction
            if keys[pg.K_a]:
                self.rect.x -= self.speed
            if keys[pg.K_d]:
                self.rect.x += self.speed

            # Prevent moving outside boundaries or colliding with obstacles
            if (self.rect.left < 0 or self.rect.right > screen_width or
                    pg.sprite.spritecollide(self, obstacles, False)):
                self.rect.x = original_x # Undo movement

            # Y Direction
            if keys[pg.K_w]:
                self.rect.y -= self.speed
            if keys[pg.K_s]:
                self.rect.y += self.speed

            # Prevent moving outside boundaries or colliding with obstacles
            if (self.rect.top < 0 or self.rect.bottom > screen_height or
                    pg.sprite.spritecollide(self, obstacles, False)):
                self.rect.y =  original_y  # Undo movement

            if pg.sprite.spritecollide(self,game.door,True):
                game.scene += 1
                if game.scene == 5:
                    game.scene = 0
                game.door.empty()
                game.all_sprites.empty()
                # come back here to remove door
                game.gen()
                
                
                

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
    def __init__(self, x, y, width=TILE_SIZE, height=TILE_SIZE,image= Placholder_img,indestructible = False):
        super().__init__(x, y, width, height, GREEN, image)
        self.pos = (x,y)
        self.indestructible = indestructible

class Drop(Obstacle):
    def __init__(self, x, y, width=TILE_SIZE, height=TILE_SIZE, image=Placholder_img, indestructible=True):
        super().__init__(x, y, width, height, image, indestructible)
        self.item_index = random.randint(0,3,1)

#spawn drop neeeeeeeeeeeeeed


class Enemy(BaseSprite):
    def __init__(self, x, y, width=TILE_SIZE, height=TILE_SIZE, speed=2,bullet_speed = 5,image = Placholder_img,indestructible= False,gif = False,bullet_size = TILE_SIZE/2.5):
        super().__init__(x, y, width, height,(0,0,255),image ,gif)
        self.speed = speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.last_shot_time = pg.time.get_ticks() - 100*random.randint(0,10)  # Track the last time the enemy shot a bullet
        self.bullet_speed = bullet_speed
        self.image.blit(image,(0,0))
        self.indestructible = indestructible
        self.hp = 250
        self.bullet_size = bullet_size
        self.last_skill_time = pg.time.get_ticks()
        if width > TILE_SIZE:
            self.boss = True
        else:
            self.boss = False


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

    def c_alive(self):
        if self.hp <= 0 :
            print('boss dead')
            self.kill()     

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
                color=(255, 0, 0),  # Red bullets for enemies
                width= self.bullet_size,
                height= self.bullet_size
            )
            self.last_shot_time = current_time

    def skill(self,target):
        current_time = pg.time.get_ticks()
        if current_time - self.last_skill_time > SKILL_COOLDOWN:
            if random.randint(1,10) <= 8 :
                for i in range(0,int(SCREEN_WIDTH/TILE_SIZE),2):
                    a = i*TILE_SIZE    
                    Bullet(
                        x=a,
                        y=TILE_SIZE*3,
                        target=target,
                        owner=self,
                        speed=self.bullet_speed,
                        color=(255, 0, 0),  # Red bullets for enemies
                        width= self.bullet_size,
                        height= self.bullet_size)
            else:
                for i in range(0,int(SCREEN_WIDTH/TILE_SIZE),2):
                    a = i*TILE_SIZE    
                    Bullet(
                        x=a,
                        y=SCREEN_HEIGHT-TILE_SIZE*3,
                        target=(a,0),
                        owner=self,
                        speed=self.bullet_speed,
                        color=(255, 0, 0),  # Red bullets for enemies
                        width= self.bullet_size,
                        height= self.bullet_size)                        
            
            self.last_skill_time = current_time
                      

    def update(self, obstacles, screen_width, screen_height, target):
        """Update the enemy's position and handle shooting."""
        self.move(obstacles, screen_width, screen_height)
        self.shoot(target)
        self.c_alive()
        self.animate()
        if self.boss == True:
            self.skill(target)
        


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
        self.scene = 2
        
        # Initialize sprites
        self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4,image= steve_img)
        self.obstacles = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.door = pg.sprite.Group()
        self.Animate = pg.sprite.Group()
        

        for i in range(len(entity_grid)):
            if i == 0:
                self.player.rect.x , self.player.rect.y = entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE
  
            elif len(entity_grid) > 1:
                a =Enemy(entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE,image= skeleton_img)
                self.enemies.add(a)
                

                  
        draw_grid(self.screen,Obstacle,self.obstacles,BaseSprite,self.background) #all obstacle

        self.all_sprites = pg.sprite.Group(self.player, *self.obstacles, *self.enemies,*self.Animate)
        
    def gen(self):
        if self.scene == 3:
            generate1()
        else:
            generate()
        if self.scene ==4:
            room_1l()
        global door_grid,entity_grid
        entity_grid,door_grid = get()
        self.obstacles = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.door = pg.sprite.Group()
        self.Animate = pg.sprite.Group()

        if self.scene == 3:
                a =Enemy(entity_grid[1][0]*TILE_SIZE-(TILE_SIZE*2) ,entity_grid[1][1]*TILE_SIZE-(TILE_SIZE*2),height=TILE_SIZE*3,width=TILE_SIZE*3,indestructible=True,gif = boss_image_group,bullet_size= TILE_SIZE/2.5,speed=0)
                self.enemies.add(a)
        elif self.scene == 4:
            a = BaseSprite(SCREEN_WIDTH/2-TILE_SIZE,TILE_SIZE*3,TILE_SIZE*2,TILE_SIZE*2,BLACK,gif = penguin_image_group)
            self.Animate.add(a)

          



        for i in range(len(entity_grid)):
            if i == 0:
                
                self.player.rect.x , self.player.rect.y = entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE
              
            elif len(entity_grid) > 1:
                a =Enemy(entity_grid[i][0]*TILE_SIZE ,entity_grid[i][1]*TILE_SIZE,image= skeleton_img)
                self.enemies.add(a)
                print(self.enemies)
        
        draw_grid(self.screen,Obstacle,self.obstacles,BaseSprite,self.background) #all obstacle

        self.all_sprites = pg.sprite.Group(self.player, *self.obstacles, *self.enemies,*self.Animate)
      

    def game_end(self, win):
        if win == 0:
            subprocess.Popen(['python', 'GameOverScreen.py'])
            print('Game Over')
            pg.quit()
            sys.exit()

        elif win == 1:
            subprocess.Popen(['python', 'GameClearScreen.py'])
            print('Game Clear')
            pg.quit()
            sys.exit()

    def run(self):
        self.running = True
        
        while self.running:
            self.clock.tick(60)  # Cap at 60 FPS
            self.handle_events()
            if self.scene == 0 :
                self.update()
                self.draw()
            elif self.scene == 1:
                self.update()
                self.draw()
            elif self.scene == 2:
                self.update()
                self.draw()
            elif self.scene == 3:
                self.update()
                self.draw()
            elif self.scene == 4:
                self.update()
                self.draw()
            if self.player.hp <= 0:
                self.game_end(0)
            
                '''print("Game Over!")
                subprocess.Popen(['python', 'GameOverScreen.py'])
                pg.quit()
                sys.exit()'''

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
        self.check_clear()
        self.Animate.update()
      
    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(background,(0,0))
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)
        bullets.draw(self.screen)  # <- Draw bullets
        self.UI()
        pg.display.flip()
    
    def UI(self):
        pg.draw.rect(self.screen,(WHITE),pg.Rect(22,10,200,40))
        pg.draw.rect(self.screen,(GREEN),pg.Rect(22,10,self.player.hp *2,40))
        self.screen.blit(health_frame_img,(0,0))
        

    def check_clear(self):
        if len(self.enemies) ==0 and self.scene ==0 :
            if len(self.door) == 0:
                a =BaseSprite(door_grid[0][0]*TILE_SIZE,door_grid[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE,color=BLACK)
                self.all_sprites.add(a)
                self.door.add(a)
     
        elif self.scene == 1 and len(self.enemies) ==0 :
            if len(self.door) == 0:
                a =BaseSprite(door_grid[0][0]*TILE_SIZE,door_grid[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE,color=BLACK)
                self.all_sprites.add(a)
                self.door.add(a)
        
        elif self.scene == 2 and len(self.enemies) ==0 :
            if len(self.door) == 0:
                a =BaseSprite(door_grid[0][0]*TILE_SIZE,door_grid[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE,color=BLACK)
                self.all_sprites.add(a)
                self.door.add(a)

        elif self.scene == 3  and len(self.enemies) ==0:
            if len(self.door) == 0:
                print('aaaaaaaa')
                a =BaseSprite(SCREEN_WIDTH/2-TILE_SIZE/2,SCREEN_HEIGHT/2-TILE_SIZE/2,TILE_SIZE,TILE_SIZE,color=BLACK)
                self.all_sprites.add(a)
                self.door.add(a)

        elif self.scene == 4  and len(self.enemies) ==0:
            if len(self.door) == 0:
                print('aaaaaaaa')
                a =BaseSprite(SCREEN_WIDTH/2-TILE_SIZE/2,SCREEN_HEIGHT/2-TILE_SIZE/2,TILE_SIZE,TILE_SIZE,color=BLACK)
                self.all_sprites.add(a)
                self.door.add(a)

        elif self.scene==5:
            #self.screen.blit(game_clear_img,(0,0))
            #pg.display.flip()
            #pg.time.wait(1500)
            back_to_menu()
      
 

# To Non-san, pls make a button for this function
def back_to_menu():
    subprocess.Popen(['python', 'game_opening.py'])
    pg.quit()
    sys.exit()



# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()




#thing todo 1) add attack pattern for boss    2) texture    3)boss hp bar
            
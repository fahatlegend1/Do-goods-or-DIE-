import random,pygame
from Load_texture import background,Barrel_img,bedrock_img,stonebrick_img
from room_1 import room_1

WIDTH, HEIGHT = 1200, 720
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
ROOM_MAX_SIZE, ROOM_MIN_SIZE = 8, 6
NUM_ROOMS = 8
NUM_OBSTACLES = 25
NUM_WALLS = 10
NUM_ENTITY = 8
NUM_DOOR = 1


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
DARK_GRAY = (50, 50, 50)
floor_texture = background
floor_texture = pygame.transform.scale(floor_texture, (TILE_SIZE, TILE_SIZE))
Barrel_texture = pygame.transform.scale(Barrel_img, (TILE_SIZE, TILE_SIZE))
bedrock_texture = pygame.transform.scale(bedrock_img, (TILE_SIZE, TILE_SIZE))
stonebrick_texture = pygame.transform.scale(stonebrick_img, (TILE_SIZE, TILE_SIZE))

grid = [[1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
rooms = []
obstacles = []
walls = []
entity_grid = []
door_grid = []

def room_1l():
    global grid,obstacles,door_grid,entity_grid
    entity_grid = [(4,4)]
    obstacles = []
    door_grid = [((WIDTH/2)/GRID_WIDTH,(HEIGHT/6)/GRID_WIDTH)]
    grid = room_1

def generate1():
    global grid 
    global rooms 
    global obstacles 
    global walls 
    global entity_grid 
    global door_grid 
    grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    rooms = []
    obstacles = []
    walls = []
    entity_grid = [(10,10),(int(GRID_WIDTH/2),int((GRID_HEIGHT)/2))]
    door_grid = [(WIDTH/GRID_WIDTH,HEIGHT/GRID_HEIGHT)]
    print(entity_grid)

    for _ in range(NUM_OBSTACLES):
        x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
        if grid[x][y] == 0:  # Place obstacles only in open spaces
            obstacles.append((x, y))

    for x in range(GRID_WIDTH):
        grid[x][0] = 2  # Top border
        grid[x][GRID_HEIGHT - 1] = 2  # Bottom border
    for y in range(GRID_HEIGHT):
        grid[0][y] = 2  # Left border
        grid[GRID_WIDTH - 1][y] = 2  # Right border  

   
def generate2():
    global grid 
    global rooms 
    global obstacles 
    global walls 
    global entity_grid 
    global door_grid 
    grid = [[0 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    rooms = []
    obstacles = []
    walls = []
    entity_grid = [(10,10),(int(GRID_WIDTH/2),int((GRID_HEIGHT)/2))]
    door_grid = [(WIDTH/GRID_WIDTH,HEIGHT/GRID_HEIGHT)]
    print(entity_grid)

    for _ in range(NUM_OBSTACLES):
        x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
        if grid[x][y] == 0:  # Place obstacles only in open spaces
            obstacles.append((x, y))

    for x in range(GRID_WIDTH):
        grid[x][0] = 2  # Top border
        grid[x][GRID_HEIGHT - 1] = 2  # Bottom border
    for y in range(GRID_HEIGHT):
        grid[0][y] = 2  # Left border
        grid[GRID_WIDTH - 1][y] = 2  # Right border  
 




def generate():
    global grid 
    global rooms 
    global obstacles 
    global walls 
    global entity_grid 
    global door_grid 
    grid = [[1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    rooms = []
    obstacles = []
    walls = []
    entity_grid = []
    door_grid = []
    
    # Create map boundaries
    for x in range(GRID_WIDTH):
        grid[x][0] = 2  # Top border
        grid[x][GRID_HEIGHT - 1] = 2  # Bottom border
    for y in range(GRID_HEIGHT):
        grid[0][y] = 2  # Left border
        grid[GRID_WIDTH - 1][y] = 2  # Right border

    # Generate rooms
    class Room:
        def __init__(self, x, y, w, h):
            self.x, self.y = x, y
            self.w, self.h = w, h
            self.center = (x + w // 2, y + h // 2)
        
        def carve(self):
            for i in range(self.x, self.x + self.w):
                for j in range(self.y, self.y + self.h):
                    grid[i][j] = 0

    def create_hallway(x1, y1, x2, y2):
        if random.random() < 0.5:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[x][y1] = 0
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[x2][y] = 0
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[x1][y] = 0
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[x][y2] = 0

    for _ in range(NUM_ROOMS):
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, GRID_WIDTH - w - 2)
        y = random.randint(1, GRID_HEIGHT - h - 2)
        new_room = Room(x, y, w, h)
        rooms.append(new_room)
        new_room.carve()
        if len(rooms) > 1:
            create_hallway(rooms[-2].center[0], rooms[-2].center[1], new_room.center[0], new_room.center[1])
            
    for _ in range(NUM_OBSTACLES):
        x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
        if grid[x][y] == 0:  # Place obstacles only in open spaces
            obstacles.append((x, y))

    # Generate walls
    for _ in range(NUM_WALLS):
        x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
        if grid[x][y] == 0:  # Place walls in open spaces
            walls.append((x, y))
            grid[x][y] = 2  # Mark as wall

    for _ in range(NUM_ENTITY):
        while True:
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
            if grid[x][y] == 0:  # Place walls in open spaces
                entity_grid.append((x, y))
                break

    for _ in range(NUM_DOOR):
        while True:
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
            if grid[x][y] == 0:  # Place walls in open spaces
                door_grid.append((x, y))
                break

generate()
        

def get():
    return entity_grid,door_grid
    


map_grid = grid

def draw_grid(screen,Obstacle,ob_group,BaseSprite,base_group):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 0:
                c = BaseSprite(x* TILE_SIZE,y* TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE,color = (255,0,0),image = floor_texture)
                base_group.add(c)
            elif grid[x][y] == 2:
                a = Obstacle(x* TILE_SIZE,y* TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE,indestructible = True,image = bedrock_texture)
                ob_group.add(a)
            else:
                a = Obstacle(x* TILE_SIZE,y* TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE,image = stonebrick_texture,indestructible = True)
                ob_group.add(a)
    for (x, y) in obstacles:
        a = Obstacle(x* TILE_SIZE,y* TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE,image =Barrel_img)
        ob_group.add(a)
    for (x, y) in walls:
            a = Obstacle(x* TILE_SIZE,y* TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE,indestructible = True,image = bedrock_texture)
            ob_group.add(a)  # Dark gray for walls


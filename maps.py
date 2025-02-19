import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
ROOM_MAX_SIZE, ROOM_MIN_SIZE = 8, 6
NUM_ROOMS = 8
NUM_OBSTACLES = 20
NUM_WALLS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
DARK_GRAY = (50, 50, 50)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SoulKnight-Style Map Generator with Obstacles")

# Load floor texture
floor_texture = pygame.image.load(r"Assets\Texture\background1.jpg")
floor_texture = pygame.transform.scale(floor_texture, (TILE_SIZE, TILE_SIZE))

# Grid
grid = [[1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
rooms = []
obstacles = []
walls = []

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

# Generate obstacles
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

# Draw map
def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 0:
                screen.blit(floor_texture, (x * TILE_SIZE, y * TILE_SIZE))
            elif grid[x][y] == 2:
                pygame.draw.rect(screen, DARK_GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for (x, y) in obstacles:
        pygame.draw.rect(screen, BROWN, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Brown for crates/rocks
        pygame.draw.circle(screen, GREEN, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)  # Green for bushes
    for (x, y) in walls:
        pygame.draw.rect(screen, DARK_GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Dark gray for walls

def main():
    running = True
    while running:
        screen.fill(BLACK)
        draw_grid()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import sys, subprocess
import random, math



# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Game Over Screen")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up fonts
font = pygame.font.SysFont("Arial", 64)
button_font = pygame.font.SysFont("Arial", 32)

# Load sound effect
game_over_sound = pygame.mixer.Sound(r"Assets\Audio\game_over_sound.wav")

# Particle class for confetti effect
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 10)
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-2, 2)
        self.lifetime = random.randint(30, 60)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# Function to create a dynamic background effect (gradient with moving color)
def draw_background(offset):
    for i in range(0, screen_width, 20):
        r = int((math.sin(i / 100.0 + offset) * 127) + 128)
        g = int((math.cos(i / 100.0 + offset) * 127) + 128)
        b = int((math.sin(i / 50.0 + offset) * 127) + 128)
        pygame.draw.line(screen, (r, g, b), (i, 0), (i, screen_height), 1)

# Function to create bouncing text animation
def draw_text(text, font, color, x, y, offset, scale_factor=1.0):
    text_surface = font.render(text, True, color)
    width, height = text_surface.get_size()
    scaled_surface = pygame.transform.scale(text_surface, (int(width * scale_factor), int(height * scale_factor)))
    screen.blit(scaled_surface, (x - scaled_surface.get_width() // 2, y - scaled_surface.get_height() // 2))
    return scaled_surface

def game_over_screen(score, offset):
    # Background animation (moving gradient)
    draw_background(offset)

    # Bouncing text
    scale_factor = 1 + math.sin(offset * 0.1) * 0.1  # Scale text up and down
    game_over_text = draw_text("Game Over", font, WHITE, screen_width // 2, screen_height // 4, offset, scale_factor)
    
    # Score Text
    score_text = button_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))

    # Instructions
    quit_text = button_font.render("Press Q to Quit", True, WHITE)
    screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 1.5))

    restart_text = button_font.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 1.7))

def main():
    running = True
    score = 0  # Random score for demonstration
    game_over_sound.play()  # Play the game over sound

    # Create a list to store particles for the confetti effect
    particles = []

    offset = 0  # Used to animate the background and text

    while running:
        screen.fill(BLACK)

        # Create particles for confetti effect
        if random.random() < 0.1:  # Add new particles randomly
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            particles.append(Particle(random.randint(0, screen_width), random.randint(0, screen_height), color))

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        # Show the enhanced game-over screen
        game_over_screen(score, offset)

        # Handle events (quit, restart)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Press Q to quit
                    running = False
                elif event.key == pygame.K_r:  # Press R to restart
                    score = 0  # Reset score or handle restart logic
                    print("Game restarted!")  # Placeholder
                    subprocess.Popen(["python", "Main.py"]) # Run the main game script
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        offset += 0.05  # Increment to animate the background and text

        pygame.time.delay(10)

    pygame.quit()
    sys.exit()

# Start the game
main()

import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Do Good or DIE!")

# Load sounds
pygame.mixer.music.load("menu_music.mp3")  # Background music
pygame.mixer.music.set_volume(0.5)  # Default music volume
pygame.mixer.music.play(-1)  # Loop music indefinitely

click_sound = pygame.mixer.Sound("click.wav")  # Button click sound
click_sound.set_volume(0.7)  # Default click sound volume

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (200, 50, 50)
DARK_RED = (150, 0, 0)

# Font
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 40)

# Game states
MENU = "menu"
EDITOR_SCREEN = "editor"
SETTINGS_SCREEN = "settings"
current_screen = MENU  # Start on the main menu

# Volume settings
master_volume = 1.0  # Overall volume
music_volume = 0.5   # Background music volume

# Background gradient function
def draw_gradient():
    for i in range(HEIGHT):
        color = (max(0, 30 - i // 10), max(0, 30 - i // 10), max(0, 30 - i // 20))  # Darkening effect
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = self.rect.inflate(10, 10) if self.rect.collidepoint(mouse_pos) else self.rect
        pygame.draw.rect(screen, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, button_rect, border_radius=10)

        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            click_sound.play()
            self.action()

# Slider class
class Slider:
    def __init__(self, x, y, width, value, min_value, max_value, action):
        self.x = x
        self.y = y
        self.width = width
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.action = action
        self.dragging = False

    def draw(self, screen):
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 5)
        handle_x = self.x + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
        pygame.draw.circle(screen, RED if self.dragging else WHITE, (handle_x, self.y), 10)

    def check_event(self, event):
        global master_volume, music_volume
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_x = self.x + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.width)
            if abs(event.pos[0] - handle_x) < 10 and abs(event.pos[1] - self.y) < 10:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_value = (event.pos[0] - self.x) / self.width * (self.max_value - self.min_value) + self.min_value
            self.value = max(self.min_value, min(self.max_value, new_value))
            self.action(self.value)

# Volume control functions
def set_master_volume(value):
    global master_volume
    master_volume = value
    click_sound.set_volume(master_volume * 0.7)  # Adjust click sound volume

def set_music_volume(value):
    global music_volume
    music_volume = value
    pygame.mixer.music.set_volume(music_volume)  # Adjust background music volume

# Button actions
def start_game():
    print("Game Started!")  # Replace with actual game logic

def quit_game():
    pygame.quit()
    sys.exit()

def go_to_editor():
    global current_screen
    current_screen = EDITOR_SCREEN

def go_to_settings():
    global current_screen
    current_screen = SETTINGS_SCREEN

def go_to_menu():
    global current_screen
    current_screen = MENU

# Create buttons
start_button = Button("Start", 300, 280, 200, 60, RED, DARK_RED, start_game)
quit_button = Button("Quit", 300, 380, 200, 60, RED, DARK_RED, quit_game)
question_button = Button("?", 20, HEIGHT - 60, 50, 50, GRAY, WHITE, go_to_editor)
settings_button = Button("⚙", WIDTH - 70, HEIGHT - 60, 50, 50, GRAY, WHITE, go_to_settings)
back_button = Button("Back", 300, 500, 200, 60, RED, DARK_RED, go_to_menu)

# Create sliders
master_volume_slider = Slider(300, 250, 200, master_volume, 0.0, 1.0, set_master_volume)
music_volume_slider = Slider(300, 350, 200, music_volume, 0.0, 1.0, set_music_volume)

# Title animation variables
title_y = 120
title_direction = 1

# Game loop
running = True
while running:
    screen.fill(BLACK)
    draw_gradient()

    if current_screen == MENU:
        # Animate title (bouncing effect)
        title_surf = title_font.render("Do Good or DIE!", True, RED)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, title_y))
        screen.blit(title_surf, title_rect)

        title_y += title_direction
        if title_y >= 130 or title_y <= 110:
            title_direction *= -1

        # Draw main menu buttons
        start_button.draw(screen)
        quit_button.draw(screen)
        question_button.draw(screen)
        settings_button.draw(screen)

    elif current_screen == EDITOR_SCREEN:
        # Show editor info
        editor_text = small_font.render("Game Editor: Kaan,Non,Tonnam,Fahad,Neo,Japan ", True, WHITE)
        text_rect = editor_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(editor_text, text_rect)

        # Draw back button
        back_button.draw(screen)

    elif current_screen == SETTINGS_SCREEN:
        # Show settings title
        settings_text = small_font.render("Settings", True, WHITE)
        screen.blit(settings_text, (350, 150))

        # Draw sliders
        master_volume_slider.draw(screen)
        music_volume_slider.draw(screen)

        # Draw back button
        back_button.draw(screen)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_screen == MENU:
            start_button.check_click(event)
            quit_button.check_click(event)
            question_button.check_click(event)
            settings_button.check_click(event)
        elif current_screen == EDITOR_SCREEN or current_screen == SETTINGS_SCREEN:
            back_button.check_click(event)
            if current_screen == SETTINGS_SCREEN:
                master_volume_slider.check_event(event)
                music_volume_slider.check_event(event)

    pygame.display.flip()

pygame.quit()

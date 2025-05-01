# ui.py

import sys
import pygame

# Initialize Pygame UI context
pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption("Game UI")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Reusable Button class
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.color = GRAY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2)
        txt = font.render(self.text, True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.color = BLUE if self.rect.collidepoint(event.pos) else GRAY
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

# --- Main Menu ---
def main_menu():
    running = True
    start_game = False

    def start_callback():
        nonlocal start_game
        start_game = True

    start_button = Button("Start Game", 200, 160, 200, 60, start_callback)

    while running and not start_game:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.handle_event(event)

        # Draw title and button
        title = font.render("Welcome to My Game", True, BLACK)
        screen.blit(title, (180, 80))
        start_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return start_game

# --- Death Screen ---
def death_screen(cause: str):
    print("death occurred")

    restart = False

    def restart_game():
        nonlocal restart
        restart = True


    restart_button = Button("Restart", 230, 280, 140, 50, restart_game)

    while not restart:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if restart_button.handle_event(event):
                return True

        title = big_font.render("You Died", True, RED)
        cause_text = font.render(f"Cause: {cause}", True, BLACK)

        screen.blit(title, (210, 100))
        screen.blit(cause_text, (200, 160))
        restart_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    return True

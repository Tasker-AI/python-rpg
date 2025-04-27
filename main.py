import pygame
import sys
import os
from datetime import datetime
from src.engine.game_state import GameStateManager
from src.engine.states import MenuState, PlayState

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TICK_RATE = 0.6  # seconds per game tick

# Colors - RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game setup code
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python RPG")

# Create a clock for tracking delta time
clock = pygame.time.Clock()

# Initialize game state manager
state_manager = GameStateManager()

# Create and add game states
menu_state = MenuState()
play_state = PlayState()
state_manager.add_state("menu", menu_state)
state_manager.add_state("play", play_state)

# Start with the menu state
state_manager.change_state("menu")

# Variables for tick-based system
tick_timer = 0
game_ticks = 0

# Main game loop
running = True
while running:
    # Calculate delta time in seconds (time passed since last frame)
    delta_time = clock.tick(FPS) / 1000.0
    
    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    # Pass events to current state
    state_manager.handle_events(events)
    
    # Update game state
    state_manager.update(delta_time)
    
    # Update tick-based system (global game ticks)
    tick_timer += delta_time
    if tick_timer >= TICK_RATE:
        game_ticks += 1
        tick_timer -= TICK_RATE
        # Global tick-based logic can go here
    
    # Draw to the screen
    screen.fill(BLACK)  # Clear the screen
    state_manager.draw(screen)
    
    # Display FPS in the corner (for debugging)
    font = pygame.font.Font(None, 24)
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
    
    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()

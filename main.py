import pygame
import sys
import os
from datetime import datetime
from src.engine.game_state import GameStateManager
from src.engine.states import MenuState, PlayState
from src.engine.logger import game_logger
from src.engine.click_simulator import click_simulator

# Initialize pygame
pygame.init()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)
game_logger.info("Starting game")

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
game_logger.info(f"Screen initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# Create a clock for tracking delta time
clock = pygame.time.Clock()

# Initialize font for FPS display
font = pygame.font.SysFont(None, 24)

# Create state manager
state_manager = GameStateManager()

# Create asset manager
from src.engine.asset_manager import AssetManager
asset_manager = AssetManager()

# Add states
state_manager.add_state("menu", MenuState())
state_manager.add_state("play", PlayState(asset_manager))

# Set initial state
state_manager.change_state("play")

# Start click simulator
click_simulator.start()
game_logger.info("Click simulator ready - use the console to simulate clicks")

# Variables for tick-based system
tick_timer = 0
game_ticks = 0

# Main game loop
running = True
while running:
    # Calculate delta time
    delta_time = clock.tick(FPS) / 1000.0
    
    # Handle events from both pygame and simulator
    events = pygame.event.get()
    simulated_events = click_simulator.get_events()
    if simulated_events:
        game_logger.info(f"Processing {len(simulated_events)} simulated events")
        events.extend(simulated_events)
    
    for event in events:
        if event.type == pygame.QUIT:
            game_logger.info("Game quit requested")
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
game_logger.info("Game shutting down")
click_simulator.stop()
pygame.quit()
sys.exit()

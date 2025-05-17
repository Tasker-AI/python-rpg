import pygame
import sys
import os
from datetime import datetime
from src.game_state.game_state import GameStateManager
from src.game_state.menu_state import MenuState
from src.game_state.play_state import PlayState
from src.game_state.character_select_state import CharacterSelectState
from src.engine.logger import game_logger
from src.engine.save_manager import SaveManager

# Initialize pygame
pygame.init()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)
game_logger.info("Starting game")

# Game constants
SCREEN_WIDTH = 800  # Default width
SCREEN_HEIGHT = 600  # Default height
FPS = 60
TICK_RATE = 0.6  # seconds per game tick
FULLSCREEN = False  # Start in windowed mode by default

# Colors - RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game setup code
# Set resizable flag for the window
flags = pygame.RESIZABLE
if FULLSCREEN:
    flags |= pygame.FULLSCREEN
    # Get the current display info to set fullscreen resolution
    display_info = pygame.display.Info()
    SCREEN_WIDTH = display_info.current_w
    SCREEN_HEIGHT = display_info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
pygame.display.set_caption("Python RPG")
game_logger.info(f"Screen initialized: {SCREEN_WIDTH}x{SCREEN_HEIGHT}, Fullscreen: {FULLSCREEN}")

# Create a clock for tracking delta time
clock = pygame.time.Clock()

# Initialize font for FPS display
font = pygame.font.SysFont(None, 24)

# Create state manager
state_manager = GameStateManager()

# Create asset manager
from src.engine.asset_manager import AssetManager
asset_manager = AssetManager()

# Create save manager without a default character
save_manager = SaveManager(character_name=None)

# Create states
state_manager.add_state("menu", MenuState())
state_manager.add_state("character_select", CharacterSelectState(asset_manager, save_manager))

# Create PlayState with asset and save managers
map_file = 'assets/maps/map.json'
play_state = PlayState(asset_manager, save_manager, map_file=map_file)
state_manager.add_state("play", play_state)

# Set initial state
state_manager.change_state("character_select")


# Variables for tick-based system
tick_timer = 0
game_ticks = 0

# Main game loop
running = True
while running:
    # Calculate delta time
    delta_time = clock.tick(FPS) / 1000.0
    
    # Handle pygame events
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            game_logger.info("Game quit requested")
            # Force a final save before quitting
            if isinstance(state_manager.current_state, PlayState):
                play_state = state_manager.current_state
                if hasattr(play_state, 'save_manager') and play_state.player:
                    game_logger.info("Performing final save before exit")
                    # Collect character and world states separately
                    character_state, world_state = play_state.save_manager.collect_game_states(
                        play_state.player, play_state.tilemap, play_state.game_ticks)
                    # Save both states
                    play_state.save_manager.save_game_state(character_state, world_state, play_state.game_ticks)
                    game_logger.info("Final save complete")
            running = False
        
        # Handle window resize events
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            game_logger.info(f"Window resized to {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            # Notify the current state about the resize
            state_manager.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Toggle fullscreen with F11 key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    # Save window size before going fullscreen
                    window_size = screen.get_size()
                    # Switch to fullscreen
                    display_info = pygame.display.Info()
                    SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    game_logger.info(f"Switched to fullscreen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                    # Notify the current state about the resize
                    state_manager.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
                else:
                    # Return to windowed mode with previous size
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    game_logger.info(f"Switched to windowed mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                    # Notify the current state about the resize
                    state_manager.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
            # Allow escape key to exit fullscreen
            elif event.key == pygame.K_ESCAPE and FULLSCREEN:
                FULLSCREEN = False
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                game_logger.info(f"Exited fullscreen with Escape key: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
                # Notify the current state about the resize
                state_manager.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
    
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
pygame.quit()
sys.exit()

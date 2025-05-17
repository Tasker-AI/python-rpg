"""
Character selection state for the game.
"""
import pygame
import os
from .game_state import GameState
from src.main_menu.character_select import CharacterSelect as CharacterSelectMenu
from src.main_menu.new_character import NewCharacter as NewCharacterMenu
from src.engine.logger import game_logger

class CharacterSelectState(GameState):
    """State for character selection screen"""
    
    def __init__(self, asset_manager, save_manager):
        super().__init__()
        self.asset_manager = asset_manager
        self.save_manager = save_manager
        self.current_menu = None
        self.screen = pygame.display.get_surface()
        self.setup_ui()
    
    def enter_state(self):
        """Called when the state is entered"""
        self.done = False
        self.next_state = "character_select"
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the character selection UI"""
        self.character_select = CharacterSelectMenu(self.save_manager)
        self.new_character = NewCharacterMenu(self.save_manager)
        self.current_menu = self.character_select
    
    def handle_events(self, events):
        """Handle pygame events."""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            
            # Handle menu-specific events
            result = self.current_menu.handle_event(event)
            if result:
                if result == "new_character":
                    self.current_menu = self.new_character
                elif result == "character_select":
                    self.current_menu = self.character_select
                elif result == "play":
                    # Set the next state and mark as done to trigger the transition
                    self.next_state = ("play", {"character_name": self.save_manager.character_name})
                    self.done = True
                    game_logger.info(f"Selected character: {self.save_manager.character_name}")
                    return self.next_state
        return None
    
    def update(self, delta_time):
        """Update the state."""
        # No continuous updates needed for menu
        pass
    
    def draw(self, screen):
        """Draw the current menu."""
        # Clear screen with a dark background
        screen.fill((30, 30, 40))
        
        if self.current_menu:
            self.current_menu.draw(screen)
    
    def resize(self, width, height):
        """Handle window resize."""
        # Re-initialize UI elements when window is resized
        self.setup_ui()
        self.setup_ui()

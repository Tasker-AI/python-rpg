import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
from src.engine.game_state import GameState, GameStateManager

class TestMenuState(GameState):
    def __init__(self):
        super().__init__()
        self.next_state = "play"
    
    def update(self, delta_time):
        # Just for testing: automatically transition after update
        self.done = True

class TestPlayState(GameState):
    def __init__(self):
        super().__init__()
        self.next_state = "menu"

def test_game_state_manager():
    # Create a game state manager
    manager = GameStateManager()
    
    # Create test states
    menu_state = TestMenuState()
    play_state = TestPlayState()
    
    # Add states to manager
    # TODO: Add states after implementing add_state method
    
    # Test changing states
    # TODO: Test state changes after implementing change_state method
    
    # Basic assertion - we have a manager object
    assert isinstance(manager, GameStateManager)
    print("Game state manager created successfully")
    return True

if __name__ == "__main__":
    pygame.init()
    result = test_game_state_manager()
    pygame.quit()
    print(f"Test passed: {result}")

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
    manager.add_state("menu", menu_state)
    manager.add_state("play", play_state)
    
    # Test changing states
    manager.change_state("menu")
    assert manager.current_state == "menu"
    
    # Test state update and transition
    manager.update(0.1)  # This should trigger the transition in TestMenuState
    assert menu_state.done == True
    assert manager.current_state == "play"
    
    # Basic assertion - we have a manager object
    assert isinstance(manager, GameStateManager)
    print("Game state manager created successfully")
    return True

if __name__ == "__main__":
    pygame.init()
    result = test_game_state_manager()
    pygame.quit()
    print(f"Test passed: {result}")

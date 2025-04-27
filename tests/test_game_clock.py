import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame

def test_game_clock():
    # Test that we can create a clock and get delta time
    clock = pygame.time.Clock()
    
    # First tick just initializes the clock
    clock.tick(60)
    
    # Second tick should return milliseconds passed
    delta_time = clock.tick(60)
    
    # Delta time should be a number (usually small if called quickly)
    assert isinstance(delta_time, int)
    print(f"Delta time: {delta_time}ms")
    return True

if __name__ == "__main__":
    pygame.init()
    result = test_game_clock()
    pygame.quit()
    print(f"Test passed: {result}")

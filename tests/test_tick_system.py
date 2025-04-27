import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
import unittest
from unittest.mock import Mock, patch

class TestTickSystem(unittest.TestCase):
    """Test the tick-based update system"""
    
    def setUp(self):
        pygame.init()
        self.tick_rate = 0.6  # seconds per tick
        self.tick_timer = 0
        self.game_ticks = 0
    
    def tearDown(self):
        pygame.quit()
    
    def test_tick_increment(self):
        """Test that game ticks increment correctly based on elapsed time"""
        # Simulate 3 seconds of game time in 0.1 second increments
        for _ in range(30):
            delta_time = 0.1  # 100ms
            self.tick_timer += delta_time
            if self.tick_timer >= self.tick_rate:
                self.game_ticks += 1
                self.tick_timer -= self.tick_rate
        
        # After 3 seconds with a tick rate of 0.6, we should have 5 ticks
        # (3.0 / 0.6 = 5)
        self.assertEqual(self.game_ticks, 5)
    
    def test_partial_ticks(self):
        """Test that partial ticks accumulate correctly"""
        # Add 0.5 seconds (not enough for a tick)
        self.tick_timer += 0.5
        self.assertEqual(self.game_ticks, 0)
        
        # Add 0.2 more seconds (now we have 0.7 seconds, enough for 1 tick)
        self.tick_timer += 0.2
        if self.tick_timer >= self.tick_rate:
            self.game_ticks += 1
            self.tick_timer -= self.tick_rate
        
        self.assertEqual(self.game_ticks, 1)
        # We should have 0.1 seconds left in the timer
        self.assertAlmostEqual(self.tick_timer, 0.1, delta=0.001)
    
    def test_multiple_ticks_in_one_update(self):
        """Test that multiple ticks can occur in a single update if enough time has passed"""
        # Add 1.5 seconds at once (should be 2 ticks with 0.3 seconds remaining)
        delta_time = 1.5
        self.tick_timer += delta_time
        while self.tick_timer >= self.tick_rate:
            self.game_ticks += 1
            self.tick_timer -= self.tick_rate
        
        self.assertEqual(self.game_ticks, 2)
        self.assertAlmostEqual(self.tick_timer, 0.3, delta=0.001)

if __name__ == "__main__":
    unittest.main()

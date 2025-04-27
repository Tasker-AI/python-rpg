import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
import unittest
from unittest.mock import Mock
from src.game.player import Player
from src.game.tilemap import TileMap, TileType

class TestPlayer(unittest.TestCase):
    """Test the Player class functionality"""
    
    def setUp(self):
        pygame.init()
        # Create a mock asset manager
        self.asset_manager = Mock()
        self.asset_manager.get_image.return_value = None
        
        # Create a mock surface for the player image
        self.mock_surface = pygame.Surface((32, 32))
        self.mock_surface.fill((255, 0, 0))
        self.asset_manager.load_image.return_value = self.mock_surface
        
        # Create a tilemap for testing
        self.tilemap = TileMap(20, 15, 32)
        # Fill with grass (walkable)
        for x in range(self.tilemap.width):
            for y in range(self.tilemap.height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Create player instance at grid position (3, 3)
        self.player = Player(3, 3, self.tilemap, self.asset_manager)
    
    def tearDown(self):
        pygame.quit()
    
    def test_initialization(self):
        """Test that player initializes with correct values"""
        self.assertEqual(self.player.grid_x, 3)
        self.assertEqual(self.player.grid_y, 3)
        # Pixel position should be center of tile
        expected_x, expected_y = self.tilemap.grid_to_pixel(3, 3)
        self.assertEqual(self.player.x, expected_x)
        self.assertEqual(self.player.y, expected_y)
        
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.max_health, 100)
        self.assertEqual(self.player.attack, 10)
        self.assertEqual(self.player.defense, 5)
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.experience, 0)
        
        # Test skills initialization
        self.assertEqual(self.player.get_skill_level("woodcutting"), 1)
        self.assertEqual(self.player.get_skill_level("fishing"), 1)
        
        # Test that asset manager was called
        self.asset_manager.get_image.assert_called_once_with("player")
        self.asset_manager.load_image.assert_called_once_with("player", "player.png")
    
    def test_movement(self):
        """Test player movement functionality"""
        # Mock the pathfinding to return a simple path
        original_find_path = self.tilemap.find_path
        self.tilemap.find_path = Mock(return_value=[(3, 3), (4, 3), (5, 3)])
        
        # Set target position (pixel coordinates of tile 5,3)
        target_x, target_y = self.tilemap.grid_to_pixel(5, 3)
        self.player.move_to(target_x, target_y)
        
        # Check that movement was initialized correctly
        self.assertTrue(self.player.moving)
        self.assertEqual(self.player.next_grid_x, 4)
        self.assertEqual(self.player.next_grid_y, 3)
        
        # Simulate a game tick occurring
        self.player.update(0.6, tick_occurred=True)
        
        # Should have moved to the next tile
        self.assertEqual(self.player.grid_x, 4)
        self.assertEqual(self.player.grid_y, 3)
        
        # Should still be moving to the next tile
        self.assertTrue(self.player.moving)
        self.assertEqual(self.player.next_grid_x, 5)
        self.assertEqual(self.player.next_grid_y, 3)
        
        # Simulate another game tick
        self.player.update(0.6, tick_occurred=True)
        
        # Should have reached the final destination
        self.assertEqual(self.player.grid_x, 5)
        self.assertEqual(self.player.grid_y, 3)
        
        # Should have stopped moving
        self.assertFalse(self.player.moving)
        
        # Restore original pathfinding function
        self.tilemap.find_path = original_find_path
    
    def test_experience_and_leveling(self):
        """Test experience gain and leveling up"""
        initial_level = self.player.level
        initial_max_health = self.player.max_health
        
        # Gain enough experience to level up
        self.player.gain_experience(100)
        
        # Check level up occurred
        self.assertEqual(self.player.level, initial_level + 1)
        self.assertEqual(self.player.max_health, initial_max_health + 10)
        self.assertEqual(self.player.health, self.player.max_health)  # Health should be full after level up
        
        # Experience should be reset
        self.assertTrue(self.player.experience < 100)
    
    def test_smooth_movement(self):
        """Test smooth movement between ticks"""
        # Mock the pathfinding to return a simple path
        original_find_path = self.tilemap.find_path
        self.tilemap.find_path = Mock(return_value=[(3, 3), (4, 3)])
        
        # Set target position
        target_x, target_y = self.tilemap.grid_to_pixel(4, 3)
        self.player.move_to(target_x, target_y)
        
        # Get starting position
        start_x, start_y = self.tilemap.grid_to_pixel(3, 3)
        
        # Update with half the tick time
        self.player.update(0.3, tick_occurred=False)
        
        # Should be halfway between tiles
        expected_x = start_x + (target_x - start_x) * 0.5
        expected_y = start_y + (target_y - start_y) * 0.5
        self.assertAlmostEqual(self.player.x, expected_x, delta=1)
        self.assertAlmostEqual(self.player.y, expected_y, delta=1)
        
        # Should still be at the original grid position
        self.assertEqual(self.player.grid_x, 3)
        self.assertEqual(self.player.grid_y, 3)
        
        # Restore original pathfinding function
        self.tilemap.find_path = original_find_path
        
    def test_damage_and_healing(self):
        """Test taking damage and healing"""
        initial_health = self.player.health
        
        # Take damage
        damage_taken = self.player.take_damage(10)
        self.assertTrue(damage_taken > 0)
        self.assertTrue(self.player.health < initial_health)
        
        # Heal
        self.player.heal(5)
        self.assertEqual(self.player.health, initial_health - damage_taken + 5)
        
        # Heal beyond max health
        self.player.heal(1000)
        self.assertEqual(self.player.health, self.player.max_health)
    
    def test_skill_experience(self):
        """Test skill experience gain"""
        initial_woodcutting = self.player.get_skill_level("woodcutting")
        
        # Not enough experience to level up
        self.player.gain_skill_experience("woodcutting", 10)
        self.assertEqual(self.player.get_skill_level("woodcutting"), initial_woodcutting)
        
        # Enough experience to level up
        self.player.gain_skill_experience("woodcutting", 100)
        self.assertEqual(self.player.get_skill_level("woodcutting"), initial_woodcutting + 1)

if __name__ == "__main__":
    unittest.main()

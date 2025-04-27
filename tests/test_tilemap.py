import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
import unittest
from unittest.mock import Mock
from src.game.tilemap import TileMap, TileType, Tile

class TestTileMap(unittest.TestCase):
    """Test the TileMap class functionality"""
    
    def setUp(self):
        pygame.init()
        self.map_width = 20
        self.map_height = 15
        self.tile_size = 32
        self.tilemap = TileMap(self.map_width, self.map_height, self.tile_size)
        
        # Create a mock asset manager
        self.asset_manager = Mock()
        mock_surface = pygame.Surface((32, 32))
        self.asset_manager.get_image.return_value = mock_surface
        self.tilemap.set_asset_manager(self.asset_manager)
    
    def tearDown(self):
        pygame.quit()
    
    def test_initialization(self):
        """Test that tilemap initializes with correct values"""
        self.assertEqual(self.tilemap.width, self.map_width)
        self.assertEqual(self.tilemap.height, self.map_height)
        self.assertEqual(self.tilemap.tile_size, self.tile_size)
        
        # Check that all tiles are initialized as EMPTY and walkable
        for x in range(self.map_width):
            for y in range(self.map_height):
                tile = self.tilemap.get_tile(x, y)
                self.assertEqual(tile.tile_type, TileType.EMPTY)
                self.assertTrue(tile.walkable)
    
    def test_set_tile(self):
        """Test setting tile types"""
        # Set a grass tile
        self.tilemap.set_tile(5, 5, TileType.GRASS)
        tile = self.tilemap.get_tile(5, 5)
        self.assertEqual(tile.tile_type, TileType.GRASS)
        self.assertTrue(tile.walkable)
        
        # Set a water tile (should be unwalkable)
        self.tilemap.set_tile(6, 6, TileType.WATER)
        tile = self.tilemap.get_tile(6, 6)
        self.assertEqual(tile.tile_type, TileType.WATER)
        self.assertFalse(tile.walkable)
    
    def test_coordinate_conversion(self):
        """Test grid to pixel and pixel to grid conversion"""
        # Test grid to pixel
        pixel_x, pixel_y = self.tilemap.grid_to_pixel(3, 4)
        self.assertEqual(pixel_x, 3 * self.tile_size + self.tile_size // 2)
        self.assertEqual(pixel_y, 4 * self.tile_size + self.tile_size // 2)
        
        # Test pixel to grid
        grid_x, grid_y = self.tilemap.pixel_to_grid(100, 150)
        self.assertEqual(grid_x, 100 // self.tile_size)
        self.assertEqual(grid_y, 150 // self.tile_size)
    
    def test_pathfinding_straight(self):
        """Test A* pathfinding with a straight path"""
        # Create a simple map with all grass (walkable)
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Find path from (1,1) to (5,1) - should be a straight line
        path = self.tilemap.find_path(1, 1, 5, 1)
        expected_path = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]
        self.assertEqual(path, expected_path)
    
    def test_pathfinding_around_obstacle(self):
        """Test A* pathfinding with obstacles"""
        # Create a simple map with all grass (walkable)
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Add a water obstacle in the middle
        self.tilemap.set_tile(2, 1, TileType.WATER)
        self.tilemap.set_tile(2, 2, TileType.WATER)
        self.tilemap.set_tile(2, 3, TileType.WATER)
        
        # Find path from (1,2) to (3,2) - should go around the water
        path = self.tilemap.find_path(1, 2, 3, 2)
        
        # Check that path exists and avoids water
        self.assertTrue(len(path) > 0)
        for x, y in path:
            tile = self.tilemap.get_tile(x, y)
            self.assertTrue(tile.walkable)
    
    def test_pathfinding_diagonal(self):
        """Test diagonal movement in pathfinding"""
        # Create a simple map with all grass (walkable)
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Find path from (1,1) to (5,5) - should include diagonal moves
        path = self.tilemap.find_path(1, 1, 5, 5)
        
        # Check that path exists and is shorter than manhattan distance
        self.assertTrue(len(path) > 0)
        self.assertTrue(len(path) < 9)  # Manhattan distance would be 8 steps
    
    def test_pathfinding_blocked_diagonal(self):
        """Test that diagonal movement is blocked when appropriate"""
        # Create a simple map with all grass (walkable)
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Add obstacles that block diagonal movement
        self.tilemap.set_tile(2, 1, TileType.ROCK)
        self.tilemap.set_tile(1, 2, TileType.ROCK)
        
        # Find path from (1,1) to (2,2) - should not move diagonally
        path = self.tilemap.find_path(1, 1, 2, 2)
        
        # Path should be longer than just diagonal
        self.assertTrue(len(path) > 2)
    
    def test_no_path_found(self):
        """Test when no path can be found"""
        # Create a simple map with all grass (walkable)
        for x in range(self.map_width):
            for y in range(self.map_height):
                self.tilemap.set_tile(x, y, TileType.GRASS)
        
        # Surround a tile with water to make it unreachable
        self.tilemap.set_tile(10, 9, TileType.WATER)
        self.tilemap.set_tile(10, 11, TileType.WATER)
        self.tilemap.set_tile(9, 10, TileType.WATER)
        self.tilemap.set_tile(11, 10, TileType.WATER)
        
        # Try to find path to the isolated tile
        path = self.tilemap.find_path(1, 1, 10, 10)
        
        # Should return empty list
        self.assertEqual(path, [])

if __name__ == "__main__":
    unittest.main()

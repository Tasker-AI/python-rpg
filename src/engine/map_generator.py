import random
from enum import Enum
from typing import List, Tuple, Dict, Optional
from src.maps.tilemap import Tile, TileMap, TileType
from src.entities.resources import Tree, Rock

class MapGenerator:
    """
    Handles generation of game maps with different biomes and features.
    """
    
    def __init__(self, width: int, height: int, tile_size: int = 32):
        """
        Initialize the map generator.
        
        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            tile_size: Size of each tile in pixels
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tile_map = None
        self.resources = {}
    
    def generate_map(self, seed: Optional[int] = None) -> TileMap:
        """
        Generate a new map with the specified dimensions.
        
        Args:
            seed: Optional random seed for reproducible generation
            
        Returns:
            A new TileMap instance with generated terrain
        """
        if seed is not None:
            random.seed(seed)
        
        # Create a new tilemap
        self.tile_map = TileMap(self.width, self.height, self.tile_size)
        self.resources = {}
        
        # Generate terrain
        self._generate_terrain()
        
        # Add resources
        self._add_resources()
        
        return self.tile_map
    
    def _generate_terrain(self):
        """Generate the base terrain for the map."""
        # Simple terrain generation - can be expanded with noise algorithms later
        for y in range(self.height):
            for x in range(self.width):
                # Simple random terrain generation
                rand_val = random.random()
                
                if rand_val < 0.05:  # 5% chance for water
                    self.tile_map.set_tile(x, y, TileType.WATER)
                elif rand_val < 0.1:  # 5% chance for sand (near water)
                    self.tile_map.set_tile(x, y, TileType.SAND)
                else:  # 90% chance for grass (main terrain)
                    self.tile_map.set_tile(x, y, TileType.GRASS)
    
    def _add_resources(self):
        """Add resources like trees and rocks to the map."""
        # Add trees
        num_trees = int(self.width * self.height * 0.03)  # 3% of map is trees
        self._place_resources(num_trees, TileType.TREE, Tree)
        
        # Add rocks
        num_rocks = int(self.width * self.height * 0.02)  # 2% of map is rocks
        self._place_resources(num_rocks, TileType.ROCK, Rock)
    
    def _place_resources(self, count: int, tile_type: TileType, resource_class):
        """
        Place resources of a specific type on the map.
        
        Args:
            count: Number of resources to place
            tile_type: The type of tile to place
            resource_class: The class of resource to create
        """
        placed = 0
        attempts = 0
        max_attempts = count * 2  # Limit placement attempts
        
        while placed < count and attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            # Only place on grass tiles that don't already have a resource
            tile = self.tile_map.get_tile(x, y)
            if tile and tile.tile_type == TileType.GRASS and (x, y) not in self.resources:
                # Create and place the resource
                resource = resource_class(x, y)
                self.resources[(x, y)] = resource
                self.tile_map.set_tile(x, y, tile_type)
                placed += 1
                
            attempts += 1
    
    def get_resources(self) -> dict:
        """
        Get the dictionary of resources on the map.
        
        Returns:
            Dictionary mapping (x, y) coordinates to Resource objects
        """
        return self.resources


def create_map(width: int, height: int, tile_size: int = 32, seed: Optional[int] = None) -> Tuple[TileMap, dict]:
    """
    Convenience function to create a new map with resources.
    
    Args:
        width: Width of the map in tiles
        height: Height of the map in tiles
        tile_size: Size of each tile in pixels
        seed: Optional random seed for reproducible generation
        
    Returns:
        A tuple containing the generated TileMap and a dictionary of resources
    """
    generator = MapGenerator(width, height, tile_size)
    tile_map = generator.generate_map(seed)
    resources = generator.get_resources()
    return tile_map, resources

"""
World state management for the game.
"""
import os
import json
import pygame
import random
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List

from src.entities.resources import Tree, Rock
from src.engine.logger import game_logger

class TileType(Enum):
    """Types of tiles in the game world."""
    GRASS = auto()
    WATER = auto()
    SAND = auto()
    DIRT = auto()
    STONE = auto()

@dataclass
class Tile:
    """Represents a single tile in the game world."""
    tile_type: TileType = TileType.GRASS
    walkable: bool = True
    image: pygame.Surface = None
    rect: pygame.Rect = None
    
    def __post_init__(self):
        """Initialize the tile with default values based on type."""
        self.walkable = self.tile_type not in [TileType.WATER, TileType.STONE]
        
    def draw(self, screen: pygame.Surface, x: int, y: int, tile_size: int) -> None:
        """
        Draw the tile on the screen.
        
        Args:
            screen: The surface to draw on
            x: X position to draw at
            y: Y position to draw at
            tile_size: Size of the tile in pixels
        """
        if self.image:
            screen.blit(self.image, (x, y))
        else:
            # Fallback colored rectangles if no image is available
            colors = {
                TileType.GRASS: (34, 139, 34),  # Forest green
                TileType.WATER: (30, 144, 255),  # Dodger blue
                TileType.SAND: (238, 214, 175),  # Sand
                TileType.DIRT: (139, 69, 19),    # Brown
                TileType.STONE: (169, 169, 169)  # Dark gray
            }
            color = colors.get(self.tile_type, (0, 0, 0))  # Default to black
            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size))

class WorldState:
    """Manages the game world state including tilemap and resources."""
    
    def __init__(self, map_file='assets/maps/generated_map.json'):
        """
        Initialize world state.
        
        Args:
            map_file: Path to the map JSON file to load
        """
        self.map_file = map_file
        self.asset_manager = None  # Initialize asset_manager attribute
        # Initialize tick-based logic
        self.game_ticks = 0
        self.last_tick_time = pygame.time.get_ticks()
        self.tick_interval = 300  # 0.3 seconds per game tick (300ms) for 1 tile per game tick
        self.resources = {}  # (x, y) -> Resource mapping
        game_logger.debug(f"WorldState initialized with tick_interval={self.tick_interval}ms")
        
        # Tile map properties
        self.width = 100  # Default, will be overwritten by _load_map
        self.height = 100  # Default, will be overwritten by _load_map
        self.tile_size = 32  # Default, will be overwritten by _load_map
        self.tiles = []  # 2D list of Tile objects
        
        # Initialize with a default map in case setup_world isn't called
        self._init_tiles(100, 100, 32)
        
        # Set up the world by loading the map
        self.setup_world()
        
    def set_asset_manager(self, asset_manager):
        """Set the asset manager for the world and load tile images."""
        self.asset_manager = asset_manager
        self._load_tile_images()
        
    def setup_world(self):
        """Set up the world by loading it from the map file."""
        # Load the map from file
        self._load_map()
        
        # Load tile images if asset manager is available
        if self.asset_manager:
            self._load_tile_images()
    
    def _init_tiles(self, width: int, height: int, tile_size: int) -> None:
        """
        Initialize the tile grid with default grass tiles.
        
        Args:
            width: Width of the map in tiles
            height: Height of the map in tiles
            tile_size: Size of each tile in pixels
        """
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []
        
        # Create a 2D grid of default grass tiles
        for y in range(height):
            row = []
            for x in range(width):
                tile = Tile(TileType.GRASS)
                tile.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                row.append(tile)
            self.tiles.append(row)
    
    def _load_tile_images(self) -> None:
        """Load images for tiles from the asset manager."""
        if not self.asset_manager:
            return
            
        # Load tile images from the images directory
        self.asset_manager.load_image("grass", "images/grass.png")
        self.asset_manager.load_image("water", "images/water.png")
        # Use placeholder images for missing tiles
        self.asset_manager.load_image("sand", "images/grass.png")  # Using grass as placeholder
        self.asset_manager.load_image("dirt", "images/grass.png")   # Using grass as placeholder
        self.asset_manager.load_image("stone", "images/rock.png")   # Using rock as placeholder
        
        # Assign images to tiles
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile.tile_type == TileType.GRASS:
                    tile.image = self.asset_manager.get_image("grass")
                elif tile.tile_type == TileType.WATER:
                    tile.image = self.asset_manager.get_image("water")
                elif tile.tile_type == TileType.SAND:
                    tile.image = self.asset_manager.get_image("sand")
                elif tile.tile_type == TileType.DIRT:
                    tile.image = self.asset_manager.get_image("dirt")
                elif tile.tile_type == TileType.STONE:
                    tile.image = self.asset_manager.get_image("stone")
    
    def _load_map(self):
        """Load the map from the JSON file."""
        try:
            with open(self.map_file, 'r') as f:
                map_data = json.load(f)
            
            # Initialize tiles with the loaded dimensions
            self._init_tiles(
                width=map_data['width'],
                height=map_data['height'],
                tile_size=map_data['tile_size']
            )
            
            # Load tiles
            tile_type_map = {
                'GRASS': TileType.GRASS,
                'WATER': TileType.WATER,
                'SAND': TileType.SAND,
                'DIRT': TileType.DIRT,
                'STONE': TileType.STONE
            }
            
            for y, row in enumerate(map_data['tiles']):
                for x, tile_type_name in enumerate(row):
                    if tile_type_name in tile_type_map:
                        tile_type = tile_type_map[tile_type_name]
                        self.set_tile(x, y, tile_type)
            
            # Load resources
            self.resources = {}
            for pos_str, resource_data in map_data.get('resources', {}).items():
                x, y = map(int, pos_str.split(','))
                resource_type = resource_data['type']
                
                if resource_type == 'Tree':
                    resource = Tree(x, y)
                elif resource_type == 'Rock':
                    resource = Rock(x, y)
                else:
                    continue
                
                self.resources[(x, y)] = resource
            
            # Load tile images if asset manager is available
            if self.asset_manager:
                self._load_tile_images()
            
            game_logger.info(f"Loaded map from {self.map_file} with {len(self.resources)} resources")
            
        except Exception as e:
            game_logger.error(f"Failed to load map from {self.map_file}: {e}")
            raise
        
    def update(self, current_time):
        """Update world state."""
        # Handle game ticks (every tick_interval milliseconds)
        time_since_last_tick = current_time - self.last_tick_time
        if time_since_last_tick > self.tick_interval:
            # Calculate how many ticks have passed (in case we missed some)
            ticks_passed = time_since_last_tick // self.tick_interval
            self.game_ticks += ticks_passed
            self.last_tick_time = current_time
            
            # Log tick update
            game_logger.debug(f"Tick update: game_ticks={self.game_ticks}, time_since_last_tick={time_since_last_tick}ms")
            
            # Update world state based on game ticks
            self._update_world_state()
    
    def _update_world_state(self):
        """Update world state based on game ticks."""
        # TODO: Implement world state updates based on game ticks
        # This could include resource regeneration, day/night cycle, etc.
        pass
    
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int) -> None:
        """
        Draw the world.
        
        Args:
            screen: The surface to draw on
            camera_x: Camera x offset (will be converted to int)
            camera_y: Camera y offset (will be converted to int)
        """
        try:
            # Ensure camera coordinates are integers
            camera_x = int(camera_x)
            camera_y = int(camera_y)
            
            # Calculate visible tile range with bounds checking
            start_x = max(0, camera_x // self.tile_size)
            start_y = max(0, camera_y // self.tile_size)
            end_x = min(self.width, (camera_x + screen.get_width()) // self.tile_size + 2)  # +2 for edge cases
            end_y = min(self.height, (camera_y + screen.get_height()) // self.tile_size + 2)  # +2 for edge cases
            
            # Ensure we have valid ranges
            if start_x >= end_x or start_y >= end_y:
                return
                
            # Convert to integers for range
            start_x, start_y = int(start_x), int(start_y)
            end_x, end_y = int(end_x), int(end_y)
            
            # Draw visible tiles
            for y in range(start_y, end_y):
                for x in range(start_x, end_x):
                    tile = self.get_tile(x, y)
                    if tile:
                        screen_x = x * self.tile_size - camera_x
                        screen_y = y * self.tile_size - camera_y
                        tile.draw(screen, screen_x, screen_y, self.tile_size)
            
            # Draw resources
            for (res_x, res_y), resource in self.resources.items():
                if (start_x <= res_x < end_x and start_y <= res_y < end_y and 
                    hasattr(resource, 'draw') and callable(resource.draw)):
                    screen_x = res_x * self.tile_size - camera_x
                    screen_y = res_y * self.tile_size - camera_y
                    resource.draw(screen, screen_x, screen_y, self.asset_manager)
                    
        except Exception as e:
            game_logger.error(f"Error in WorldState.draw: {e}")
            # Try to recover by redrawing with safe defaults
            if 'camera_x' not in locals():
                camera_x, camera_y = 0, 0
            screen.fill((0, 0, 0))  # Clear screen to black on error
    
    def is_walkable(self, x: int, y: int) -> bool:
        """
        Check if a tile is walkable.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the tile is walkable, False otherwise
        """
        tile = self.get_tile(x, y)
        if not tile:
            return False
            
        # Check if there's a resource that blocks movement
        resource = self.get_resource_at(x, y)
        if resource and hasattr(resource, 'blocks_movement') and resource.blocks_movement:
            return False
            
        return tile.walkable
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Get the tile at the specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            The Tile object at (x, y) or None if out of bounds
        """
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return self.tiles[y][x]
        
    def set_tile(self, x: int, y: int, tile_type: TileType) -> None:
        """
        Set the type of a tile at the specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            tile_type: Type of tile to set
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x].tile_type = tile_type
            self.tiles[y][x].walkable = tile_type not in [TileType.WATER, TileType.STONE]
            
            # Update tile image if asset manager is available
            if self.asset_manager:
                if tile_type == TileType.GRASS:
                    self.tiles[y][x].image = self.asset_manager.get_image("grass")
                elif tile_type == TileType.WATER:
                    self.tiles[y][x].image = self.asset_manager.get_image("water")
                elif tile_type == TileType.SAND:
                    self.tiles[y][x].image = self.asset_manager.get_image("sand")
                elif tile_type == TileType.DIRT:
                    self.tiles[y][x].image = self.asset_manager.get_image("dirt")
                elif tile_type == TileType.STONE:
                    self.tiles[y][x].image = self.asset_manager.get_image("stone")
        
    def get_resource_at(self, x, y):
        """
        Get the resource at the specified coordinates, if any.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            The Resource object at (x, y) or None if no resource is present
        """
        return self.resources.get((int(x), int(y)))
        
    def remove_resource(self, x, y):
        """
        Remove a resource from the specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            The removed Resource or None if no resource was present
        """
        return self.resources.pop((int(x), int(y)), None)
        
    def get_tile_size(self) -> int:
        """
        Get the size of tiles in the world.
        
        Returns:
            int: The size of each tile in pixels
        """
        return self.tile_size
        
    def world_to_screen(self, grid_x, grid_y):
        """
        Convert grid coordinates to screen coordinates.
        
        Args:
            grid_x: X coordinate in grid space
            grid_y: Y coordinate in grid space
            
        Returns:
            tuple: (screen_x, screen_y) screen coordinates
        """
        screen_x = grid_x * self.tile_size + self.tile_size // 2
        screen_y = grid_y * self.tile_size + self.tile_size // 2
        return screen_x, screen_y
    
    def screen_to_world(self, screen_x, screen_y):
        """
        Convert screen coordinates to grid coordinates.
        
        Args:
            screen_x: X coordinate in screen space
            screen_y: Y coordinate in screen space
            
        Returns:
            tuple: (grid_x, grid_y) grid coordinates
        """
        grid_x = int(screen_x // self.tile_size)
        grid_y = int(screen_y // self.tile_size)
        return grid_x, grid_y
    
    def save_state(self, save_manager=None):
        """
        Save world state back to the map file.
        
        Args:
            save_manager: Kept for compatibility, not used
        """
        try:
            # Create a dictionary to hold the map data
            map_data = {
                'width': self.width,
                'height': self.height,
                'tile_size': self.tile_size,
                'tiles': [],
                'resources': {}
            }
            
            # Save tile data
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    tile = self.get_tile(x, y)
                    row.append(tile.tile_type.name)
                map_data['tiles'].append(row)
            
            # Save resources
            for (x, y), resource in self.resources.items():
                map_data['resources'][f"{x},{y}"] = {
                    'type': resource.__class__.__name__,
                    'position': [x, y]
                }
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.map_file), exist_ok=True)
            
            # Write to file
            with open(self.map_file, 'w') as f:
                json.dump(map_data, f, indent=2)
                
            game_logger.info(f"Saved world state to {self.map_file}")
            
        except Exception as e:
            game_logger.error(f"Failed to save world state: {e}")
            raise
        
    def is_walkable(self, x, y):
        """
        Check if a tile is walkable.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            bool: True if the tile is walkable, False otherwise
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x].walkable
        return False
        
    def find_path(self, start_pos, end_pos):
        """
        Find a path from start_pos to end_pos using A* algorithm.
        
        Args:
            start_pos: Tuple of (x, y) grid coordinates for the start position
            end_pos: Tuple of (x, y) grid coordinates for the target position
            
        Returns:
            List of (x, y) tuples representing the path, or None if no path found
        """
        import heapq
        
        # Convert to integers if needed
        start_x, start_y = int(start_pos[0]), int(start_pos[1])
        end_x, end_y = int(end_pos[0]), int(end_pos[1])
        
        # Check if end position is walkable
        if not self.is_walkable(end_x, end_y):
            game_logger.debug(f"Target position ({end_x}, {end_y}) is not walkable")
            return None
            
        # Diagonal distance heuristic (better for 8-way movement)
        def heuristic(a, b):
            dx = abs(a[0] - b[0])
            dy = abs(a[1] - b[1])
            # D1 = cost of straight movement, D2 = cost of diagonal movement
            D1 = 1
            D2 = 1.4142  # sqrt(2)
            return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)
        
        # Initialize data structures
        open_set = []
        heapq.heappush(open_set, (0, (start_x, start_y)))
        
        came_from = {}
        g_score = {(start_x, start_y): 0}
        f_score = {(start_x, start_y): heuristic((start_x, start_y), (end_x, end_y))}
        
        # Possible movement directions (8-way movement including diagonals)
        directions = [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Cardinal directions
            (1, 1), (1, -1), (-1, 1), (-1, -1)   # Diagonal directions
        ]
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == (end_x, end_y):
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
                
            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check if neighbor is walkable or is the target
                if neighbor != (end_x, end_y) and not self.is_walkable(neighbor[0], neighbor[1]):
                    continue
                    
                # For diagonal movement, check that both adjacent tiles are walkable
                # This prevents cutting through walls diagonally
                if dx != 0 and dy != 0:
                    if not self.is_walkable(current[0] + dx, current[1]) or not self.is_walkable(current[0], current[1] + dy):
                        continue
                    
                # Calculate tentative g score (diagonal movement costs more)
                movement_cost = 1.4142 if (dx != 0 and dy != 0) else 1.0  # sqrt(2) for diagonal, 1 for cardinal
                tentative_g_score = g_score[current] + movement_cost
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, (end_x, end_y))
                    
                    # Add to open set if not already there
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No path found
        game_logger.debug(f"No path found from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        return None
        
    def load_state(self, save_manager):
        """Load world state."""
        if hasattr(save_manager, 'load_world_save'):
            world_save = save_manager.load_world_save()
            if world_save:
                self.game_ticks = world_save.get('game_ticks', 0)
                game_logger.info(f"Loaded world state with game ticks: {self.game_ticks}")

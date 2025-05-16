import pygame
import json
import heapq
import math
from enum import Enum
from src.engine.logger import game_logger

class TileType(Enum):
    """Enum for different tile types"""
    EMPTY = 0
    GRASS = 1
    WATER = 2
    TREE = 3
    ROCK = 4
    SAND = 5

class Tile:
    """Represents a single tile in the game world"""
    def __init__(self, tile_type, walkable=True, x=0, y=0):
        self.tile_type = tile_type
        self.walkable = walkable
        self.x = x  # Grid coordinates
        self.y = y
        self.f_score = 0  # For A* pathfinding
        self.g_score = 0  # For A* pathfinding
        self.parent = None  # For A* pathfinding
        
        # Set walkability based on tile type
        if tile_type in [TileType.WATER, TileType.TREE, TileType.ROCK]:
            self.walkable = False
    
    def __lt__(self, other):
        """For priority queue in A* algorithm"""
        return self.f_score < other.f_score
    
    def __eq__(self, other):
        """For comparing tiles"""
        if not isinstance(other, Tile):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        """For using tiles in sets"""
        return hash((self.x, self.y))

class TileMap:
    """Represents the game world as a grid of tiles"""
    def __init__(self, width, height, tile_size=32):
        self.width = width  # Number of tiles wide
        self.height = height  # Number of tiles high
        self.tile_size = tile_size  # Size of each tile in pixels
        self.tiles = [[Tile(TileType.EMPTY, True, x, y) for y in range(height)] for x in range(width)]
        self.asset_manager = None
    
    def set_asset_manager(self, asset_manager):
        """Set the asset manager for loading tile images"""
        self.asset_manager = asset_manager
    
    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel coordinates (center of tile)"""
        return (grid_x * self.tile_size + self.tile_size // 2, 
                grid_y * self.tile_size + self.tile_size // 2)
    
    def pixel_to_grid(self, pixel_x, pixel_y):
        """Convert pixel coordinates to grid coordinates"""
        # Use integer division to get the correct grid coordinates
        grid_x = int(pixel_x // self.tile_size)
        grid_y = int(pixel_y // self.tile_size)
        game_logger.debug(f"Converting pixel ({pixel_x}, {pixel_y}) to grid ({grid_x}, {grid_y})")
        return (grid_x, grid_y)
    
    def get_tile(self, x, y):
        """Get the tile at the specified grid coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[x][y]
        return None
    
    def set_tile(self, x, y, tile_type):
        """Set the tile at the specified grid coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            walkable = tile_type not in [TileType.WATER, TileType.TREE, TileType.ROCK]
            self.tiles[x][y] = Tile(tile_type, walkable, x, y)
    
    def is_walkable(self, x, y):
        """Check if a tile is walkable"""
        if not self.is_valid_tile(x, y):
            game_logger.debug(f"Tile ({x}, {y}) is outside map bounds")
            return False
        walkable = self.tiles[x][y].walkable
        if not walkable:
            game_logger.debug(f"Tile ({x}, {y}) is not walkable, type: {self.tiles[x][y].tile_type}")
        return walkable
    
    def is_valid_tile(self, x, y):
        """Check if coordinates are within the map"""
        valid = 0 <= x < self.width and 0 <= y < self.height
        if not valid:
            game_logger.debug(f"Tile ({x}, {y}) is outside map bounds ({self.width}x{self.height})")
        return valid
    
    def load_from_file(self, filename):
        """Load the map from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            self.width = data.get('width', self.width)
            self.height = data.get('height', self.height)
            self.tile_size = data.get('tile_size', self.tile_size)
            
            # Initialize tiles array
            self.tiles = [[Tile(TileType.EMPTY, True, x, y) for y in range(self.height)] for x in range(self.width)]
            
            # Load tile data
            tile_data = data.get('tiles', [])
            for tile_info in tile_data:
                x = tile_info.get('x', 0)
                y = tile_info.get('y', 0)
                tile_type = TileType(tile_info.get('type', 0))
                self.set_tile(x, y, tile_type)
                
            return True
        except Exception as e:
            print(f"Error loading map from {filename}: {e}")
            return False
    
    def save_to_file(self, filename):
        """Save the map to a JSON file"""
        try:
            data = {
                'width': self.width,
                'height': self.height,
                'tile_size': self.tile_size,
                'tiles': []
            }
            
            for x in range(self.width):
                for y in range(self.height):
                    tile = self.tiles[x][y]
                    if tile.tile_type != TileType.EMPTY:
                        data['tiles'].append({
                            'x': x,
                            'y': y,
                            'type': tile.tile_type.value
                        })
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error saving map to {filename}: {e}")
            return False
    
    def draw_base_tiles(self, screen, camera_x, camera_y):
        """Draw the base tiles (grass, water, sand) to the screen."""
        if not self.asset_manager:
            game_logger.error("Asset manager not set for tilemap")
            return
            
        # Get screen dimensions
        screen_width, screen_height = screen.get_size()
        
        # Calculate visible tile range (with buffer for smoother scrolling)
        buffer_tiles = 2  # Extra tiles to render beyond screen edges
        start_x = max(0, int(camera_x // self.tile_size) - buffer_tiles)
        start_y = max(0, int(camera_y // self.tile_size) - buffer_tiles)
        end_x = min(self.width, int((camera_x + screen_width) // self.tile_size) + buffer_tiles + 1)
        end_y = min(self.height, int((camera_y + screen_height) // self.tile_size) + buffer_tiles + 1)
        
        game_logger.debug(f"Drawing base tiles from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        
        # Pre-fetch commonly used images
        grass_img = self.asset_manager.get_image("grass")
        water_img = self.asset_manager.get_image("water")
        
        # Draw visible base tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                pixel_x = x * self.tile_size - camera_x
                pixel_y = y * self.tile_size - camera_y
                
                # Skip rendering if completely outside the screen
                if (pixel_x + self.tile_size < 0 or pixel_x > screen_width or
                    pixel_y + self.tile_size < 0 or pixel_y > screen_height):
                    continue
                
                # Draw base tile
                if tile.tile_type == TileType.EMPTY:
                    pygame.draw.rect(screen, (0, 0, 0), (pixel_x, pixel_y, self.tile_size, self.tile_size))
                elif tile.tile_type == TileType.GRASS or tile.tile_type == TileType.TREE or tile.tile_type == TileType.ROCK:
                    # Draw grass for grass tiles and as the base for tree and rock tiles
                    screen.blit(grass_img, (pixel_x, pixel_y))
                elif tile.tile_type == TileType.WATER:
                    screen.blit(water_img, (pixel_x, pixel_y))
                elif tile.tile_type == TileType.SAND:
                    pygame.draw.rect(screen, (240, 230, 140), (pixel_x, pixel_y, self.tile_size, self.tile_size))
    
    def draw_resources(self, screen, camera_x, camera_y):
        """Draw resource objects (trees, rocks) that should appear above the player."""
        if not self.asset_manager:
            game_logger.error("Asset manager not set for tilemap")
            return
            
        # Get screen dimensions
        screen_width, screen_height = screen.get_size()
        
        # Calculate visible tile range (with buffer for smoother scrolling)
        buffer_tiles = 2  # Extra tiles to render beyond screen edges
        start_x = max(0, int(camera_x // self.tile_size) - buffer_tiles)
        start_y = max(0, int(camera_y // self.tile_size) - buffer_tiles)
        end_x = min(self.width, int((camera_x + screen_width) // self.tile_size) + buffer_tiles + 1)
        end_y = min(self.height, int((camera_y + screen_height) // self.tile_size) + buffer_tiles + 1)
        
        game_logger.debug(f"Drawing resources from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        
        # Pre-fetch commonly used images
        tree_img = self.asset_manager.get_image("tree")
        rock_img = self.asset_manager.get_image("rock")
        
        # Draw visible resource objects
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                pixel_x = x * self.tile_size - camera_x
                pixel_y = y * self.tile_size - camera_y
                
                # Skip rendering if completely outside the screen
                if (pixel_x + self.tile_size < 0 or pixel_x > screen_width or
                    pixel_y + self.tile_size < 0 or pixel_y > screen_height):
                    continue
                
                # Draw resource objects
                if tile.tile_type == TileType.TREE:
                    # Draw tree on top of grass
                    screen.blit(tree_img, (pixel_x, pixel_y - self.tile_size))  # Tree is taller
                elif tile.tile_type == TileType.ROCK:
                    # Draw rock on top of grass
                    screen.blit(rock_img, (pixel_x, pixel_y))
    
    def draw(self, screen, camera_x, camera_y):
        """Draw the visible portion of the tilemap to the screen."""
        # This is now a wrapper that calls the base tiles drawing method
        # The resources will be drawn separately after the player
        self.draw_base_tiles(screen, camera_x, camera_y)
    
    def find_path(self, start_x, start_y, end_x, end_y):
        """
        Find a path from start to end using A* pathfinding algorithm.
        """
        game_logger.debug(f"Finding path from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        
        # If start and end are the same, return just the start position
        if (start_x, start_y) == (end_x, end_y):
            game_logger.debug(f"Start and end are the same tile, returning simple path")
            return [(start_x, start_y)]
        
        # Check if start and end are valid tiles
        if not self.is_valid_tile(start_x, start_y):
            game_logger.warning(f"Start tile ({start_x}, {start_y}) is invalid")
            return []
            
        if not self.is_valid_tile(end_x, end_y):
            game_logger.warning(f"End tile ({end_x}, {end_y}) is invalid")
            return []
        
        # Check if end tile is walkable
        if not self.is_walkable(end_x, end_y):
            game_logger.warning(f"End tile ({end_x}, {end_y}) is not walkable")
            return []
        
        # A* algorithm
        open_set = []
        closed_set = set()
        
        # Add start node to open set
        heapq.heappush(open_set, (0, (start_x, start_y)))
        
        # Dictionary to store the cost to reach each node
        g_score = {(start_x, start_y): 0}
        
        # Dictionary to store the parent of each node
        came_from = {}
        
        # Track algorithm stats
        nodes_examined = 0
        
        while open_set:
            # Get the node with the lowest f_score
            current_f, current = heapq.heappop(open_set)
            nodes_examined += 1
            
            # If we've reached the end, reconstruct the path
            if current == (end_x, end_y):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append((start_x, start_y))
                path.reverse()
                
                # Ensure the target tile is the last in the path
                if path[-1] != (end_x, end_y):
                    game_logger.debug(f"Adding target tile ({end_x}, {end_y}) to path")
                    path.append((end_x, end_y))
                
                game_logger.debug(f"Path found with {len(path)} steps, examined {nodes_examined} nodes")
                game_logger.debug(f"Final path: {path}")
                return path
            
            # Add current node to closed set
            closed_set.add(current)
            
            # Check all neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Skip if neighbor is not valid or not walkable
                if not self.is_valid_tile(neighbor[0], neighbor[1]):
                    continue
                    
                if not self.is_walkable(neighbor[0], neighbor[1]):
                    continue
                
                # Skip if neighbor is in closed set
                if neighbor in closed_set:
                    continue
                
                # Check for diagonal movement
                if dx != 0 and dy != 0:
                    # Check if we can move diagonally (both adjacent tiles must be walkable)
                    if not self.is_walkable(current[0] + dx, current[1]) or not self.is_walkable(current[0], current[1] + dy):
                        game_logger.debug(f"Diagonal movement blocked at ({neighbor[0]}, {neighbor[1]})")
                        continue
                
                # Calculate tentative g_score
                # Diagonal movement costs more
                if dx != 0 and dy != 0:
                    tentative_g = g_score[current] + 1.4  # sqrt(2)
                else:
                    tentative_g = g_score[current] + 1
                
                # If neighbor is not in open set or tentative_g is better than previous
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    # Update came_from and g_score
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    
                    # Calculate f_score (g_score + heuristic)
                    f_score = tentative_g + self.heuristic(neighbor, (end_x, end_y))
                    
                    # Add to open set if not already there
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score, neighbor))
        
        # No path found
        game_logger.warning(f"No path found from ({start_x}, {start_y}) to ({end_x}, {end_y}), examined {nodes_examined} nodes")
        return []
    
    def heuristic(self, a, b):
        """Calculate the heuristic (estimated distance) between two tiles"""
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    
    def create_test_map(self):
        """Create a large test map with various terrain types"""
        # Fill with grass
        for x in range(self.width):
            for y in range(self.height):
                self.set_tile(x, y, TileType.GRASS)
        
        # Add lakes (large water areas)
        # Lake 1
        for x in range(20, 40):
            for y in range(30, 50):
                self.set_tile(x, y, TileType.WATER)
        
        # Lake 2
        for x in range(150, 180):
            for y in range(100, 130):
                self.set_tile(x, y, TileType.WATER)
        
        # Add forests (clusters of trees)
        # Forest 1
        for x in range(60, 90):
            for y in range(40, 60):
                if (x + y) % 3 != 0:  # Make it less uniform
                    self.set_tile(x, y, TileType.TREE)
        
        # Forest 2
        for x in range(120, 140):
            for y in range(150, 180):
                if (x * y) % 5 != 0:  # Different pattern
                    self.set_tile(x, y, TileType.TREE)
        
        # Add mountain ranges (rocks)
        # Mountain 1
        for x in range(80, 100):
            for y in range(80, 100):
                if (x + y) % 4 != 0:
                    self.set_tile(x, y, TileType.ROCK)
        
        # Mountain 2
        for x in range(200, 230):
            for y in range(50, 70):
                if (x * y) % 6 != 0:
                    self.set_tile(x, y, TileType.ROCK)
        
        # Add some paths (clear areas in forests)
        for x in range(60, 90):
            self.set_tile(x, 50, TileType.GRASS)
        
        for y in range(40, 60):
            self.set_tile(75, y, TileType.GRASS)
        
        # Add some individual landmarks
        self.set_tile(10, 10, TileType.ROCK)  # Starting area landmark
        self.set_tile(11, 10, TileType.TREE)
        self.set_tile(10, 11, TileType.TREE)
        
        # Add some random elements throughout the map
        import random
        random.seed(42)  # For reproducibility
        
        # Random trees
        for _ in range(500):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.get_tile(x, y).tile_type == TileType.GRASS:
                self.set_tile(x, y, TileType.TREE)
        
        # Random rocks
        for _ in range(300):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.get_tile(x, y).tile_type == TileType.GRASS:
                self.set_tile(x, y, TileType.ROCK)
        
        # Random small ponds
        for _ in range(50):
            center_x = random.randint(10, self.width - 10)
            center_y = random.randint(10, self.height - 10)
            size = random.randint(1, 3)
            for dx in range(-size, size + 1):
                for dy in range(-size, size + 1):
                    if dx*dx + dy*dy <= size*size:  # Circular shape
                        x, y = center_x + dx, center_y + dy
                        if 0 <= x < self.width and 0 <= y < self.height:
                            if self.get_tile(x, y).tile_type == TileType.GRASS:
                                self.set_tile(x, y, TileType.WATER)

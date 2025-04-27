import pygame
import json
import heapq
import math
from enum import Enum

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
        """Check if the tile at the specified grid coordinates is walkable"""
        tile = self.get_tile(x, y)
        return tile is not None and tile.walkable
    
    def grid_to_pixel(self, grid_x, grid_y):
        """Convert grid coordinates to pixel coordinates (center of tile)"""
        return (grid_x * self.tile_size + self.tile_size // 2, 
                grid_y * self.tile_size + self.tile_size // 2)
    
    def pixel_to_grid(self, pixel_x, pixel_y):
        """Convert pixel coordinates to grid coordinates"""
        return (pixel_x // self.tile_size, pixel_y // self.tile_size)
    
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
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw the tilemap to the screen"""
        if not self.asset_manager:
            print("Warning: Asset manager not set for tilemap")
            return
            
        # Calculate visible range of tiles
        screen_width, screen_height = screen.get_size()
        start_x = max(0, camera_x // self.tile_size - 1)
        end_x = min(self.width, (camera_x + screen_width) // self.tile_size + 1)
        start_y = max(0, camera_y // self.tile_size - 1)
        end_y = min(self.height, (camera_y + screen_height) // self.tile_size + 1)
        
        # Draw visible tiles
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tiles[x][y]
                pixel_x = x * self.tile_size - camera_x
                pixel_y = y * self.tile_size - camera_y
                
                # Draw tile based on type
                if tile.tile_type == TileType.EMPTY:
                    pygame.draw.rect(screen, (0, 0, 0), (pixel_x, pixel_y, self.tile_size, self.tile_size))
                elif tile.tile_type == TileType.GRASS:
                    image = self.asset_manager.get_image("grass")
                    screen.blit(image, (pixel_x, pixel_y))
                elif tile.tile_type == TileType.WATER:
                    image = self.asset_manager.get_image("water")
                    screen.blit(image, (pixel_x, pixel_y))
                elif tile.tile_type == TileType.TREE:
                    # Draw grass underneath tree
                    image = self.asset_manager.get_image("grass")
                    screen.blit(image, (pixel_x, pixel_y))
                    # Draw tree on top
                    image = self.asset_manager.get_image("tree")
                    screen.blit(image, (pixel_x, pixel_y - self.tile_size))  # Tree is taller
                elif tile.tile_type == TileType.ROCK:
                    # Draw grass underneath rock
                    image = self.asset_manager.get_image("grass")
                    screen.blit(image, (pixel_x, pixel_y))
                    # Draw rock on top
                    image = self.asset_manager.get_image("rock")
                    screen.blit(image, (pixel_x, pixel_y))
                elif tile.tile_type == TileType.SAND:
                    pygame.draw.rect(screen, (240, 230, 140), (pixel_x, pixel_y, self.tile_size, self.tile_size))
    
    def find_path(self, start_x, start_y, end_x, end_y):
        """
        Find a path from start to end using A* pathfinding algorithm.
        Returns a list of (x, y) tuples representing the path.
        """
        # Check if start and end are valid
        if not self.is_walkable(start_x, start_y) or not self.is_walkable(end_x, end_y):
            return []
        
        # A* algorithm
        start_tile = self.tiles[start_x][start_y]
        end_tile = self.tiles[end_x][end_y]
        
        # Reset pathfinding values
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                tile.f_score = float('inf')
                tile.g_score = float('inf')
                tile.parent = None
        
        # Set start values
        start_tile.g_score = 0
        start_tile.f_score = self.heuristic(start_tile, end_tile)
        
        # Open and closed sets
        open_set = []
        heapq.heappush(open_set, start_tile)
        closed_set = set()
        
        while open_set:
            current = heapq.heappop(open_set)
            
            # Check if we reached the end
            if current == end_tile:
                # Reconstruct path
                path = []
                while current:
                    path.append((current.x, current.y))
                    current = current.parent
                return path[::-1]  # Reverse to get start-to-end
            
            closed_set.add(current)
            
            # Check neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = current.x + dx, current.y + dy
                
                # Skip if out of bounds or not walkable
                if not self.is_walkable(nx, ny):
                    continue
                
                neighbor = self.tiles[nx][ny]
                
                # Skip if already evaluated
                if neighbor in closed_set:
                    continue
                
                # Check if diagonal movement is blocked
                if abs(dx) == 1 and abs(dy) == 1:
                    # Check if diagonal movement is blocked by obstacles
                    if not self.is_walkable(current.x + dx, current.y) or not self.is_walkable(current.x, current.y + dy):
                        continue
                
                # Calculate tentative g score
                # Diagonal movement costs more
                move_cost = 1.4 if abs(dx) + abs(dy) == 2 else 1.0
                tentative_g = current.g_score + move_cost
                
                # Skip if this path is worse
                if tentative_g >= neighbor.g_score:
                    continue
                
                # This is the best path so far
                neighbor.parent = current
                neighbor.g_score = tentative_g
                neighbor.f_score = tentative_g + self.heuristic(neighbor, end_tile)
                
                # Add to open set if not already there
                if neighbor not in [item for item in open_set]:
                    heapq.heappush(open_set, neighbor)
        
        # No path found
        return []
    
    def heuristic(self, a, b):
        """Heuristic function for A* (Euclidean distance)"""
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
    
    def create_test_map(self):
        """Create a simple test map with various terrain types"""
        # Fill with grass
        for x in range(self.width):
            for y in range(self.height):
                self.set_tile(x, y, TileType.GRASS)
        
        # Add some water
        for x in range(5, 8):
            for y in range(3, 10):
                self.set_tile(x, y, TileType.WATER)
        
        # Add some trees
        for x in range(12, 15):
            for y in range(5, 8):
                self.set_tile(x, y, TileType.TREE)
        
        # Add some rocks
        for x in range(18, 20):
            for y in range(12, 14):
                self.set_tile(x, y, TileType.ROCK)
        
        # Add some individual obstacles
        self.set_tile(3, 3, TileType.ROCK)
        self.set_tile(4, 7, TileType.TREE)
        self.set_tile(10, 15, TileType.WATER)
        self.set_tile(15, 10, TileType.TREE)

"""
Player state management for the game.
"""
import pygame
from src.entities.player.player import Player
from src.engine.logger import game_logger

class PlayerState:
    """Manages player state and actions."""
    
    def __init__(self, asset_manager, save_manager, world_state):
        """
        Initialize player state.
        
        Args:
            asset_manager: The asset manager for loading player assets
            save_manager: The save manager for handling game saves
            world_state: Reference to the WorldState for world interaction
        """
        self.player = None
        self.asset_manager = asset_manager
        self.save_manager = save_manager
        self.world_state = world_state
        self.click_indicators = []  # List of (x, y, time_remaining) tuples
        self.current_resource = None  # Currently targeted resource
        self.harvesting = False  # Whether the player is currently harvesting a resource
        
        # Set up player after world is initialized
        if world_state:
            self._setup_player()
    
    def _setup_player(self):
        """Set up the player with the current world state."""
        if not hasattr(self, 'player') or not self.player:
            # Create player at a default position if not already created
            self.create_player(10, 10)
        
    def create_player(self, x=10, y=10):
        """
        Create a new player at the specified position.
        
        Args:
            x: X coordinate in grid space
            y: Y coordinate in grid space
            
        Returns:
            The created Player instance
        """
        if not hasattr(self, 'world_state') or not self.world_state:
            raise ValueError("World state must be set before creating player")
            
        self.player = Player(
            x, y, 
            tilemap=None,  # We'll use world_state for pathfinding
            asset_manager=self.asset_manager,
            world_state=self.world_state
        )
        return self.player
    
    def load_player(self):
        """
        Load player from save file.
        
        Returns:
            bool: True if player was loaded successfully, False otherwise
        """
        if not hasattr(self, 'save_manager') or not self.save_manager:
            game_logger.warning("No save manager available to load player")
            return False
            
        character_save = self.save_manager.load_character_save()
        if character_save:
            grid_position = character_save.get('grid_position', (10, 10))
            grid_x, grid_y = grid_position
            
            if not hasattr(self, 'player') or not self.player:
                self.create_player(grid_x, grid_y)
            else:
                self.player.grid_x = grid_x
                self.player.grid_y = grid_y
                # Update player's position
                self.player.x, self.player.y = self.world_state.world_to_screen(grid_x, grid_y)
                self.player.rect.x = self.player.x - 16  # Adjust for sprite width
                self.player.rect.y = self.player.y - 16   # Adjust for sprite height
            
            game_logger.info(f"Loaded character at position ({grid_x}, {grid_y}) from save file")
            return True
            
        return False
    
    def update(self, current_time):
        """Update player state.
        
        Args:
            current_time: Current game time in seconds
        """
        if not hasattr(self, 'player') or not self.player:
            return
            
        try:
            # Process any pending movements first
            if hasattr(self.player, 'process_movement_queue'):
                self.player.process_movement_queue()
                
            # Update player state with current time for movement interpolation
            if hasattr(self.player, 'update'):
                self.player.update(current_time)
                
        except Exception as e:
            game_logger.error(f"Error updating player: {e}")
            
        # Update click indicators (using fixed time step since we don't have delta_time)
        click_indicator_duration = 0.1  # seconds
        self.click_indicators = [
            (x, y, time_remaining - click_indicator_duration)
            for x, y, time_remaining in self.click_indicators
            if time_remaining - click_indicator_duration > 0
        ]
    
    def draw(self, screen, camera_x, camera_y):
        """Draw player and related UI elements."""
        if self.player:
            self.player.draw(screen, camera_x, camera_y)
        
        # Draw click indicators
        if hasattr(self, 'world_state') and self.world_state:
            tile_size = self.world_state.tile_size
            for x, y, time_remaining in self.click_indicators:
                alpha = int(255 * (time_remaining / 1000))  # Fade out over 1 second
                if alpha > 0:
                    s = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                    pygame.draw.rect(s, (255, 255, 0, alpha), (0, 0, tile_size, tile_size), 2)
                    screen.blit(s, (x * tile_size - camera_x, y * tile_size - camera_y))
    
    def handle_click(self, tile_x, tile_y, button=1):
        """
        Handle click on the game world.
        
        Args:
            tile_x: X coordinate of the clicked tile in grid space
            tile_y: Y coordinate of the clicked tile in grid space
            button: Mouse button that was clicked (1=left, 3=right, etc.)
        """
        # Only process left mouse button clicks
        if button != 1 or not self.player or not self.world_state:
            game_logger.debug(f"CLICK_IGNORED: button={button}, player={self.player is not None}, world_state={self.world_state is not None}")
            return
            
        # Convert to integers if they aren't already
        grid_x = int(round(tile_x))
        grid_y = int(round(tile_y))
        game_logger.info(f"CLICK: Processing click at grid position: ({grid_x}, {grid_y})")
        
        if self.world_state.is_walkable(grid_x, grid_y):
            game_logger.info(f"MOVE_START: Moving to walkable tile: ({grid_x}, {grid_y})")
            success = self.player.move_to_tile(grid_x, grid_y)
            game_logger.info(f"MOVE_INITIATED: {success}")
        else:
            game_logger.warning(f"MOVE_BLOCKED: Tile not walkable: ({grid_x}, {grid_y})")
            
        # Clear any existing click indicators and add new one
        self.click_indicators = [(grid_x, grid_y, 1000)]  # 1000ms = 1 second
        
        # Check if we clicked on a resource
        resource = self.world_state.get_resource_at(grid_x, grid_y)
        
        # If we clicked on a resource, target it
        if resource:
            self.current_resource = resource
            game_logger.info(f"TARGET_RESOURCE: Targeting {type(resource).__name__} at ({grid_x}, {grid_y})")
            
            # Move to the nearest walkable tile next to the resource
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = grid_x + dx, grid_y + dy
                if self.world_state.is_walkable(nx, ny):
                    # Clear any existing movement queue first
                    if hasattr(self.player, 'movement_queue'):
                        self.player.movement_queue.clear()
                    self.player.move_to_tile(nx, ny)
                    game_logger.info(f"MOVE_TO_RESOURCE: Moving to ({nx}, {ny}) to access resource")
                    return
        # Otherwise, just move to the clicked tile if it's walkable
        elif self.world_state.is_walkable(grid_x, grid_y):
            # Clear any existing movement queue first
            if hasattr(self.player, 'movement_queue'):
                self.player.movement_queue.clear()
            self.player.move_to_tile(grid_x, grid_y)
            game_logger.info(f"MOVE_TO_TILE: Moving to ({grid_x}, {grid_y})")
            self.current_resource = None  # Clear any targeted resource
        else:
            game_logger.warning(f"CLICK_UNWALKABLE: Tile at ({grid_x}, {grid_y}) is not walkable")
    
    def save_state(self):
        """Save player state."""
        if self.player and hasattr(self.save_manager, 'save_character'):
            self.save_manager.save_character(self.player)

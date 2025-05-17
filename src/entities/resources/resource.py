import pygame
from enum import Enum
from typing import Tuple, Optional

class ResourceType(Enum):
    """Types of resources in the game."""
    TREE = "tree"
    ROCK = "rock"

class Resource:
    """Base class for all harvestable resources in the game."""
    
    def __init__(self, x: int, y: int, resource_type: ResourceType, harvest_time: int, walkable: bool = False):
        """
        Initialize a resource.
        
        Args:
            x: Grid x-coordinate
            y: Grid y-coordinate
            resource_type: Type of the resource
            harvest_time: Number of ticks required to harvest this resource
            walkable: Whether the resource can be walked through
        """
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.harvest_time = harvest_time
        self.walkable = walkable
        self.current_harvest_time = 0
        self.is_harvesting = False
        self.is_harvested = False
        self.harvester = None  # Reference to the entity harvesting this resource
        
    def start_harvesting(self, harvester) -> bool:
        """
        Start the harvesting process.
        
        Args:
            harvester: Reference to the entity that is harvesting this resource
            
        Returns:
            bool: True if harvesting started successfully, False otherwise
        """
        if self.is_harvested:
            return False
            
        self.is_harvesting = True
        self.harvester = harvester
        self.current_harvest_time = 0
        return True
        
    def update(self) -> bool:
        """
        Update the harvesting progress.
        
        Returns:
            bool: True if the resource has been fully harvested, False otherwise
        """
        if not self.is_harvesting or self.is_harvested:
            return False
            
        self.current_harvest_time += 1
        
        if self.current_harvest_time >= self.harvest_time:
            self.is_harvested = True
            self.is_harvesting = False
            return True
            
        return False
        
    def stop_harvesting(self):
        """Stop the current harvesting process."""
        self.is_harvesting = False
        self.current_harvest_time = 0
        self.harvester = None
        
    def get_rewards(self) -> dict:
        """
        Get the rewards for harvesting this resource.
        
        Returns:
            dict: Dictionary of item types and quantities
        """
        # Base class returns an empty dict, should be overridden by subclasses
        return {}
        
    def draw(self, screen: pygame.Surface, camera_x: int, camera_y: int, asset_manager):
        """
        Draw the resource on the screen.
        
        Args:
            screen: Pygame surface to draw on
            camera_x: Camera x position
            camera_y: Camera y position
            asset_manager: Asset manager to get the resource image
        """
        if self.is_harvested:
            return
            
        # Calculate the pixel position relative to the camera
        pixel_x = self.x * 32 - camera_x  # Assuming 32x32 tiles
        pixel_y = self.y * 32 - camera_y
        
        # Skip drawing if the resource is completely off-screen
        if (pixel_x + 32 < 0 or pixel_x > screen.get_width() or
            pixel_y + 32 < 0 or pixel_y > screen.get_height()):
            return
        
        # Get the appropriate image based on resource type
        image = asset_manager.get_image(self.resource_type.value)
        if image:
            # For trees, adjust the y-position to account for the height of the sprite
            y_offset = -16 if self.resource_type == ResourceType.TREE else 0
            screen.blit(image, (pixel_x, pixel_y + y_offset))
            
            # Draw progress bar if being harvested
            if self.is_harvesting and self.harvest_time > 0:
                progress = self.current_harvest_time / self.harvest_time
                bar_width = 32
                bar_height = 4
                bar_x = pixel_x
                bar_y = pixel_y - 6 + y_offset  # Position above the resource
                
                # Draw background of progress bar
                pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
                # Draw progress
                pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * progress), bar_height))
    
    def get_rect(self) -> pygame.Rect:
        """
        Get the rectangle for collision detection.
        
        Returns:
            pygame.Rect: The rectangle representing this resource
        """
        return pygame.Rect(self.x * 32, self.y * 32, 32, 32)

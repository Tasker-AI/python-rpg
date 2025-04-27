import pygame
import math
from collections import deque
from src.engine.logger import game_logger

class Player:
    """
    Player class that handles player attributes, movement, and rendering.
    """
    def __init__(self, grid_x, grid_y, tilemap, asset_manager):
        # Tile-based position and movement
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.tilemap = tilemap
        
        # Pixel position (center of tile)
        self.x, self.y = tilemap.grid_to_pixel(grid_x, grid_y)
        
        # Movement queue for pathfinding
        self.movement_queue = deque()
        self.moving = False
        self.move_progress = 0.0  # Progress toward next tile (0.0 to 1.0)
        self.next_grid_x = None
        self.next_grid_y = None
        
        # Interpolation variables for smooth movement
        self.start_x = self.x
        self.start_y = self.y
        self.target_x = self.x
        self.target_y = self.y
        self.tick_rate = 0.6  # Same as game tick rate
        
        # Path visualization
        self.current_path = []
        
        # Pending movements to be processed on tick
        self.pending_movements = []
        
        # Track final destination for verification
        self.final_destination = None
        
        # Create player rectangle for collision
        self.rect = pygame.Rect(self.x - 16, self.y - 16, 32, 32)
        
        # Attributes and stats
        self.max_health = 100
        self.health = 100
        self.attack = 10
        self.defense = 5
        
        # Skills
        self.skills = {
            "woodcutting": 1,
            "firemaking": 1,
            "fishing": 1,
            "cooking": 1,
            "mining": 1,
            "smithing": 1,
            "agility": 1
        }
        
        # Experience and level
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100  # Experience needed for next level
        
        # Assets
        self.asset_manager = asset_manager
        self.image = asset_manager.get_image("player")
        if not self.image:  # If image not loaded yet
            self.image = asset_manager.load_image("player", "player.png")
        
        # Collision rectangle
        self.rect = pygame.Rect(self.x - 16, self.y - 16, 32, 32)
    
    def queue_movement(self, grid_x, grid_y):
        """Queue a movement to be processed on the next game tick."""
        game_logger.debug(f"Player.queue_movement: Current tile: ({self.grid_x}, {self.grid_y}), Target tile: ({grid_x}, {grid_y})")
        
        # Check if target is within map bounds
        if not (0 <= grid_x < self.tilemap.width and 0 <= grid_y < self.tilemap.height):
            game_logger.warning(f"Target tile ({grid_x}, {grid_y}) is outside map bounds")
            return
            
        # Check if target is walkable
        if not self.tilemap.is_walkable(grid_x, grid_y):
            game_logger.warning(f"Target tile ({grid_x}, {grid_y}) is not walkable")
            return
        
        # Add to pending movements (will be processed on next tick)
        self.pending_movements.append((grid_x, grid_y))
        game_logger.debug(f"Added movement to ({grid_x}, {grid_y}) to pending queue. Queue size: {len(self.pending_movements)}")
    
    def process_movement_queue(self):
        """Process the pending movement queue on a game tick."""
        if not self.pending_movements:
            return
        
        # Get the most recent click and clear the queue
        grid_x, grid_y = self.pending_movements[-1]
        self.pending_movements.clear()
        game_logger.debug(f"Processing movement to ({grid_x}, {grid_y}) on tick")
        
        # Find path to target
        path = self.tilemap.find_path(self.grid_x, self.grid_y, grid_x, grid_y)
        
        # Log path information
        if path:
            game_logger.debug(f"Path found with {len(path)} steps")
            game_logger.debug(f"Path: {path}")
        else:
            game_logger.warning(f"No path found to ({grid_x}, {grid_y})")
            return
        
        # Clear current movement queue and add new path
        self.movement_queue.clear()
        game_logger.debug(f"Cleared movement queue")
        
        # Store the final destination for verification
        self.final_destination = (grid_x, grid_y)
        
        if path:
            # Make sure the target tile is the last one in the path
            if path[-1] != (grid_x, grid_y):
                game_logger.warning(f"Target tile ({grid_x}, {grid_y}) not in path, forcing it")
                path.append((grid_x, grid_y))
            
            # Skip the first position (current position) if it exists
            start_index = 1 if len(path) > 1 and path[0] == (self.grid_x, self.grid_y) else 0
            
            # Add all path steps to the movement queue
            for x, y in path[start_index:]:
                self.movement_queue.append((x, y))
            
            game_logger.debug(f"Added {len(self.movement_queue)} steps to movement queue: {list(self.movement_queue)}")
            
            # Start moving to the first position in the queue
            self.start_next_move()
    
    def move_to_tile(self, grid_x, grid_y):
        """Set a target position for the player to move towards using pathfinding."""
        game_logger.info(f"MOVE_TO_TILE: Player at ({self.grid_x}, {self.grid_y}) moving to ({grid_x}, {grid_y})")
        
        # Check if target is within map bounds
        if not (0 <= grid_x < self.tilemap.width and 0 <= grid_y < self.tilemap.height):
            game_logger.warning(f"Target tile ({grid_x}, {grid_y}) is outside map bounds")
            return
            
        # Check if target is walkable
        if not self.tilemap.is_walkable(grid_x, grid_y):
            game_logger.warning(f"Target tile ({grid_x}, {grid_y}) is not walkable")
            return
            
        # If we're already at the target tile, no need to move
        if self.grid_x == grid_x and self.grid_y == grid_y:
            game_logger.info(f"Already at target tile ({grid_x}, {grid_y})")
            return
        
        # Find path to target
        path = self.tilemap.find_path(self.grid_x, self.grid_y, grid_x, grid_y)
        
        # Log path information
        if path:
            game_logger.debug(f"Path found with {len(path)} steps")
            game_logger.debug(f"Path: {path}")
        else:
            game_logger.warning(f"No path found to ({grid_x}, {grid_y})")
            return
        
        # Clear current movement queue and add new path
        self.movement_queue.clear()
        game_logger.debug(f"Cleared movement queue")
        
        if path:
            # Make sure the target tile is the last one in the path
            if path[-1] != (grid_x, grid_y):
                game_logger.debug(f"Adding target tile ({grid_x}, {grid_y}) to path")
                path.append((grid_x, grid_y))
            
            # Skip the first position (current position)
            if len(path) > 1:
                for x, y in path[1:]:
                    self.movement_queue.append((x, y))
            
            game_logger.debug(f"Added {len(self.movement_queue)} steps to movement queue")
            
            # Start moving to the first position in the queue
            self.start_next_move()
    
    def move_to(self, pixel_x, pixel_y):
        """Set a target position for the player to move towards using pathfinding."""
        # Convert pixel coordinates to grid coordinates
        target_grid_x, target_grid_y = self.tilemap.pixel_to_grid(pixel_x, pixel_y)
        
        # Use the more reliable tile-based movement method
        self.move_to_tile(target_grid_x, target_grid_y)
    
    def start_next_move(self):
        """Start moving to the next position in the queue."""
        if self.movement_queue:
            self.next_grid_x, self.next_grid_y = self.movement_queue.popleft()
            game_logger.debug(f"Moving to next tile: ({self.next_grid_x}, {self.next_grid_y})")
            
            # Verify the tile is walkable
            if not self.tilemap.is_walkable(self.next_grid_x, self.next_grid_y):
                game_logger.warning(f"Attempted to move to non-walkable tile ({self.next_grid_x}, {self.next_grid_y}), skipping")
                self.start_next_move()  # Try the next tile in the queue
                return
                
            self.moving = True
            self.move_progress = 0.0
        else:
            # No more moves in the queue
            self.moving = False
            self.next_grid_x = None
            self.next_grid_y = None
            
            # Set position to exact center of current tile
            exact_x, exact_y = self.tilemap.grid_to_pixel(self.grid_x, self.grid_y)
            self.x = exact_x
            self.y = exact_y
            
            # Check if we reached our final destination
            if self.final_destination:
                if (self.grid_x, self.grid_y) == self.final_destination:
                    game_logger.info(f"DESTINATION REACHED: Player arrived at final destination {self.final_destination} at exact center ({self.x}, {self.y})")
                else:
                    game_logger.warning(f"DESTINATION MISSED: Player stopped at ({self.grid_x}, {self.grid_y}) but destination was {self.final_destination}")
                self.final_destination = None
            
            self.current_path = []
    
    def update(self, delta_time, tick_occurred=False):
        """Update player position and state."""
        # Handle movement state
        if self.moving:
            if tick_occurred and self.next_grid_x is not None and self.next_grid_y is not None:
                # Log current state before movement
                game_logger.debug(f"Player tick update: Current position: ({self.x}, {self.y}), Tile: ({self.grid_x}, {self.grid_y})")
                
                # Complete the move on a game tick
                self.grid_x = self.next_grid_x
                self.grid_y = self.next_grid_y
                
                # Get the exact center pixel position for the new grid position
                exact_x, exact_y = self.tilemap.grid_to_pixel(self.grid_x, self.grid_y)
                
                # Store start position for interpolation
                self.start_x = self.x
                self.start_y = self.y
                self.target_x = exact_x
                self.target_y = exact_y
                self.move_progress = 0.0
                
                game_logger.info(f"Player moved to tile: ({self.grid_x}, {self.grid_y}), Exact center: ({exact_x}, {exact_y})")
                
                # If this is the final destination, log it
                if self.final_destination and (self.grid_x, self.grid_y) == self.final_destination:
                    game_logger.info(f"DESTINATION REACHED: Player arrived at final destination {self.final_destination}")
                    self.final_destination = None
                
                # Check if there are more moves in the queue
                if len(self.movement_queue) > 0:
                    self.start_next_move()
                else:
                    # If no more moves, continue interpolation but mark as not moving
                    # This allows the interpolation to finish without jerky movement
                    self.next_grid_x = None
                    self.next_grid_y = None
                    # Don't set moving=False yet - we'll do that when interpolation completes
                    game_logger.info(f"Final movement to exact center: ({exact_x}, {exact_y})")
            
            # Always update interpolation when moving, regardless of tick
            # Smooth movement between positions using interpolation
            self.move_progress = min(1.0, self.move_progress + delta_time / self.tick_rate)
            
            # Interpolate position
            self.x = self.start_x + (self.target_x - self.start_x) * self.move_progress
            self.y = self.start_y + (self.target_y - self.start_y) * self.move_progress
            
            # Update collision rectangle
            self.rect.x = self.x - 16
            self.rect.y = self.y - 16
            
            # If interpolation is complete and no more moves, mark as not moving
            if self.move_progress >= 0.99 and len(self.movement_queue) == 0 and self.next_grid_x is None:
                self.moving = False
                # Ensure exact position at end of movement
                self.x = self.target_x
                self.y = self.target_y
                game_logger.debug(f"Movement complete, final position: ({self.x}, {self.y})")
        
        # If we're not moving, ensure we're exactly at the center of our tile
        elif not self.moving:
            exact_x, exact_y = self.tilemap.grid_to_pixel(self.grid_x, self.grid_y)
            if abs(self.x - exact_x) > 0.01 or abs(self.y - exact_y) > 0.01:
                game_logger.info(f"Correcting player position from ({self.x}, {self.y}) to exact center: ({exact_x}, {exact_y})")
                self.x, self.y = exact_x, exact_y
                self.rect.x = self.x - 16
                self.rect.y = self.y - 16
    
    def draw(self, screen, camera_x=0, camera_y=0):
        """Draw the player on the screen."""
        # Draw movement path if there is one
        if self.current_path:
            for i in range(1, len(self.current_path)):
                x1, y1 = self.tilemap.grid_to_pixel(self.current_path[i-1][0], self.current_path[i-1][1])
                x2, y2 = self.tilemap.grid_to_pixel(self.current_path[i][0], self.current_path[i][1])
                pygame.draw.line(screen, (255, 255, 0), 
                               (x1 - camera_x, y1 - camera_y), 
                               (x2 - camera_x, y2 - camera_y), 2)
                
                # Draw dots at each path point
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (x2 - camera_x, y2 - camera_y), 3)
        
        # Draw player sprite
        screen.blit(self.image, (self.x - 16 - camera_x, self.y - 16 - camera_y))
        
        # Draw health bar above player
        health_percent = self.health / self.max_health
        bar_width = 32
        bar_height = 5
        
        # Background (gray)
        pygame.draw.rect(screen, (100, 100, 100), 
                        (self.x - 16 - camera_x, self.y - 25 - camera_y, bar_width, bar_height))
        
        # Health (red)
        pygame.draw.rect(screen, (200, 0, 0), 
                        (self.x - 16 - camera_x, self.y - 25 - camera_y, int(bar_width * health_percent), bar_height))
    
    def gain_experience(self, amount):
        """Add experience and check for level up."""
        self.experience += amount
        
        # Check for level up
        if self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        """Increase player level and stats."""
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)  # Increase exp needed for next level
        
        # Increase stats
        self.max_health += 10
        self.health = self.max_health  # Heal to full on level up
        self.attack += 2
        self.defense += 1
        
        print(f"Level up! Now level {self.level}")
    
    def take_damage(self, amount):
        """Take damage, considering defense."""
        # Apply defense reduction (simple formula)
        actual_damage = max(1, amount - self.defense // 2)
        self.health -= actual_damage
        
        if self.health <= 0:
            self.health = 0
            self.die()
            
        return actual_damage
    
    def heal(self, amount):
        """Heal the player."""
        self.health = min(self.health + amount, self.max_health)
    
    def die(self):
        """Handle player death."""
        print("Player died!")
        # Will implement respawn logic later
    
    def get_skill_level(self, skill):
        """Get the level of a specific skill."""
        # Return the integer part of the skill level
        return int(self.skills.get(skill, 1))
    
    def gain_skill_experience(self, skill, amount):
        """Add experience to a skill and check for level up."""
        if skill not in self.skills:
            return
            
        current_level = int(self.skills[skill])
        # Simple formula: each level requires level*100 experience
        experience_needed = current_level * 100
        
        # Track fractional experience as a separate value
        skill_exp = (self.skills[skill] - current_level) * experience_needed
        skill_exp += amount
        
        # Calculate new level and remaining exp
        level_ups = int(skill_exp / experience_needed)
        remaining_exp = skill_exp % experience_needed
        
        # Update skill level
        new_level = current_level + level_ups
        self.skills[skill] = new_level + (remaining_exp / experience_needed)
        
        # If we've reached a new level
        if new_level > current_level:
            print(f"{skill.capitalize()} level up! Now level {new_level}")
            # Keep the fractional part for progress towards next level

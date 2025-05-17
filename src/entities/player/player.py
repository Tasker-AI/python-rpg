"""
Player class that handles player movement, rendering, and interactions.
"""
import pygame
import math
from collections import deque
from src.engine.logger import game_logger
from src.entities.player.human_sprite import HumanSprite

class Player:
    """
    Player class that handles player attributes, movement, and rendering.
    """
    def __init__(self, grid_x, grid_y, tilemap, asset_manager, world_state=None):
        """
        Initialize the player.
        
        Args:
            grid_x: Initial x-coordinate in grid space
            grid_y: Initial y-coordinate in grid space
            tilemap: For backward compatibility, but should be None
            asset_manager: Asset manager for loading images and resources
            world_state: Reference to the world state for world interaction and pathfinding
        """
        if world_state is None:
            raise ValueError("world_state is required for Player initialization")
            
        # Tile-based position and movement
        self.grid_x = int(grid_x)
        self.grid_y = int(grid_y)
        self.world_state = world_state
        self.on_arrival_callback = None  # Callback for when the player reaches their destination
        
        # Initialize sprite and rect with blue color
        self.sprite = HumanSprite(color=(0, 0, 255))  # Blue clothing
        
        # Force regeneration of sprite cache to ensure different animations for each direction
        self.sprite._generate_cached_sprites()
        
        # Explicitly set the initial direction to down (0)
        self.sprite.direction = 0
        
        self.rect = self.sprite.rect
        
        # Set initial position
        self.x, self.y = self.world_state.world_to_screen(self.grid_x, self.grid_y)
        self.rect.x = self.x - 16  # Center the sprite on the tile
        self.rect.y = self.y - 16   # Position feet at the tile position
        
        # Store tile size for quick access
        self.tile_size = self.world_state.tile_size
        
        # Movement queue for pathfinding
        self.movement_queue = deque()
        self.moving = False
        
        # Store pixel positions for smooth rendering
        self.start_x = float(self.x)
        self.start_y = float(self.y)
        self.target_x = float(self.x)
        self.target_y = float(self.y)
        
        # Movement state
        self.last_move_tick = 0  # Last game tick when the player started moving
        self.move_start_tick = 0  # When the current move started
        self.moving = False  # Whether the player is currently moving
        self.move_duration = 0.2  # Duration of movement animation in seconds
        self.move_progress = 0.0  # Progress through current movement (0.0 to 1.0)
        self.start_x = float(self.x)  # Starting x position for current move
        self.start_y = float(self.y)  # Starting y position for current move
        self.target_x = float(self.x)  # Target x position for current move
        self.target_y = float(self.y)  # Target y position for current move
        self.tiles_per_move = 1  # Number of tiles to move per move
        self.move_direction = (0, 0)  # Current movement direction (dx, dy)
        
        # Direction the player is facing
        self.facing = 'down'  # Default facing direction
        
        # Character rendering offset
        self.character_y_offset = 16  # Offset to move character up by 16 pixels
        
        # Movement flags
        self.final_tile_pending = False  # Flag to handle final tile movement
        self.actually_moving = False     # Flag to track when character is physically moving (not just queued)
        self.path = []  # Path for movement
        
        # Attributes and stats
        self.max_health = 100
        self.health = 100
        self.attack = 10
        self.defense = 5
        
        # Assets
        self.asset_manager = asset_manager

    def move_to_tile(self, tile_x, tile_y, on_arrival=None):
        """Move the player to a specific tile."""
        if not hasattr(self, 'world_state') or not hasattr(self.world_state, 'tile_size'):
            game_logger.warning("Cannot move - world state not properly initialized")
            return False
        
        # Check if the target tile is walkable
        if not self.world_state.is_walkable(tile_x, tile_y):
            game_logger.info(f"MOVE_TO_TILE: Cannot move to non-walkable tile ({tile_x}, {tile_y})")
            return False
        
        game_logger.info(f"MOVE_TO_TILE: Moving to ({tile_x}, {tile_y})")
        
        # Determine the starting position for pathfinding
        # If we're already moving and have a pending tile, use that as the start position
        start_x, start_y = self.grid_x, self.grid_y
        
        # If we're in the middle of a movement and have a next position, use that instead
        if self.moving and hasattr(self, 'next_grid_x') and hasattr(self, 'next_grid_y'):
            start_x, start_y = self.next_grid_x, self.next_grid_y
            game_logger.debug(f"Starting new path from next position: ({start_x}, {start_y})")
        
        # Find path using A* from the appropriate starting position
        path = self.world_state.find_path((start_x, start_y), (tile_x, tile_y))
        
        # If no path found, return False
        if not path:
            game_logger.info(f"MOVE_TO_TILE: No path found to ({tile_x}, {tile_y})")
            return False
        
        # Set the callback to be called when we arrive
        if on_arrival:
            self.on_arrival_callback = on_arrival
        
        # Store the path
        self.path = path
        
        # Queue the movement until the next tick
        # We set moving to True to indicate we have a path to follow
        # but actually_moving stays False until the next game tick
        self.moving = True
        self.actually_moving = False
        self.movement_queued = True
        self.last_move_tick = getattr(self.world_state, 'game_ticks', 0) - 1  # Ensure movement starts on next tick
        
        # Set initial facing direction based on the first step in the path
        if len(path) > 1:
            # Get the first movement step
            first_step = path[1]  # path[0] is current position
            dx = first_step[0] - start_x
            dy = first_step[1] - start_y
            
            # Set facing direction based on the first step
            if abs(dx) > abs(dy):
                self.facing = 'right' if dx > 0 else 'left'
            else:
                self.facing = 'down' if dy > 0 else 'up'
                
            # Update sprite direction immediately, but NEVER start walking animation here
            if hasattr(self, 'sprite') and self.sprite:
                # Just set the direction property directly to avoid any side effects
                if self.facing == 'left':
                    self.sprite.direction = 1  # Left
                elif self.facing == 'right':
                    self.sprite.direction = 3  # Right
                elif self.facing == 'up':
                    self.sprite.direction = 2  # Up
                else:  # down or default
                    self.sprite.direction = 0  # Down
                    
                # CRITICAL: Force walking to False until actual movement starts
                self.sprite.walking = False
                # Reset animation time to ensure we start from a standing pose
                self.sprite.animation_time = 0
        
        # Clear any pending movement flags
        self.final_tile_pending = False
        
        # Initialize movement positions to current position
        current_pos = self.world_state.world_to_screen(self.grid_x, self.grid_y)
        self.movement_start_x = current_pos[0]
        self.movement_start_y = current_pos[1]
        self.x = current_pos[0]
        self.y = current_pos[1]
            
        game_logger.debug(f"Found path with {len(self.path)} tiles to ({tile_x}, {tile_y})")
        
        return True
        
    def _setup_next_movement_segment(self):
        """Set up the next movement segment."""
        if not self.path:
            self.moving = False
            return
            
        # Get the next position from the path
        self.next_grid_x, self.next_grid_y = self.path[0]
        
        # Calculate screen coordinates
        self.start_x, self.start_y = self.world_state.world_to_screen(self.grid_x, self.grid_y)
        self.target_x, self.target_y = self.world_state.world_to_screen(self.next_grid_x, self.next_grid_y)
        
        # Update sprite facing direction based on movement direction
        dx = self.next_grid_x - self.grid_x
        dy = self.next_grid_y - self.grid_y
        
        if abs(dx) > abs(dy):
            self.facing = 'right' if dx > 0 else 'left'
        else:
            self.facing = 'down' if dy > 0 else 'up'
            
        if hasattr(self, 'sprite') and self.sprite:
            self.sprite.set_direction(self.facing)
            
        # Reset movement progress
        self.move_progress = 0.0
        
        game_logger.debug(f"Moving from ({self.grid_x}, {self.grid_y}) to ({self.next_grid_x}, {self.next_grid_y})")
        
        return True

    def _start_next_move(self):
        """Start moving to the next position in the movement queue."""
        game_logger.debug(f"_start_next_move: Queue size: {len(self.movement_queue) if hasattr(self, 'movement_queue') else 'N/A'})")
        
        # If no more movements in queue, stop moving
        if not hasattr(self, 'movement_queue') or not self.movement_queue:
            game_logger.debug("_start_next_move: No movement queue or queue is empty")
            self.moving = False
            
            # Call the arrival callback if it exists
            if hasattr(self, 'on_arrival_callback') and self.on_arrival_callback:
                try:
                    game_logger.debug("Calling arrival callback")
                    self.on_arrival_callback()
                except Exception as e:
                    game_logger.error(f"Error in arrival callback: {e}")
                finally:
                    self.on_arrival_callback = None
            return
            
        # Get the next position from the queue
        next_pos = self.movement_queue.popleft()
        
        # If we got a grid position, convert it to screen coordinates
        if len(next_pos) == 2:  # It's a grid position
            target_x, target_y = next_pos
            # Convert grid to screen coordinates if needed
            if hasattr(self, 'world_state') and hasattr(self.world_state, 'world_to_screen'):
                target_x, target_y = self.world_state.world_to_screen(target_x, target_y)
            
            # Store the target grid position
            self.grid_x, self.grid_y = next_pos
        else:  # It's already screen coordinates
            target_x, target_y = next_pos
            # Convert screen to grid coordinates
            if hasattr(self, 'world_state') and hasattr(self.world_state, 'screen_to_world'):
                self.grid_x, self.grid_y = self.world_state.screen_to_world(target_x, target_y)
        
        # Store starting position for smooth movement
        self.start_x = float(self.x)
        self.start_y = float(self.y)
        self.target_x = float(target_x)
        self.target_y = float(target_y)
        
        # Calculate direction for sprite animation
        dx = 0
        dy = 0
        if abs(self.target_x - self.start_x) > abs(self.target_y - self.start_y):
            dx = 1 if self.target_x > self.start_x else -1
        else:
            dy = 1 if self.target_y > self.start_y else -1
        self.move_direction = (dx, dy)
        
        # Update sprite facing direction
        if dx > 0:
            self.facing = 'right'
        elif dx < 0:
            self.facing = 'left'
        elif dy > 0:
            self.facing = 'down'
        elif dy < 0:
            self.facing = 'up'
            
        if hasattr(self, 'sprite') and self.sprite:
            self.sprite.set_direction(self.facing)
        
        # Start movement
        self.moving = True
        self.move_progress = 0.0
        self.last_move_tick = getattr(self.world_state, 'game_ticks', 0)
        
        game_logger.debug(f"Starting smooth movement from ({self.start_x}, {self.start_y}) to ({self.target_x}, {self.target_y})")
    
    def update(self, current_time):
        """Update the player's movement and position based on game ticks."""
        try:
            # Get current game tick and tick information from world state
            current_tick = getattr(self.world_state, 'game_ticks', 0)
            tick_interval = getattr(self.world_state, 'tick_interval', 300) / 1000.0  # Convert to seconds
            last_tick_time = getattr(self.world_state, 'last_tick_time', current_time - 16)
            
            # Calculate delta time since last update
            dt = 1.0 / 60.0  # Default delta time if we can't calculate it
            if hasattr(self, '_last_update_time'):
                dt = (current_time - self._last_update_time) / 1000.0  # Convert to seconds
            self._last_update_time = current_time
            
            # Handle movement
            if self.moving:
                # Check if we're on a new game tick
                if current_tick > self.last_move_tick:
                    # Check if this is the first movement (queued movement)
                    if hasattr(self, 'movement_queued') and self.movement_queued:
                        # Start the movement on this tick
                        self.movement_queued = False
                        # This is when we actually start moving - set the flag here
                        self.actually_moving = True
                        
                        # Now that we're actually moving, set the sprite's walking state
                        # THIS IS THE ONLY PLACE WHERE walking SHOULD BE SET TO TRUE
                        if hasattr(self, 'sprite') and self.sprite:
                            self.sprite.walking = True
                            # Start animation from beginning
                            self.sprite.animation_time = 0
                            
                        game_logger.debug(f"Starting queued movement on tick {current_tick}")
                        
                    # Check if we need to finalize the last movement
                    elif hasattr(self, 'final_tile_pending') and self.final_tile_pending:
                        # Update grid position to the final tile
                        self.grid_x, self.grid_y = self.next_grid_x, self.next_grid_y
                        
                        # Remove the tiles we've moved through
                        tiles_to_remove = getattr(self, 'tiles_to_remove', 1)
                        for _ in range(min(tiles_to_remove, len(self.path))):
                            self.path.pop(0)
                            
                        self.final_tile_pending = False
                        
                        # If we've reached the end of the path
                        if not self.path:
                            self.moving = False
                            self.actually_moving = False
                            self.path = []          
                            # Call the arrival callback if it exists
                            if hasattr(self, 'on_arrival_callback') and self.on_arrival_callback:
                                try:
                                    self.on_arrival_callback()
                                except Exception as e:
                                    game_logger.error(f"Error in arrival callback: {e}")
                                finally:
                                    self.on_arrival_callback = None
                    
                    # We've moved to a new tick, process the movement for this tick if still moving
                    if self.moving and self.path:
                        self._process_movement_for_tick(current_tick)
                
                # Always do smooth visual interpolation between positions
                # Get current position in screen coordinates
                current_x, current_y = self.world_state.world_to_screen(self.grid_x, self.grid_y)
                
                # Determine the next position to move towards
                if hasattr(self, 'path') and self.path:
                    # Calculate how far we should be between current position and next position
                    # based on time since last tick
                    time_since_tick = (current_time - last_tick_time) / 1000.0
                    progress = min(1.0, time_since_tick / tick_interval)
                    
                    # Get the next position (either from next_grid_x/y or from path)
                    if hasattr(self, 'next_grid_x') and hasattr(self, 'next_grid_y'):
                        next_x, next_y = self.world_state.world_to_screen(self.next_grid_x, self.next_grid_y)
                    elif self.path:
                        next_x, next_y = self.world_state.world_to_screen(self.path[0][0], self.path[0][1])
                    else:
                        next_x, next_y = current_x, current_y
                    
                    # Store the start position for this movement segment if not already set
                    if not hasattr(self, 'movement_start_x') or not hasattr(self, 'movement_start_y'):
                        self.movement_start_x = current_x
                        self.movement_start_y = current_y
                        self.movement_target_x = next_x
                        self.movement_target_y = next_y
                    
                    # Interpolate position for smooth movement
                    # Use the stored start and target positions to avoid jumps
                    self.x = self.movement_start_x + (self.movement_target_x - self.movement_start_x) * progress
                    self.y = self.movement_start_y + (self.movement_target_y - self.movement_start_y) * progress
                    
                    # Update the rect position
                    if hasattr(self, 'rect'):
                        self.rect.centerx = int(self.x)
                        self.rect.centery = int(self.y) - self.character_y_offset  # Apply character y offset
                else:
                    # No path, just stay at current position
                    self.x = current_x
                    self.y = current_y
                    if hasattr(self, 'rect'):
                        self.rect.centerx = int(self.x)
                        self.rect.centery = int(self.y) - self.character_y_offset  # Apply character y offset
            
            # Always update the sprite direction based on facing
            if hasattr(self, 'sprite') and self.sprite:
                # Convert facing direction to sprite direction
                sprite_direction = None
                if hasattr(self, 'facing'):
                    if self.facing == 'left':
                        sprite_direction = 1  # Left
                    elif self.facing == 'right':
                        sprite_direction = 3  # Right
                    elif self.facing == 'up':
                        sprite_direction = 2  # Up
                    else:  # down or default
                        sprite_direction = 0  # Down
                
                # CRITICAL: Only update the walking state if we're actually moving
                # This ensures the walking animation only plays when physically moving
                is_moving = self.actually_moving
                
                # Update the sprite with the current direction and walking state
                self.sprite.update(dt, is_moving=is_moving, direction=sprite_direction)
                
        except Exception as e:
            game_logger.error(f"Error in player update: {e}")
            import traceback
            traceback.print_exc()
            
    def _process_movement_for_tick(self, current_tick):
        """Process movement for the current game tick."""
        # If we're not moving or have no path, do nothing
        if not self.moving or not self.path:
            return
            
        # We can move up to 2 tiles per tick
        tiles_to_move = min(len(self.path), self.tiles_per_move)
        
        # Store the tiles we'll move through in this tick
        tiles_for_this_tick = self.path[:tiles_to_move]
        
        # Set up the movement segment
        start_tile = (self.grid_x, self.grid_y)
        end_tile = tiles_for_this_tick[-1]  # Last tile in this tick's movement
        
        # Calculate screen coordinates
        start_pos = self.world_state.world_to_screen(start_tile[0], start_tile[1])
        end_pos = self.world_state.world_to_screen(end_tile[0], end_tile[1])
        
        # Store the movement information for smooth interpolation
        self.movement_start_x = start_pos[0]
        self.movement_start_y = start_pos[1]
        self.movement_target_x = end_pos[0]
        self.movement_target_y = end_pos[1]
        
        # Update the grid position to the end of this segment
        # (visual position will be interpolated)
        self.next_grid_x, self.next_grid_y = end_tile
        
        # Update direction based on movement
        dx = self.next_grid_x - self.grid_x
        dy = self.next_grid_y - self.grid_y
        
        if abs(dx) > abs(dy):
            self.facing = 'right' if dx > 0 else 'left'
        else:
            self.facing = 'down' if dy > 0 else 'up'
            
        if hasattr(self, 'sprite') and self.sprite:
            self.sprite.set_direction(self.facing)
        
        # Mark this segment for completion in the next tick
        self.final_tile_pending = True
        self.tiles_to_remove = tiles_to_move
        
        # Update the last move tick
        self.last_move_tick = current_tick
        
        game_logger.debug(f"Movement segment: {start_tile} to {end_tile}, removing {tiles_to_move} tiles next tick")
            
        # Ensure position is valid
        if not hasattr(self, 'world_state') or not hasattr(self.world_state, 'width') or not hasattr(self.world_state, 'height'):
            return
            
        # Clamp position to world bounds
        max_x = (self.world_state.width - 1) * self.world_state.tile_size
        max_y = (self.world_state.height - 1) * self.world_state.tile_size
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))
        
        # Update sprite position
        if hasattr(self, 'sprite') and self.sprite and hasattr(self.sprite, 'rect'):
            self.sprite.rect.centerx = int(self.x)
            self.sprite.rect.centery = int(self.y)
        
        # Call the arrival callback if it exists (outside the try-except)
        if hasattr(self, 'on_arrival_callback') and self.on_arrival_callback and not self.moving:
            try:
                game_logger.debug("Calling arrival callback")
                self.on_arrival_callback()
            except Exception as e:
                game_logger.error(f"Error in arrival callback: {e}")
            finally:
                self.on_arrival_callback = None
        
        # Start the next move if there are more moves in the queue
        if hasattr(self, 'movement_queue') and self.movement_queue and not self.moving:
            self._start_next_move()
                
    def draw(self, screen, camera_x=0, camera_y=0, debug=False):
        """
        Draw the player on the screen.
        
        Args:
            screen: The surface to draw on
            camera_x: Camera x offset
            camera_y: Camera y offset
            debug: If True, draw debug information
        """
        if not screen or not hasattr(screen, 'blit') or not hasattr(self, 'sprite') or not self.sprite:
            return
            
        try:
            # Ensure we have valid position
            if not hasattr(self, 'x') or not hasattr(self, 'y'):
                return
                
            # Calculate screen position with camera offset
            screen_x = int(self.x - camera_x)
            screen_y = int(self.y - camera_y)
            
            # Skip drawing if off-screen (with some margin for sprites that might be partially visible)
            margin = 128  # Increased margin to account for sprite size
            if (screen_x < -margin or screen_x > screen.get_width() + margin or 
                screen_y < -margin or screen_y > screen.get_height() + margin):
                return
            
            # Update animation state
            self.sprite.walking = hasattr(self, 'moving') and self.moving
            
            # Update sprite facing direction
            if hasattr(self, 'facing'):
                if self.facing == 'left':
                    self.sprite.direction = 1  # Left
                elif self.facing == 'right':
                    self.sprite.direction = 3  # Right
                elif self.facing == 'up':
                    self.sprite.direction = 2  # Up
                else:  # down or default
                    self.sprite.direction = 0  # Down
            
            # Draw the sprite at the current position
            # Make sure to update the rect position first
            self.rect.centerx = screen_x
            self.rect.centery = screen_y
            self.sprite.rect = self.rect
            
            # Draw the sprite with feet at the specified position, applying the y offset
            self.sprite.draw(screen, screen_x, screen_y - self.character_y_offset)
            
            # Draw debug information
            if debug:
                # Draw player position
                font = pygame.font.Font(None, 20)
                pos_text = f"Player: ({int(self.x)}, {int(self.y)}) Grid: ({self.grid_x}, {self.grid_y})"
                text_surface = font.render(pos_text, True, (255, 255, 255), (0, 0, 0))
                screen.blit(text_surface, (screen_x - text_surface.get_width() // 2, screen_y - 50))
                
                # Draw movement target
                if hasattr(self, 'target_x') and hasattr(self, 'target_y'):
                    target_screen_x = int(self.target_x - camera_x)
                    target_screen_y = int(self.target_y - camera_y)
                    pygame.draw.circle(screen, (255, 0, 0), (target_screen_x, target_screen_y), 5)
                    pygame.draw.line(screen, (255, 0, 0), (screen_x, screen_y), 
                                   (target_screen_x, target_screen_y), 1)
                
                # Draw movement queue
                if hasattr(self, 'movement_queue') and self.movement_queue:
                    prev_x, prev_y = screen_x, screen_y
                    for i, (gx, gy) in enumerate(self.movement_queue):
                        qx, qy = self.world_state.world_to_screen(gx, gy)
                        qx -= camera_x
                        qy -= camera_y
                        pygame.draw.circle(screen, (0, 255, 0) if i == 0 else (0, 200, 0), 
                                        (int(qx), int(qy)), 3)
                        pygame.draw.line(screen, (0, 200, 0), (prev_x, prev_y), (int(qx), int(qy)), 1)
                        prev_x, prev_y = int(qx), int(qy)
                
                # Draw sprite rect
                if hasattr(self.sprite, 'rect'):
                    rect = self.sprite.rect.copy()
                    rect.x -= camera_x
                    rect.y -= camera_y
                    pygame.draw.rect(screen, (255, 255, 0), rect, 1)

        except Exception as e:
            import traceback
            error_msg = f"Error in player draw: {e}\n{traceback.format_exc()}"
            game_logger.error(error_msg)
            # Try to draw error text on screen
            try:
                font = pygame.font.Font(None, 24)
                error_surface = font.render("Player draw error", True, (255, 0, 0))
                screen.blit(error_surface, (10, 10))
            except:
                pass

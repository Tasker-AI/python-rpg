import pygame
import math

class HumanSprite:
    """
    A class that renders a human-like character with separate body parts.
    """
    def __init__(self, color=(0, 0, 255)):
        try:
            print("Initializing HumanSprite...")
            # Initialize rect attribute (will be updated in draw method)
            self.rect = pygame.Rect(0, 0, 32, 32)
            
            # Body part colors
            self.body_color = color
            self.head_color = (255, 218, 185)  # Peach color for head
            self.feet_color = (139, 69, 19)    # Brown for feet/shoes
            
            # Body part sizes and positions (relative to center point)
            self.head_radius = 6  # Smaller head radius for better proportions
            self.body_width = 16
            self.body_height = 20
            self.arm_width = 6
            self.arm_height = 16
            self.leg_width = 6
            self.leg_height = 14
            self.foot_width = 8
            self.foot_height = 4
            
            # Animation state
            self.walking = False
            self.animation_time = 0
            self.animation_speed = 5  # Animation cycles per second
            
            # Direction (0=down, 1=left, 2=up, 3=right)
            self.direction = 0
            
            # Create surfaces for caching the rendered sprite in each direction
            self.cached_sprites = {
                'standing': [None, None, None, None],  # Down, Left, Up, Right
                'walking1': [None, None, None, None],
                'walking2': [None, None, None, None]
            }
            
            # Generate the cached sprites
            print("Generating cached sprites...")
            self._generate_cached_sprites()
            print("Cached sprites generated")
            
            # Verify all sprites were created
            for state in ['standing', 'walking1', 'walking2']:
                for i, sprite in enumerate(self.cached_sprites[state]):
                    if sprite is None:
                        print(f"Warning: {state} sprite {i} is None!")
                    elif not hasattr(sprite, 'get_width'):
                        print(f"Warning: {state} sprite {i} is not a valid surface!")
                        
        except Exception as e:
            print(f"Error initializing HumanSprite: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _generate_cached_sprites(self):
        """Generate and cache all sprite animations and directions.
        
        This method creates surfaces for each animation state (standing, walking1, walking2)
        in all four directions (down, left, up, right).
        """
        try:
            print("Starting sprite generation...")
            sprite_size = 48  # Size of the sprite surface (square)
            
            # Define poses and their corresponding states
            poses = [
                (0, 'standing'),
                (1, 'walking1'),
                (2, 'walking2')
            ]
            
            # Generate all poses for all directions
            for direction in range(4):
                try:
                    print(f"Generating sprites for direction {direction}...")
                    
                    for pose_num, state in poses:
                        try:
                            # Create a new surface with per-pixel alpha
                            surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                            if surface is None or not hasattr(surface, 'blit'):
                                print(f"Error: Failed to create surface for direction {direction}, {state}")
                                continue
                                
                            # Clear the surface with transparent color
                            surface.fill((0, 0, 0, 0))
                            
                            # Calculate center position
                            center_x = sprite_size // 2
                            center_y = sprite_size // 2
                            
                            # Temporarily set the direction for this sprite
                            original_direction = self.direction
                            self.direction = direction
                            
                            # Draw the character in the current pose and direction
                            self._draw_human(surface, center_x, center_y, pose_num)
                            
                            # Restore the original direction
                            self.direction = original_direction
                            
                            # Store the surface in the cache
                            self.cached_sprites[state][direction] = surface
                            
                            # Verify the surface is valid
                            if not hasattr(surface, 'get_width') or surface.get_width() == 0:
                                print(f"Warning: Invalid surface generated for {state}, direction {direction}")
                                
                        except Exception as e:
                            print(f"Error generating {state} sprite for direction {direction}: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    print(f"Successfully generated sprites for direction {direction}")
                    
                except Exception as e:
                    print(f"Critical error generating sprites for direction {direction}: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Verify all sprites were created
            missing = []
            for state, directions in self.cached_sprites.items():
                for i, sprite in enumerate(directions):
                    if sprite is None or not hasattr(sprite, 'blit'):
                        missing.append(f"{state} direction {i}")
            
            if missing:
                print(f"Warning: Failed to generate {len(missing)} sprites: {', '.join(missing)}")
                
                # Create fallback sprites for missing ones
                fallback = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
                pygame.draw.rect(fallback, (255, 0, 0, 128), (0, 0, sprite_size, sprite_size))
                font = pygame.font.Font(None, 24)
                text = font.render('SPRITE', True, (255, 255, 255))
                text_rect = text.get_rect(center=(sprite_size//2, sprite_size//2))
                fallback.blit(text, text_rect)
                
                for state, directions in self.cached_sprites.items():
                    for i in range(len(directions)):
                        if directions[i] is None or not hasattr(directions[i], 'blit'):
                            self.cached_sprites[state][i] = fallback
                            
            print("Sprite generation complete")
            
        except Exception as e:
            print(f"Critical error in _generate_cached_sprites: {e}")
            import traceback
            traceback.print_exc()
            # Try to continue with whatever sprites we could generate
    
    def _draw_human(self, surface, center_x, center_y, pose):
        """Draw a human figure with all body parts."""
        # Adjust positions based on direction
        if self.direction == 0:  # Down
            self._draw_human_front(surface, center_x, center_y, pose)
        elif self.direction == 1:  # Left
            self._draw_human_side(surface, center_x, center_y, pose, flip=True)
        elif self.direction == 2:  # Up
            self._draw_human_back(surface, center_x, center_y, pose)
        elif self.direction == 3:  # Right
            self._draw_human_side(surface, center_x, center_y, pose, flip=False)
    
    def _draw_human_front(self, surface, center_x, center_y, pose):
        """Draw human from front view."""
        # Calculate offsets based on pose
        leg_offset = 0
        arm_offset = 0
        
        if pose == 1:  # Walking pose 1
            leg_offset = 3
            arm_offset = 2
        elif pose == 2:  # Walking pose 2
            leg_offset = -3
            arm_offset = -2
        # For pose 0 (idle), ensure we still have a small offset so feet are visible
        elif pose == 0:  # Idle pose
            leg_offset = 1  # Small offset to make feet visible
        
        # Draw body - this is our reference point for alignment
        body_rect = pygame.Rect(
            center_x - self.body_width // 2,
            center_y - self.body_height // 2,
            self.body_width,
            self.body_height
        )
        pygame.draw.rect(surface, self.body_color, body_rect, 0, 3)
        
        # Draw head - centered exactly above the body
        head_y = center_y - self.body_height // 2 - self.head_radius - 2
        pygame.draw.circle(surface, self.head_color, (center_x, head_y), self.head_radius)
        
        # Draw arms - positioned at the sides of the body
        # Left arm
        left_arm_rect = pygame.Rect(
            center_x - self.body_width // 2 - self.arm_width + 2,
            center_y - self.arm_height // 2 + arm_offset,
            self.arm_width,
            self.arm_height
        )
        # Draw left arm with 1px border
        pygame.draw.rect(surface, self.body_color, left_arm_rect, 0, 2)
        pygame.draw.rect(surface, (0, 0, 0), left_arm_rect, 1, 2)  # Black 1px border
        
        # Add a hand at the end of the left arm
        hand_size = 5
        left_hand_rect = pygame.Rect(
            center_x - self.body_width // 2 - self.arm_width + 2 + (self.arm_width - hand_size) // 2,
            center_y - self.arm_height // 2 + arm_offset + self.arm_height - hand_size,
            hand_size,
            hand_size
        )
        # Draw left hand with 1px border
        pygame.draw.rect(surface, self.head_color, left_hand_rect, 0, 2)  # Same color as head (skin tone)
        pygame.draw.rect(surface, (0, 0, 0), left_hand_rect, 1, 2)  # Black 1px border
        
        # Right arm
        right_arm_rect = pygame.Rect(
            center_x + self.body_width // 2 - 2,
            center_y - self.arm_height // 2 - arm_offset,
            self.arm_width,
            self.arm_height
        )
        # Draw right arm with 1px border
        pygame.draw.rect(surface, self.body_color, right_arm_rect, 0, 2)
        pygame.draw.rect(surface, (0, 0, 0), right_arm_rect, 1, 2)  # Black 1px border
        
        # Add a hand at the end of the right arm
        right_hand_rect = pygame.Rect(
            center_x + self.body_width // 2 - 2 + (self.arm_width - hand_size) // 2,
            center_y - self.arm_height // 2 - arm_offset + self.arm_height - hand_size,
            hand_size,
            hand_size
        )
        # Draw right hand with 1px border
        pygame.draw.rect(surface, self.head_color, right_hand_rect, 0, 2)  # Same color as head (skin tone)
        pygame.draw.rect(surface, (0, 0, 0), right_hand_rect, 1, 2)  # Black 1px border
        
        # Draw legs perfectly centered under the body
        # For perfect centering, calculate exact center and position legs symmetrically
        leg_gap = 2  # Small gap between legs
        total_width = (self.leg_width * 2) + leg_gap
        
        # Calculate left leg position (exactly half of total width to the left of center)
        left_leg_x = center_x - (total_width / 2)
        
        # Draw left leg
        left_leg_rect = pygame.Rect(
            left_leg_x,
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height - leg_offset
        )
        pygame.draw.rect(surface, self.body_color, left_leg_rect, 0, 2)
        
        # Draw right leg (left leg position + leg width + gap)
        right_leg_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap,
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height + leg_offset
        )
        pygame.draw.rect(surface, self.body_color, right_leg_rect, 0, 2)
        
        # Draw feet centered under the legs
        foot_offset = (self.foot_width - self.leg_width) // 2
        
        # Draw left foot
        left_foot_rect = pygame.Rect(
            left_leg_x - foot_offset,
            center_y + self.body_height // 2 + self.leg_height - leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, left_foot_rect, 0, 2)
        
        # Draw right foot
        right_foot_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap - foot_offset,
            center_y + self.body_height // 2 + self.leg_height + leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, right_foot_rect, 0, 2)
    
    def _draw_human_back(self, surface, center_x, center_y, pose):
        """Draw human from back view."""
        # Calculate offsets based on pose
        leg_offset = 0
        arm_offset = 0
        
        if pose == 1:  # Walking pose 1
            leg_offset = 3
            arm_offset = 2
        elif pose == 2:  # Walking pose 2
            leg_offset = -3
            arm_offset = -2
        
        # Draw body (centered rectangle)
        body_rect = pygame.Rect(
            center_x - self.body_width // 2,
            center_y - self.body_height // 2,
            self.body_width,
            self.body_height
        )
        pygame.draw.rect(surface, self.body_color, body_rect, 0, 3)
        
        # Draw head (back of head, same color as body) - centered exactly above the body
        head_y = center_y - self.body_height // 2 - self.head_radius - 2
        pygame.draw.circle(surface, self.body_color, (center_x, head_y), self.head_radius)
        
        # Draw arms - positioned at the sides of the body
        # Left arm (from back view, so on right side of screen)
        left_arm_rect = pygame.Rect(
            center_x + self.body_width // 2 - 2,
            center_y - self.arm_height // 2 + arm_offset,
            self.arm_width,
            self.arm_height
        )
        # Draw left arm with 1px border
        pygame.draw.rect(surface, self.body_color, left_arm_rect, 0, 2)
        pygame.draw.rect(surface, (0, 0, 0), left_arm_rect, 1, 2)  # Black 1px border
        
        # Add a hand at the end of the left arm
        hand_size = 5
        left_hand_rect = pygame.Rect(
            center_x + self.body_width // 2 - 2 + (self.arm_width - hand_size) // 2,
            center_y - self.arm_height // 2 + arm_offset + self.arm_height - hand_size,
            hand_size,
            hand_size
        )
        # Draw left hand with 1px border
        pygame.draw.rect(surface, self.body_color, left_hand_rect, 0, 2)  # Same color as body for back view
        pygame.draw.rect(surface, (0, 0, 0), left_hand_rect, 1, 2)  # Black 1px border
        
        # Right arm (from back view, so on left side of screen)
        right_arm_rect = pygame.Rect(
            center_x - self.body_width // 2 - self.arm_width + 2,
            center_y - self.arm_height // 2 - arm_offset,
            self.arm_width,
            self.arm_height
        )
        # Draw right arm with 1px border
        pygame.draw.rect(surface, self.body_color, right_arm_rect, 0, 2)
        pygame.draw.rect(surface, (0, 0, 0), right_arm_rect, 1, 2)  # Black 1px border
        
        # Add a hand at the end of the right arm
        right_hand_rect = pygame.Rect(
            center_x - self.body_width // 2 - self.arm_width + 2 + (self.arm_width - hand_size) // 2,
            center_y - self.arm_height // 2 - arm_offset + self.arm_height - hand_size,
            hand_size,
            hand_size
        )
        # Draw right hand with 1px border
        pygame.draw.rect(surface, self.body_color, right_hand_rect, 0, 2)  # Same color as body for back view
        pygame.draw.rect(surface, (0, 0, 0), right_hand_rect, 1, 2)  # Black 1px border
        
        # Draw legs perfectly centered under the body (from back view)
        # For perfect centering, calculate exact center and position legs symmetrically
        leg_gap = 2  # Small gap between legs
        total_width = (self.leg_width * 2) + leg_gap
        
        # Calculate left leg position (exactly half of total width to the left of center)
        left_leg_x = center_x - (total_width / 2)
        
        # Draw left leg (from back view, so on right side of screen)
        left_leg_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap,  # Right side position
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height - leg_offset
        )
        pygame.draw.rect(surface, self.body_color, left_leg_rect, 0, 2)
        
        # Draw right leg (from back view, so on left side of screen)
        right_leg_rect = pygame.Rect(
            left_leg_x,  # Left side position
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height + leg_offset
        )
        pygame.draw.rect(surface, self.body_color, right_leg_rect, 0, 2)
        
        # Draw feet centered under the legs (from back view)
        foot_offset = (self.foot_width - self.leg_width) // 2
        
        # Draw left foot (from back view, so on right side of screen)
        left_foot_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap - foot_offset,
            center_y + self.body_height // 2 + self.leg_height - leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, left_foot_rect, 0, 2)
        
        # Draw right foot (from back view, so on left side of screen)
        right_foot_rect = pygame.Rect(
            left_leg_x - foot_offset,
            center_y + self.body_height // 2 + self.leg_height + leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, right_foot_rect, 0, 2)
    
    def _draw_human_side(self, surface, center_x, center_y, pose, flip=False):
        """Draw human from side view."""
        # Calculate offsets based on pose
        leg_offset = 0
        arm_offset = 0
        
        if pose == 1:  # Walking pose 1
            leg_offset = 3
            arm_offset = 2
        elif pose == 2:  # Walking pose 2
            leg_offset = -3
            arm_offset = -2
        # For pose 0 (idle), ensure we still have a small offset so feet are visible
        elif pose == 0:  # Idle pose
            leg_offset = 1  # Small offset to make feet visible
        
        # COMPLETELY NEW APPROACH: Draw everything as a single unit
        # Define the center line of the character (vertical line through center)
        center_line_x = center_x
        
        # Draw body (narrower for side view)
        body_width = 12  # Fixed width for side view
        body_rect = pygame.Rect(
            center_line_x - body_width // 2,
            center_y - self.body_height // 2,
            body_width,
            self.body_height
        )
        pygame.draw.rect(surface, self.body_color, body_rect, 0, 3)
        
        # Draw head directly above body center
        head_y = center_y - self.body_height // 2 - self.head_radius - 2
        pygame.draw.circle(surface, self.head_color, (center_line_x, head_y), self.head_radius)
        
        # Draw arm centered with the body
        # In side view, we only see one arm (the one in front)
        arm_rect = pygame.Rect(
            center_line_x - self.arm_width // 2,  # Perfectly centered with body
            center_y - self.arm_height // 2 + arm_offset,
            self.arm_width,
            self.arm_height
        )
        # Draw arm with 1px border
        pygame.draw.rect(surface, self.body_color, arm_rect, 0, 2)
        pygame.draw.rect(surface, (0, 0, 0), arm_rect, 1, 2)  # Black 1px border
        
        # Add a hand at the end of the arm
        hand_size = 5
        hand_rect = pygame.Rect(
            center_line_x - hand_size // 2,  # Centered with arm
            center_y - self.arm_height // 2 + arm_offset + self.arm_height - hand_size,  # At end of arm
            hand_size,
            hand_size
        )
        # Draw hand with 1px border
        pygame.draw.rect(surface, self.head_color, hand_rect, 0, 2)  # Same color as head (skin tone)
        pygame.draw.rect(surface, (0, 0, 0), hand_rect, 1, 2)  # Black 1px border
        
        # Draw two legs very close together, both under the torso
        leg_gap = 1  # Minimal gap between legs
        leg_total_width = (self.leg_width * 2) + leg_gap
        
        # Calculate left leg position (exactly half of total width to the left of center)
        left_leg_x = center_line_x - (leg_total_width / 2)
        
        # Draw left leg
        left_leg_rect = pygame.Rect(
            left_leg_x,
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height - leg_offset
        )
        pygame.draw.rect(surface, self.body_color, left_leg_rect, 0, 2)
        
        # Draw right leg
        right_leg_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap,
            center_y + self.body_height // 2,
            self.leg_width,
            self.leg_height + leg_offset
        )
        pygame.draw.rect(surface, self.body_color, right_leg_rect, 0, 2)
        
        # Draw feet centered under each leg
        foot_offset = (self.foot_width - self.leg_width) // 2
        
        # Draw left foot
        left_foot_rect = pygame.Rect(
            left_leg_x - foot_offset,
            center_y + self.body_height // 2 + self.leg_height - leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, left_foot_rect, 0, 2)
        
        # Draw right foot
        right_foot_rect = pygame.Rect(
            left_leg_x + self.leg_width + leg_gap - foot_offset,
            center_y + self.body_height // 2 + self.leg_height + leg_offset,
            self.foot_width,
            self.foot_height
        )
        pygame.draw.rect(surface, self.feet_color, right_foot_rect, 0, 2)
    
    def set_direction(self, direction_str):
        """Set the sprite direction based on a string direction.
        
        Args:
            direction_str: String direction ('up', 'down', 'left', 'right')
        """
        direction_map = {
            'down': 0,
            'left': 1,
            'up': 2,
            'right': 3
        }
        self.direction = direction_map.get(direction_str, 0)  # Default to down if invalid
        
    def update(self, delta_time, is_moving=False, direction=None):
        """Update the sprite animation.
        
        Args:
            delta_time: Time since last update in seconds
            is_moving: Whether the character is currently moving
            direction: Optional direction to face (0=down, 1=left, 2=up, 3=right)
        """
        if direction is not None:
            self.direction = direction
        
        # Update walking state
        was_walking = self.walking
        self.walking = is_moving
        
        # Reset animation time when starting to walk
        if not was_walking and self.walking:
            self.animation_time = 0
        
        # Update animation time when walking
        if self.walking:
            # Update animation time based on movement speed
            self.animation_time += delta_time * 6  # Adjust this value to control animation speed
        
        # Keep animation_time from getting too large
        if self.animation_time > 1000:
            self.animation_time = 0
    
    def get_current_frame(self):
        """Get the current animation frame based on state.
        
        Returns:
            pygame.Surface: A valid surface to draw
        """
        try:
            # Determine which animation state to use
            state = 'walking1' if int(self.animation_time) % 2 == 0 else 'walking2' if self.walking else 'standing'
            
            # Get the frame for the current direction
            frame = self.cached_sprites[state][self.direction % 4]  # Use modulo to ensure valid index
            
            # If we got a valid frame, return it
            if frame is not None and hasattr(frame, 'blit'):
                return frame
                
            # Fall back to standing frame if available
            if state != 'standing':
                frame = self.cached_sprites['standing'][self.direction % 4]
                if frame is not None and hasattr(frame, 'blit'):
                    return frame
            
            # If we still don't have a valid frame, try to generate one
            print(f"Warning: Missing frame for state '{state}', direction {self.direction}")
            self._generate_cached_sprites()  # Try to regenerate sprites
            frame = self.cached_sprites['standing'][0]  # Try to get default standing frame
            
            if frame is not None and hasattr(frame, 'blit'):
                return frame
                
        except Exception as e:
            print(f"Error in get_current_frame: {e}")
            import traceback
            traceback.print_exc()
        
        # As a last resort, create a default red surface
        default_surface = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.rect(default_surface, (255, 0, 0, 128), (0, 0, 48, 48))
        font = pygame.font.Font(None, 24)
        text = font.render('Sprite', True, (255, 255, 255))
        text_rect = text.get_rect(center=(24, 24))
        default_surface.blit(text, text_rect)
        return default_surface
    def get_current_frame(self):
        """
        Get the current animation frame based on the sprite's state and direction.
        
        Returns:
            pygame.Surface: The current frame to display
        """
        try:
            # Determine the animation state based on walking and animation time
            if self.walking:
                state = 'walking1' if int(self.animation_time) % 2 == 0 else 'walking2'
            else:
                state = 'standing'
                
            # Get the frame for the current direction
            frame = self.cached_sprites[state][self.direction]
            
            # If the frame is invalid, fall back to standing frame
            if frame is None or not hasattr(frame, 'blit'):
                frame = self.cached_sprites['standing'][self.direction]
                
            # If still invalid, use any valid frame
            if frame is None or not hasattr(frame, 'blit'):
                for state_name, directions in self.cached_sprites.items():
                    for dir_frame in directions:
                        if dir_frame is not None and hasattr(dir_frame, 'blit'):
                            return dir_frame
                            
                # If we still don't have a valid frame, create a default one
                return self._create_default_surface()
                
            return frame
            
        except Exception as e:
            print(f"Error in get_current_frame: {e}")
            import traceback
            traceback.print_exc()
            return self._create_default_surface()
    
    def set_direction(self, facing):
        """
        Set the sprite's direction based on the facing string.
        
        Args:
            facing (str): Direction to face ('up', 'down', 'left', 'right')
        """
        try:
            # Convert facing string to direction number
            if facing == 'left':
                self.direction = 1  # Left
            elif facing == 'right':
                self.direction = 3  # Right
            elif facing == 'up':
                self.direction = 2  # Up
            else:  # down or default
                self.direction = 0  # Down
                
        except Exception as e:
            print(f"Error setting direction: {e}")
            import traceback
            traceback.print_exc()
    
    def update(self, dt, is_moving=False, direction=None):
        """
        Update the sprite's animation state.
        
        Args:
            dt (float): Time elapsed since last update in seconds
            is_moving (bool): Whether the character is moving
            direction (int, optional): Direction to face (0=down, 1=left, 2=up, 3=right)
        """
        try:
            # Store old direction for debugging
            old_direction = self.direction
            
            # Update walking state
            self.walking = is_moving
            
            # Update direction if specified
            if direction is not None:
                # Only log if direction is changing
                if self.direction != direction:
                    print(f"Sprite direction changing from {old_direction} to {direction}, walking: {is_moving}")
                self.direction = direction
                
            # Update animation time if walking
            if self.walking:
                self.animation_time += dt * self.animation_speed
                
        except Exception as e:
            print(f"Error in sprite update: {e}")
            import traceback
            traceback.print_exc()
    
    def draw(self, surface, x, y):
        """
        Draw the sprite at the specified position.
        
        Args:
            surface: The pygame surface to draw on
            x: The x-coordinate to draw at (center point)
            y: The y-coordinate to draw at (center point)
        """
        try:
            # Skip if surface is invalid
            if not hasattr(surface, 'blit') or surface is None:
                return
                
            # Get the current frame
            frame = self.get_current_frame()
            
            # If we don't have a valid frame, try to regenerate sprites
            if frame is None or not hasattr(frame, 'blit'):
                print("Warning: Invalid frame, attempting to regenerate sprites...")
                self._generate_cached_sprites()
                frame = self.get_current_frame()
                
                # If still invalid, give up
                if frame is None or not hasattr(frame, 'blit'):
                    print("Error: Could not get valid frame after regeneration")
                    return
            
            # Ensure frame dimensions are valid
            try:
                frame_width = frame.get_width()
                frame_height = frame.get_height()
                if frame_width <= 0 or frame_height <= 0:
                    print(f"Error: Invalid frame dimensions: {frame_width}x{frame_height}")
                    return
            except (AttributeError, pygame.error) as e:
                print(f"Error getting frame dimensions: {e}")
                return
                
            # Calculate position to center the sprite
            try:
                # Convert to integers and ensure they're within reasonable bounds
                pos_x = int(round(x - frame_width // 2))
                pos_y = int(round(y - frame_height // 2))
                # Clamp values to reasonable bounds
                pos_x = max(-1000, min(10000, pos_x))
                pos_y = max(-1000, min(10000, pos_y))
            except (TypeError, ValueError) as e:
                print(f"Error calculating position: {e}")
                return
                
            # Draw the frame
            try:
                # Create a temporary surface if the frame has transparency
                if frame.get_flags() & pygame.SRCALPHA:
                    temp_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    temp_surface.blit(frame, (0, 0))
                    surface.blit(temp_surface, (pos_x, pos_y))
                else:
                    surface.blit(frame, (pos_x, pos_y))
                
                # Update the rect position for collision detection
                self.rect.x = pos_x
                self.rect.y = pos_y
                self.rect.width = frame_width
                self.rect.height = frame_height
                
                # Debug visualization removed - no more red rectangle
                    
            except Exception as e:
                print(f"Error drawing sprite: {e}")
                print(f"Position: ({pos_x}, {pos_y}), Frame size: {frame_width}x{frame_height}")
                print(f"Surface size: {surface.get_size() if hasattr(surface, 'get_size') else 'N/A'}")
                
        except Exception as e:
            print(f"Unexpected error in HumanSprite.draw: {e}")
            import traceback
            traceback.print_exc()

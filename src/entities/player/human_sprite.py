import pygame
import math

class HumanSprite:
    """
    A class that renders a human-like character with separate body parts.
    """
    def __init__(self, color=(0, 0, 255)):
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
        self._generate_cached_sprites()
    
    def _generate_cached_sprites(self):
        """Generate and cache all sprite animations and directions."""
        sprite_size = 48  # Size of the sprite surface (square)
        center_x = sprite_size // 2
        center_y = sprite_size // 2
        
        # Generate standing pose for all directions
        for direction in range(4):
            self.direction = direction
            
            # Standing pose
            surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            self._draw_human(surface, center_x, center_y, 0)  # 0 = standing
            self.cached_sprites['standing'][direction] = surface
            
            # Walking pose 1
            surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            self._draw_human(surface, center_x, center_y, 1)  # 1 = walking pose 1
            self.cached_sprites['walking1'][direction] = surface
            
            # Walking pose 2
            surface = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            self._draw_human(surface, center_x, center_y, 2)  # 2 = walking pose 2
            self.cached_sprites['walking2'][direction] = surface
    
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
    
    def update(self, delta_time, is_moving=False, direction=None):
        """Update the sprite animation."""
        if direction is not None:
            self.direction = direction
        
        self.walking = is_moving
        
        if self.walking:
            self.animation_time += delta_time * self.animation_speed
            if self.animation_time > 2:  # Reset after 2 frames
                self.animation_time = 0
    
    def get_current_frame(self):
        """Get the current animation frame based on state."""
        if not self.walking:
            return self.cached_sprites['standing'][self.direction]
        
        # Determine walking frame based on animation time
        frame = int(self.animation_time) % 2
        if frame == 0:
            return self.cached_sprites['walking1'][self.direction]
        else:
            return self.cached_sprites['walking2'][self.direction]
    
    def draw(self, surface, x, y):
        """Draw the sprite at the specified position."""
        current_frame = self.get_current_frame()
        surface.blit(current_frame, (x - 24, y - 24))  # Center the 48x48 sprite

import pygame
import math
from collections import deque

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
        
        # Path visualization
        self.current_path = []
        
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
    
    def move_to(self, pixel_x, pixel_y):
        """Set a target position for the player to move towards using pathfinding."""
        # Convert pixel coordinates to grid coordinates
        target_grid_x, target_grid_y = self.tilemap.pixel_to_grid(pixel_x, pixel_y)
        
        # Find path to target
        path = self.tilemap.find_path(self.grid_x, self.grid_y, target_grid_x, target_grid_y)
        
        # Clear current movement queue and add new path
        self.movement_queue.clear()
        self.current_path = path
        
        # Skip the first position (current position)
        if len(path) > 1:
            for x, y in path[1:]:
                self.movement_queue.append((x, y))
            
            # Start moving to the first position in the queue
            self.start_next_move()
    
    def start_next_move(self):
        """Start moving to the next position in the queue."""
        if self.movement_queue:
            self.next_grid_x, self.next_grid_y = self.movement_queue.popleft()
            self.moving = True
            self.move_progress = 0.0
        else:
            self.moving = False
            self.next_grid_x = None
            self.next_grid_y = None
            self.current_path = []
    
    def update(self, delta_time, tick_occurred=False):
        """Update player position and state."""
        if self.moving and self.next_grid_x is not None and self.next_grid_y is not None:
            if tick_occurred:
                # Complete the move on a game tick
                self.grid_x = self.next_grid_x
                self.grid_y = self.next_grid_y
                self.x, self.y = self.tilemap.grid_to_pixel(self.grid_x, self.grid_y)
                self.rect.x = self.x - 16
                self.rect.y = self.y - 16
                
                # Start next move if there are more in the queue
                self.start_next_move()
            else:
                # Smooth visual movement between ticks
                # Calculate progress based on time until next tick
                target_x, target_y = self.tilemap.grid_to_pixel(self.next_grid_x, self.next_grid_y)
                start_x, start_y = self.tilemap.grid_to_pixel(self.grid_x, self.grid_y)
                
                # Update visual position based on progress
                self.move_progress = min(1.0, self.move_progress + delta_time / 0.6)  # 0.6 seconds per tick
                self.x = start_x + (target_x - start_x) * self.move_progress
                self.y = start_y + (target_y - start_y) * self.move_progress
                
                # Update collision rectangle
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

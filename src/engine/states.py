import pygame
from src.engine.game_state import GameState

class MenuState(GameState):
    """Main menu state for the game"""
    def __init__(self):
        super().__init__()
        self.next_state = "play"
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.title_text = self.title_font.render("Python RPG", True, (255, 255, 255))
        self.start_text = self.font.render("Click to Start", True, (200, 200, 200))
        self.title_pos = (400, 200)
        self.start_pos = (400, 350)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Transition to play state on mouse click
                self.done = True
    
    def update(self, delta_time):
        # Pulse the start text color based on time
        pulse = (pygame.time.get_ticks() % 1000) / 1000.0
        brightness = 150 + int(105 * pulse)
        self.start_text = self.font.render("Click to Start", True, (brightness, brightness, brightness))
    
    def draw(self, screen):
        # Draw a dark background
        screen.fill((20, 20, 40))
        
        # Draw title and start text centered
        title_rect = self.title_text.get_rect(center=self.title_pos)
        start_rect = self.start_text.get_rect(center=self.start_pos)
        
        screen.blit(self.title_text, title_rect)
        screen.blit(self.start_text, start_rect)


class PlayState(GameState):
    """Main gameplay state"""
    def __init__(self):
        super().__init__()
        self.next_state = "menu"
        self.font = pygame.font.Font(None, 24)
        self.player_pos = [400, 300]
        self.target_pos = None
        self.player_speed = 200  # pixels per second
        self.game_ticks = 0
        self.tick_rate = 0.6  # seconds per tick
        self.tick_timer = 0
        
        # UI elements
        self.menu_button = pygame.Rect(700, 550, 80, 30)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if menu button was clicked
                if self.menu_button.collidepoint(event.pos):
                    self.done = True  # Return to menu
                else:
                    # Set target position for player to move to
                    self.target_pos = list(event.pos)
    
    def update(self, delta_time):
        # Handle player movement with click-to-move
        if self.target_pos:
            # Calculate direction vector to target
            dx = self.target_pos[0] - self.player_pos[0]
            dy = self.target_pos[1] - self.player_pos[1]
            
            # Calculate distance to target
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 5:  # Only move if we're not very close to target
                # Normalize direction vector and apply speed
                dx = dx / distance * self.player_speed * delta_time
                dy = dy / distance * self.player_speed * delta_time
                
                # Update position
                self.player_pos[0] += dx
                self.player_pos[1] += dy
            else:
                # We've reached the target
                self.player_pos = list(self.target_pos)
                self.target_pos = None
            
        # Keep player on screen
        self.player_pos[0] = max(20, min(self.player_pos[0], 780))
        self.player_pos[1] = max(20, min(self.player_pos[1], 580))
        
        # Update game tick system
        self.tick_timer += delta_time
        if self.tick_timer >= self.tick_rate:
            self.game_ticks += 1
            self.tick_timer -= self.tick_rate
            # Process tick-based game logic here
            print(f"Game tick: {self.game_ticks}")
    
    def draw(self, screen):
        # Draw game world
        screen.fill((0, 80, 0))  # Green background for grass
        
        # Draw target position indicator if we have one
        if self.target_pos:
            pygame.draw.circle(screen, (255, 255, 0), self.target_pos, 5, 1)
            # Draw line from player to target
            pygame.draw.line(screen, (255, 255, 0), 
                           (self.player_pos[0], self.player_pos[1]), 
                           (self.target_pos[0], self.target_pos[1]), 1)
        
        # Draw player as a red rectangle
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.player_pos[0] - 15, self.player_pos[1] - 15, 30, 30))
        
        # Draw UI elements
        tick_text = self.font.render(f"Ticks: {self.game_ticks}", True, (255, 255, 255))
        help_text = self.font.render("Click to move, use buttons for actions", True, (255, 255, 255))
        
        # Draw menu button
        pygame.draw.rect(screen, (100, 100, 200), self.menu_button)
        menu_text = self.font.render("Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        screen.blit(tick_text, (10, 10))
        screen.blit(help_text, (10, 570))

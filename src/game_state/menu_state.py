"""
Menu state for the game's main menu.
"""
import pygame
from .game_state import GameState

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
        """Handle menu events"""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Transition to play state on mouse click
                self.done = True
    
    def update(self, delta_time):
        """Update menu state"""
        # Pulse the start text color based on time
        pulse = (pygame.time.get_ticks() % 1000) / 1000.0
        brightness = 150 + int(105 * pulse)
        self.start_text = self.font.render("Click to Start", True, (brightness, brightness, brightness))
    
    def draw(self, screen):
        """Draw menu"""
        # Draw a dark background
        screen.fill((20, 20, 40))
        
        # Draw title and start text centered
        title_rect = self.title_text.get_rect(center=self.title_pos)
        start_rect = self.start_text.get_rect(center=self.start_pos)
        
        screen.blit(self.title_text, title_rect)
        screen.blit(self.start_text, start_rect)
    
    def resize(self, width, height):
        """Handle window resize"""
        # Update positions based on new screen size
        self.title_pos = (width // 2, height // 3)
        self.start_pos = (width // 2, height // 2)

import pygame
import os
from .button import Button

class CharacterSelect:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.characters = []
        self.buttons = []
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.load_characters()
        self.setup_ui()
    
    def load_characters(self):
        """Load saved characters"""
        self.characters = []
        if not os.path.exists(self.save_manager.save_directory):
            os.makedirs(self.save_manager.save_directory, exist_ok=True)
            return
            
        for filename in os.listdir(self.save_manager.save_directory):
            if filename.endswith(".json") and filename != "world.json":
                self.characters.append(filename[:-5])  # Remove .json
    
    def setup_ui(self):
        """Initialize UI elements"""
        screen_width, screen_height = pygame.display.get_surface().get_size()
        center_x = screen_width // 2
        
        # Create character buttons
        for i, char in enumerate(self.characters):
            btn = Button(
                x=center_x - 100,
                y=150 + i * 60,
                width=200,
                height=50,
                text=char,
                color=(70, 70, 200)
            )
            self.buttons.append((btn, char))
        
        # Add New Character button
        self.new_char_btn = Button(
            x=center_x - 100,
            y=screen_height - 100,
            width=200,
            height=50,
            text="New Character",
            color=(70, 200, 70)
        )
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check character buttons
            for btn, char in self.buttons:
                if btn.is_clicked(mouse_pos):
                    self.save_manager.character_name = char
                    self.save_manager.character_save_file = os.path.join(
                        self.save_manager.save_directory, f"{char}.json"
                    )
                    return "play"
            
            # Check new character button
            if self.new_char_btn.is_clicked(mouse_pos):
                return "new_character"
        
        return None
    
    def draw(self, screen):
        """Draw the character selection screen"""
        screen.fill((30, 30, 40))
        
        # Draw title
        title = self.font.render("Select Character", True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 50))
        
        # Draw character buttons
        for btn, _ in self.buttons:
            btn.draw(screen, self.small_font)
        
        # Draw new character button
        self.new_char_btn.draw(screen, self.small_font)
        
        # Draw help text
        help_text = self.small_font.render("Click a character to play or create a new one", True, (150, 150, 150))
        screen.blit(help_text, (screen.get_width()//2 - help_text.get_width()//2, screen.get_height() - 30))

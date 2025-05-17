import os
import json
import pygame
from .button import Button

class NewCharacter:
    def __init__(self, save_manager):
        self.save_manager = save_manager
        self.name = ""
        self.input_active = True
        self.error_message = ""
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.error_font = pygame.font.Font(None, 24)
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize UI elements"""
        screen_width, screen_height = pygame.display.get_surface().get_size()
        center_x = screen_width // 2
        
        # Input field dimensions
        self.input_width = 300
        self.input_height = 40
        self.input_rect = pygame.Rect(
            center_x - self.input_width // 2,
            150,
            self.input_width,
            self.input_height
        )
        
        # Calculate positions based on input field
        button_width = 140
        button_height = 40
        button_padding = 10
        
        # Position buttons relative to the input field
        buttons_y = self.input_rect.bottom + 40
        
        self.create_btn = Button(
            x=center_x - button_width - button_padding // 2,
            y=buttons_y,
            width=button_width,
            height=button_height,
            text="Create",
            color=(50, 200, 50)
        )
        
        self.cancel_btn = Button(
            x=center_x + button_padding // 2,
            y=buttons_y,
            width=button_width,
            height=button_height,
            text="Cancel",
            color=(200, 50, 50)
        )
    
    def create_character(self):
        """Create new character and save to file"""
        if not self.name.strip():
            self.error_message = "Please enter a name"
            return None
        
        save_path = os.path.join(self.save_manager.save_directory, f"{self.name}.json")
        if os.path.exists(save_path):
            self.error_message = f"Character '{self.name}' already exists"
            return None
        
        char_data = {
            'name': self.name,
            'grid_position': [0, 0],
            'inventory': [],
            'stats': {'health': 100, 'attack': 10, 'defense': 5}
        }
        
        try:
            with open(save_path, 'w') as f:
                json.dump(char_data, f, indent=4)
            
            self.save_manager.character_name = self.name
            self.save_manager.character_save_file = save_path
            self.error_message = ""  # Clear any previous error
            return "play"
        except IOError as e:
            self.error_message = f"Error saving character: {str(e)}"
            return None
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if clicking on input field
            if self.input_rect.collidepoint(mouse_pos):
                self.input_active = True
            else:
                self.input_active = False
            
            # Check buttons
            if self.create_btn.is_clicked(mouse_pos) and self.name.strip():
                return self.create_character()
            
            if self.cancel_btn.is_clicked(mouse_pos):
                return "character_select"
        
        # Handle keyboard input
        if self.input_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name.strip():
                return self.create_character()
            elif event.key == pygame.K_ESCAPE:
                return "character_select"
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.unicode.isprintable() and len(self.name) < 20:
                self.name += event.unicode
        
        return None
    
    def draw(self, screen):
        """Draw the new character screen"""
        screen.fill((30, 30, 40))
        
        # Draw title
        title = self.font.render("Create New Character", True, (255, 255, 255))
        title_y = 30
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, title_y))
        
        # Draw error message if it exists (above input field)
        if self.error_message:
            error_surface = self.error_font.render(self.error_message, True, (255, 100, 100))
            error_y = title_y + title.get_height() + 20
            screen.blit(error_surface, (screen.get_width()//2 - error_surface.get_width()//2, error_y))
        
        # Draw input field background (positioned below error message or title)
        input_y = (error_y + error_surface.get_height() + 20) if self.error_message else (title_y + title.get_height() + 40)
        self.input_rect.y = input_y
        pygame.draw.rect(screen, (50, 50, 60), self.input_rect, 0, 5)
        pygame.draw.rect(screen, (100, 100, 120), self.input_rect, 2, 5)
        
        # Draw input text with padding
        padding = 15  # Horizontal padding
        
        # Create text surface
        text_surface = self.font.render(
            self.name, True, (255, 255, 255)
        )
        
        # Calculate text position - center vertically in the input field
        text_y = self.input_rect.centery - text_surface.get_height() // 2
        text_x = self.input_rect.x + padding
        
        # Draw the text
        screen.blit(text_surface, (text_x, text_y))
        
        # Draw cursor if active
        if self.input_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = text_x + text_surface.get_width() + 2
            cursor_height = text_surface.get_height()
            cursor_rect = pygame.Rect(
                cursor_x,
                text_y,
                2,
                cursor_height
            )
            pygame.draw.rect(screen, (255, 255, 255), cursor_rect)
        
        # Draw instruction text 10px below input field
        instruction_text = f"Enter a name ({len(self.name)}/20 characters)"
        instruction_surface = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_y = self.input_rect.bottom + 10
        screen.blit(instruction_surface, (screen.get_width()//2 - instruction_surface.get_width()//2, instruction_y))

        # Draw buttons
        self.create_btn.draw(screen, self.small_font)
        self.cancel_btn.draw(screen, self.small_font)
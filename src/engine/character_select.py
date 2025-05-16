import pygame
import os
import json
from datetime import datetime
from src.engine.game_state import GameState
from src.engine.logger import game_logger

class CharacterSelectState(GameState):
    """Character selection screen where players can choose or create characters"""
    
    def __init__(self, asset_manager, save_manager):
        super().__init__()
        self.next_state = "play"
        self.asset_manager = asset_manager
        self.save_manager = save_manager
        
        # UI elements
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)
        
        # Character list
        self.characters = []
        self.selected_character = None
        
        # Button rectangles
        self.character_buttons = []
        self.create_button = pygame.Rect(250, 400, 300, 40)
        
        # Button styling
        self.button_color = (100, 100, 255)  # Blue color for all buttons
        self.button_radius = 10  # Rounded corners radius
        
        # Character creation
        self.creating_character = False
        self.new_character_name = ""
        self.input_rect = pygame.Rect(300, 400, 200, 32)
        
        # Load characters
        self.load_characters()
    
    def enter_state(self):
        """Called when state becomes active"""
        game_logger.info("Entering character selection screen")
        
        # Reset state
        self.creating_character = False
        self.new_character_name = ""
        
        # Reload characters
        self.load_characters()
        
        # Reset selection
        self.selected_character = None
        
        # If Harry exists, select him by default
        for character in self.characters:
            if character['name'].lower() == 'harry':
                self.selected_character = character
                self.save_manager.character_name = character['name']
                self.save_manager.character_save_file = os.path.join(
                    self.save_manager.save_directory, 
                    f"{character['name']}.json"
                )
                game_logger.info(f"Auto-selected character: {character['name']}")
                break
    
    def load_characters(self):
        """Load all available character save files"""
        self.characters = []
        game_logger.info(f"Loading characters from {self.save_manager.save_directory}")
        
        # Create save directory if it doesn't exist
        if not os.path.exists(self.save_manager.save_directory):
            game_logger.info("Creating save directory")
            os.makedirs(self.save_manager.save_directory, exist_ok=True)
        
        # Find all character save files
        for filename in os.listdir(self.save_manager.save_directory):
            if filename.endswith(".json") and filename != "world.json":
                character_name = filename.split(".")[0]
                save_path = os.path.join(self.save_manager.save_directory, filename)
                
                try:
                    with open(save_path, 'r') as file:
                        save_data = json.load(file)
                        self.characters.append({
                            'name': character_name,
                            'grid_position': save_data.get('grid_position', (0, 0))
                        })
                except (json.JSONDecodeError, IOError) as e:
                    game_logger.error(f"Error reading character file {filename}: {e}")
        
        # Sort alphabetically
        self.characters.sort(key=lambda x: x['name'].lower())
        game_logger.info(f"Found {len(self.characters)} characters: {[c['name'] for c in self.characters]}")
        
        # Update character buttons
        self.update_character_buttons()
    
    def update_character_buttons(self):
        """Update character button positions based on available characters"""
        self.character_buttons = []
        y_pos = 150
        
        for character in self.characters:
            button_rect = pygame.Rect(300, y_pos, 200, 40)
            self.character_buttons.append({
                'rect': button_rect,
                'character': character
            })
            y_pos += 50
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle character creation input field
                if self.creating_character:
                    if self.input_rect.collidepoint(event.pos):
                        # Clicked on input field
                        pass
                    elif self.create_button.collidepoint(event.pos):
                        # Create character with current name
                        self.create_character()
                    else:
                        # Cancel character creation
                        self.creating_character = False
                    continue
                
                # Handle character selection
                for button in self.character_buttons:
                    if button['rect'].collidepoint(event.pos):
                        self.selected_character = button['character']
                        self.save_manager.character_name = button['character']['name']
                        self.save_manager.character_save_file = os.path.join(
                            self.save_manager.save_directory, 
                            f"{button['character']['name']}.json"
                        )
                        game_logger.info(f"Selected character: {button['character']['name']}")
                        
                        # Immediately start the game with this character
                        from src.engine.game_state import GameStateManager
                        play_state = GameStateManager.instance().get_state("play")
                        if play_state:
                            play_state.save_manager = self.save_manager
                            game_logger.info(f"Starting game with character: {self.save_manager.character_name}")
                            self.done = True
                        break
                
                # Handle create new character button
                if self.create_button.collidepoint(event.pos):
                    self.creating_character = True
                    self.new_character_name = ""
                    game_logger.info("Creating new character")
                
                # No play button anymore - character selection immediately starts the game
            
            # Handle keyboard input for character creation
            elif event.type == pygame.KEYDOWN and self.creating_character:
                if event.key == pygame.K_RETURN:
                    self.create_character()
                elif event.key == pygame.K_BACKSPACE:
                    self.new_character_name = self.new_character_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.creating_character = False
                else:
                    # Limit name length
                    if len(self.new_character_name) < 15:
                        self.new_character_name += event.unicode
    
    def create_character(self):
        """Create a new character with the entered name"""
        if not self.new_character_name:
            return
        
        # Validate name (no special characters)
        valid_name = ''.join(c for c in self.new_character_name if c.isalnum() or c.isspace())
        if not valid_name:
            return
        
        # Create character save file
        self.save_manager.character_name = valid_name
        self.save_manager.character_save_file = os.path.join(
            self.save_manager.save_directory, 
            f"{valid_name}.json"
        )
        
        # Create initial character data
        timestamp = int(datetime.now().timestamp())
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        character_data = {
            'character_name': valid_name,
            'grid_position': [10, 10],
            'timestamp': timestamp,
            'formatted_time': formatted_time,
            'version': '1.0.0'
        }
        
        # Save character file
        try:
            with open(self.save_manager.character_save_file, 'w') as file:
                json.dump(character_data, file, indent=2)
            game_logger.info(f"Created new character: {valid_name}")
            
            # Reload characters and select the new one
            self.load_characters()
            for character in self.characters:
                if character['name'] == valid_name:
                    self.selected_character = character
                    
                    # Immediately start the game with the new character
                    from src.engine.game_state import GameStateManager
                    play_state = GameStateManager.instance().get_state("play")
                    if play_state:
                        play_state.save_manager = self.save_manager
                        game_logger.info(f"Starting game with new character: {self.save_manager.character_name}")
                        self.done = True
                    break
        except IOError as e:
            game_logger.error(f"Error creating character file: {e}")
        
        # Exit creation mode
        self.creating_character = False
    
    def update(self, delta_time):
        # Nothing to update
        pass
    
    def draw_rounded_rect(self, surface, rect, color, radius=10):
        """Draw a rounded rectangle without any border lines"""
        rect = pygame.Rect(rect)
        
        # Draw the main rectangle without corners
        pygame.draw.rect(surface, color, (rect.x + radius, rect.y, rect.width - 2 * radius, rect.height))
        pygame.draw.rect(surface, color, (rect.x, rect.y + radius, rect.width, rect.height - 2 * radius))
        
        # Draw the four corner circles
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + radius, rect.bottom - radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)
    
    def draw(self, screen):
        # Draw background
        screen.fill((30, 30, 50))
        
        # Draw title
        title = self.title_font.render("Character Selection", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title, title_rect)
        
        # Draw character buttons
        for button in self.character_buttons:
            # All character buttons have blue background
            # Slightly brighter blue for selected character
            color = (120, 120, 255) if (
                self.selected_character and 
                button['character']['name'] == self.selected_character['name']
            ) else self.button_color
            
            # Draw rounded rectangle button
            self.draw_rounded_rect(screen, button['rect'], color, self.button_radius)
            
            # Draw character name
            name_text = self.button_font.render(button['character']['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=button['rect'].center)
            screen.blit(name_text, name_rect)
        
        # Draw create new character button
        if not self.creating_character:
            # Use the same blue color and rounded corners
            self.draw_rounded_rect(screen, self.create_button, self.button_color, self.button_radius)
            create_text = self.button_font.render("Create New Character", True, (255, 255, 255))
            create_rect = create_text.get_rect(center=self.create_button.center)
            screen.blit(create_text, create_rect)
        
        # No play button or character info display
        
        # Draw character creation UI
        if self.creating_character:
            # Draw input field background with rounded corners
            self.draw_rounded_rect(screen, self.input_rect, (50, 50, 50), self.button_radius)
            
            # Draw input text
            input_text = self.button_font.render(self.new_character_name, True, (255, 255, 255))
            screen.blit(input_text, (self.input_rect.x + 10, self.input_rect.y + 5))
            
            # Draw prompt
            prompt = self.info_font.render("Enter character name:", True, (200, 200, 200))
            screen.blit(prompt, (self.input_rect.x, self.input_rect.y - 30))
            
            # Draw create button with same blue color and rounded corners
            self.draw_rounded_rect(screen, self.create_button, self.button_color, self.button_radius, 2, (200, 200, 200))
            create_text = self.button_font.render("Create Character", True, (255, 255, 255))
            create_rect = create_text.get_rect(center=self.create_button.center)
            screen.blit(create_text, create_rect)

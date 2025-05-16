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
        
        game_logger.info("CharacterSelectState initialized")
        
        # UI elements
        self.title_font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)
        
        # Character list
        self.characters = []
        self.selected_character = None
        self.load_characters()
        
        # Buttons
        self.buttons = []
        self.create_new_button = None
        self.play_button = None
        self.create_character_input = False
        self.new_character_name = ""
        self.input_active = False
        self.input_rect = pygame.Rect(300, 400, 200, 32)
        
        # Initialize UI
        self.init_ui()
    
    def load_characters(self):
        """Load all available character save files"""
        self.characters = []
        game_logger.info(f"Loading characters from {self.save_manager.save_directory}")
        
        # Check saves directory
        if not os.path.exists(self.save_manager.save_directory):
            game_logger.info("Saves directory does not exist, creating it")
            os.makedirs(self.save_manager.save_directory, exist_ok=True)
        
        # Look for character save files
        for filename in os.listdir(self.save_manager.save_directory):
            if filename.endswith(".json") and filename != "world.json":
                character_name = filename.split(".")[0]  # Remove .json extension
                save_path = os.path.join(self.save_manager.save_directory, filename)
                
                try:
                    with open(save_path, 'r') as file:
                        save_data = json.load(file)
                        # Extract character info
                        self.characters.append({
                            'name': character_name,
                            'filename': filename,
                            'position': save_data.get('grid_position', (0, 0)),
                            'timestamp': save_data.get('timestamp', 0),
                            'formatted_time': save_data.get('formatted_time', 'Unknown')
                        })
                except (json.JSONDecodeError, IOError) as e:
                    game_logger.error(f"Error reading character file {filename}: {e}")
        
        # Sort by most recently played
        self.characters.sort(key=lambda x: x['timestamp'], reverse=True)
        game_logger.info(f"Found {len(self.characters)} characters: {[c['name'] for c in self.characters]}")
        
        # If Harry exists, put him first
        for i, character in enumerate(self.characters):
            if character['name'].lower() == 'harry':
                if i > 0:  # If not already first
                    self.characters.pop(i)
                    self.characters.insert(0, character)
                break
    
    def enter_state(self):
        """Called when state becomes active"""
        game_logger.info("Entering CharacterSelectState")
        
        # Reload characters in case new ones were added
        self.load_characters()
        self.init_ui()
        
        # Reset selection
        self.selected_character = None
        
        # Find the play button and disable it initially
        for button in self.buttons:
            if button.get('action') == 'play':
                self.play_button = button
                button['enabled'] = False
                break
        
        # If Harry exists, select him by default
        for character in self.characters:
            if character['name'].lower() == 'harry':
                self.selected_character = character
                self.save_manager.character_name = character['name']
                self.save_manager.character_save_file = os.path.join(
                    self.save_manager.save_directory, 
                    f"{character['name']}.json"
                )
                if self.play_button:
                    self.play_button['enabled'] = True
                game_logger.info(f"Auto-selected character: {character['name']}")
                break
    
    def init_ui(self):
        """Initialize UI elements"""
        self.buttons = []
        
        # Character buttons - positioned dynamically based on number of characters
        y_pos = 150
        for character in self.characters:
            button_rect = pygame.Rect(300, y_pos, 200, 40)
            self.buttons.append({
                'rect': button_rect,
                'text': character['name'],
                'action': 'select_character',
                'character': character
            })
            y_pos += 50
        
        # Create new character button
        self.create_new_button = {
            'rect': pygame.Rect(300, y_pos, 200, 40),
            'text': "Create New Character",
            'action': 'create_new'
        }
        self.buttons.append(self.create_new_button)
        
        # Play button (initially disabled)
        self.play_button = {
            'rect': pygame.Rect(300, 500, 200, 50),
            'text': "Play",
            'action': 'play',
            'enabled': False
        }
        self.buttons.append(self.play_button)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button was clicked
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['action'] == 'select_character' and 'character' in button:
                            self.selected_character = button['character']
                            self.save_manager.character_name = button['character']['name']
                            self.save_manager.character_save_file = os.path.join(
                                self.save_manager.save_directory, 
                                f"{button['character']['name']}.json"
                            )
                            self.play_button['enabled'] = True
                            game_logger.info(f"Selected character: {button['character']['name']}")
                        
                        elif button['action'] == 'create_new':
                            self.create_character_input = True
                            self.input_active = True
                            game_logger.info("Creating new character")
                        
                        elif button['action'] == 'play' and button.get('enabled', False):
                            # Get the PlayState and set its save_manager before transitioning
                            from src.engine.game_state import GameStateManager
                            play_state = GameStateManager.instance().get_state("play")
                            if play_state:
                                play_state.save_manager = self.save_manager
                                game_logger.info(f"Passing save manager to PlayState for character: {self.save_manager.character_name}")
                            self.done = True
                            game_logger.info(f"Starting game with character: {self.save_manager.character_name}")
                
                # Check if input field was clicked
                if self.create_character_input:
                    if self.input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
            
            elif event.type == pygame.KEYDOWN and self.create_character_input and self.input_active:
                if event.key == pygame.K_RETURN:
                    # Create new character with entered name
                    if self.new_character_name:
                        self.save_manager.character_name = self.new_character_name
                        self.save_manager.character_save_file = os.path.join(
                            self.save_manager.save_directory, 
                            f"{self.new_character_name}.json"
                        )
                        
                        # Create empty character save
                        character_data = {
                            'character_name': self.new_character_name,
                            'grid_position': (10, 10),  # Default starting position
                            'timestamp': 0,
                            'formatted_time': '',
                            'version': '1.0.0'
                        }
                        
                        # Ensure save directory exists
                        os.makedirs(self.save_manager.save_directory, exist_ok=True)
                        
                        # Write initial character data
                        try:
                            with open(self.save_manager.character_save_file, 'w') as file:
                                json.dump(character_data, file, indent=2)
                            game_logger.info(f"Created new character: {self.new_character_name}")
                        except IOError as e:
                            game_logger.error(f"Error creating character file: {e}")
                        
                        # Reload characters and UI
                        self.load_characters()
                        self.init_ui()
                        
                        # Select the new character
                        for character in self.characters:
                            if character['name'] == self.new_character_name:
                                self.selected_character = character
                                break
                        
                        self.play_button['enabled'] = True
                        self.create_character_input = False
                        self.new_character_name = ""
                
                elif event.key == pygame.K_BACKSPACE:
                    self.new_character_name = self.new_character_name[:-1]
                else:
                    # Limit name length
                    if len(self.new_character_name) < 15:
                        self.new_character_name += event.unicode
    
    def update(self, delta_time):
        # Nothing to update in this state
        pass
    
    def draw(self, screen):
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw title
        title = self.title_font.render("Character Selection", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title, title_rect)
        
        # Draw character buttons
        for button in self.buttons:
            # Skip play button if disabled
            if button.get('action') == 'play' and not button.get('enabled', True):
                continue
                
            # Highlight selected character
            color = (100, 100, 255) if (
                button.get('action') == 'select_character' and 
                self.selected_character and 
                button.get('character', {}).get('name') == self.selected_character.get('name')
            ) else (100, 100, 100)
            
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, (200, 200, 200), button['rect'], 2)
            
            text = self.button_font.render(button['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)
        
        # Draw character info if selected
        if self.selected_character:
            info_text = f"Last played: {self.selected_character.get('formatted_time', 'Unknown')}"
            info = self.info_font.render(info_text, True, (200, 200, 200))
            screen.blit(info, (300, 450))
        
        # Draw character creation input field
        if self.create_character_input:
            pygame.draw.rect(screen, (50, 50, 50), self.input_rect)
            pygame.draw.rect(screen, (255, 255, 255) if self.input_active else (100, 100, 100), self.input_rect, 2)
            
            # Draw input text
            input_text = self.button_font.render(self.new_character_name, True, (255, 255, 255))
            screen.blit(input_text, (self.input_rect.x + 5, self.input_rect.y + 5))
            
            # Draw prompt
            prompt = self.info_font.render("Enter character name:", True, (200, 200, 200))
            screen.blit(prompt, (300, 370))

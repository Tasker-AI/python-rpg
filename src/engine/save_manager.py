import os
import json
import time
from datetime import datetime
from src.engine.logger import game_logger

class SaveManager:
    """
    Manages saving and loading game state.
    Automatically saves game progress and allows loading from save files.
    """
    def __init__(self, character_name=None):
        """
        Initialize the save manager.
        
        Args:
            character_name: Optional character name. If not provided, no save files will be checked.
        """
        # Ensure save directory path is absolute
        self.save_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saves"))
        
        # Set character name if provided
        self.character_name = character_name
        
        # Set up the save file paths
        self.character_save_file = None
        self.world_save_file = os.path.join(self.save_directory, "world.json")
        
        if self.character_name:
            self.character_save_file = os.path.join(self.save_directory, f"{self.character_name}.json")
        
        self.auto_save_interval = 1  # Save every game tick
        self.last_save_tick = 0
        
        # Ensure save directory exists
        os.makedirs(self.save_directory, exist_ok=True)
        game_logger.info(f"Save manager initialized. Save directory: {self.save_directory}")
    
    def get_save_files(self):
        """Get the character and world save files if they exist"""
        save_files = []
        
        if not os.path.exists(self.save_directory):
            return save_files
        
        # Check for the character's save file
        if os.path.exists(self.character_save_file):
            try:
                with open(self.character_save_file, 'r') as file:
                    save_data = json.load(file)
                    # Extract metadata for display
                    save_files.append({
                        'filename': f"{self.character_name}.json",
                        'player_name': self.character_name,
                        'timestamp': save_data.get('timestamp', 0),
                        'formatted_time': datetime.fromtimestamp(save_data.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                        'position': save_data.get('grid_position', (0, 0)),
                        'type': 'character'
                    })
            except (json.JSONDecodeError, IOError) as e:
                game_logger.error(f"Error reading save file {self.character_name}.json: {e}")
        
        # Check for world save file
        if os.path.exists(self.world_save_file):
            try:
                with open(self.world_save_file, 'r') as file:
                    world_data = json.load(file)
                    # Extract metadata for display
                    save_files.append({
                        'filename': "world.json",
                        'timestamp': world_data.get('timestamp', 0),
                        'formatted_time': datetime.fromtimestamp(world_data.get('timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                        'game_ticks': world_data.get('game_ticks', 0),
                        'type': 'world'
                    })
            except (json.JSONDecodeError, IOError) as e:
                game_logger.error(f"Error reading world save file: {e}")
        
        return save_files
    
    def create_character_save(self):
        """Create or ensure the character's save file exists"""
        # Always use the character name
        game_logger.info(f"Using save file for character: {self.character_name}")
        return self.character_save_file
    
    def create_world_save(self):
        """Create or ensure the world save file exists"""
        game_logger.info("Using world save file")
        return self.world_save_file
    
    def load_character_save(self):
        """Load the character's save file"""
        if not os.path.exists(self.character_save_file):
            game_logger.error(f"Save file not found for character: {self.character_name}")
            return None
            
        try:
            with open(self.character_save_file, 'r') as file:
                save_data = json.load(file)
                game_logger.info(f"Loaded save file for character: {self.character_name}")
                return save_data
        except (json.JSONDecodeError, IOError) as e:
            game_logger.error(f"Error loading save file for {self.character_name}: {e}")
            return None
    
    def load_world_save(self):
        """Load the world save file"""
        if not os.path.exists(self.world_save_file):
            game_logger.error("World save file not found")
            return None
            
        try:
            with open(self.world_save_file, 'r') as file:
                world_data = json.load(file)
                game_logger.info("Loaded world save file")
                return world_data
        except (json.JSONDecodeError, IOError) as e:
            game_logger.error(f"Error loading world save file: {e}")
            return None
    
    def save_game_state(self, character_state, world_state, current_tick):
        """
        Save the character and world state to separate files.
        
        Args:
            character_state: Dictionary containing character-specific data
            world_state: Dictionary containing world data (tilemap, game ticks)
            current_tick: Current game tick
        """
        # Save on every tick as specified in the game design
        self.last_save_tick = current_tick
        
        # Ensure save directory exists
        os.makedirs(self.save_directory, exist_ok=True)
        
        # Save character state
        try:
            with open(self.character_save_file, 'w') as file:
                json.dump(character_state, file, indent=2)
                
                # Only log at DEBUG level to reduce console spam
                game_logger.debug(f"Character state saved for {self.character_name}")
        except IOError as e:
            game_logger.error(f"Error saving character state: {e}")
            return False
        
        # Save world state
        try:
            with open(self.world_save_file, 'w') as file:
                json.dump(world_state, file, indent=2)
                
                # Only log at DEBUG level to reduce console spam
                game_logger.debug("World state saved")
        except IOError as e:
            game_logger.error(f"Error saving world state: {e}")
            return False
            
        return True
    
    # No longer need the cleanup method since we're only using one save file per character
    def _cleanup_old_saves(self, max_saves=1):
        """No longer needed as we're using a single save file per character"""
        pass

    
    def collect_game_states(self, player, tilemap, game_ticks):
        """
        Collect character and world state data into separate dictionaries.
        
        Args:
            player: Player object
            tilemap: Tilemap object
            game_ticks: Current game tick count
            
        Returns:
            Tuple of (character_state, world_state) dictionaries
        """
        timestamp = int(time.time())
        
        # Collect character data (only grid position as requested)
        character_state = {
            'timestamp': timestamp,
            'formatted_time': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'character_name': self.character_name,
            'grid_position': (player.grid_x, player.grid_y),
            # Add more character attributes as they are implemented
            # 'health': player.health,
            # 'inventory': player.inventory,
            # 'stats': player.stats,
            'version': '1.0.0'  # Game version for compatibility checking
        }
        
        # Collect world data (tilemap and game ticks)
        world_state = {
            'timestamp': timestamp,
            'formatted_time': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'game_ticks': game_ticks,
            'tilemap': {
                'width': tilemap.width,
                'height': tilemap.height,
                # Store only modified tiles to keep save files smaller
                'modified_tiles': []
            },
            'version': '1.0.0'  # Game version for compatibility checking
        }
        
        # In the future, we would collect modified tiles here
        # For now, we'll just store the dimensions
        
        return character_state, world_state
    
    def delete_save_file(self, filename):
        """Delete a save file by filename"""
        save_path = os.path.join(self.save_directory, filename)
        
        if not os.path.exists(save_path):
            game_logger.error(f"Save file not found: {filename}")
            return False
            
        try:
            os.remove(save_path)
            game_logger.info(f"Deleted save file: {filename}")
            
            # Reset current save file if it was the one deleted
            if self.current_save_file == save_path:
                self.current_save_file = None
                
            return True
        except IOError as e:
            game_logger.error(f"Error deleting save file {filename}: {e}")
            return False

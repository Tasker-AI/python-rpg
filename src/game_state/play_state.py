"""
Play state for the main game.
"""
import pygame
from .game_state import GameState
from .player_state import PlayerState
from .world_state import WorldState
from src.engine.asset_manager import AssetManager
from src.engine.save_manager import SaveManager
from src.engine.logger import game_logger

class PlayState(GameState):
    """Main gameplay state."""
    
    def __init__(self, asset_manager, save_manager, map_file='assets/maps/generated_map.json'):
        """
        Initialize play state.
        
        Args:
            asset_manager: The asset manager for loading game assets
            save_manager: The save manager for handling game saves
            map_file: Path to the map JSON file to load
        """
        super().__init__()
        self.asset_manager = asset_manager
        self.save_manager = save_manager
        
        # Initialize world state
        self.world = WorldState(map_file=map_file)
        self.world.set_asset_manager(asset_manager)
        
        # Initialize player state
        self.player_state = None
        self.player_initialized = False
        
        # Camera position
        self.camera_x = 0
        self.camera_y = 0
        
        # UI state
        self.show_inventory = False
        
        # Debug info
        self.debug_font = pygame.font.Font(None, 24)
        self.show_debug = False
    
    def enter_state(self, character_name=None):
        """
        Called when state becomes active.
        
        Args:
            character_name: Optional name of the character to load. If None, a new character will be created.
        """
        game_logger.info("Game state entering: PlayState")
        
        # Set up the world
        self.world.setup_world()
        
        # Initialize player state with the selected character
        if not self.player_initialized:
            self.player_state = PlayerState(
                self.asset_manager, 
                self.save_manager,
                world_state=self.world
            )
            
            if character_name and self.save_manager.character_name != character_name:
                self.save_manager.character_name = character_name
                self.save_manager.character_save_file = os.path.join(
                    self.save_manager.save_directory, 
                    f"{character_name}.json"
                )
            
            # Try to load player state if a character name is provided, otherwise create new
            if character_name and self.player_state.load_player():
                game_logger.info(f"Loaded existing character: {character_name}")
            else:
                self.player_state.create_player()
                if character_name:
                    game_logger.info(f"Created new character: {character_name}")
                else:
                    game_logger.info("Created new character")
            
            self.player_initialized = True
    
    def handle_events(self, events):
        """Handle game events."""
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
                
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                # Toggle debug info
                if event.key == pygame.K_F3:
                    self.show_debug = not self.show_debug
                # Toggle inventory
                elif event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory
                # Quick save
                elif event.key == pygame.K_F5:
                    self.save_game()
                # Quick load
                elif event.key == pygame.K_F9:
                    self.load_game()
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if not self.show_inventory and hasattr(self, 'world') and hasattr(self, 'player_state'):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    tile_size = self.world.tile_size if hasattr(self.world, 'tile_size') else 32
                    
                    # Calculate grid coordinates from screen coordinates
                    world_x = mouse_x + self.camera_x
                    world_y = mouse_y + self.camera_y
                    tile_x = int(world_x // tile_size)
                    tile_y = int(world_y // tile_size)
                    
                    game_logger.info(f"MOUSE_CLICK: Screen: ({mouse_x}, {mouse_y}), "
                                   f"World: ({world_x:.1f}, {world_y:.1f}), "
                                   f"Grid: ({tile_x}, {tile_y})")
                    
                    if hasattr(self.player_state, 'handle_click'):
                        game_logger.debug(f"Forwarding click to player_state.handle_click({tile_x}, {tile_y})")
                        self.player_state.handle_click(tile_x, tile_y)
                    else:
                        game_logger.warning("player_state has no handle_click method")
    
    def update(self, delta_time):
        """Update game state."""
        current_time = pygame.time.get_ticks()  # Keep time in milliseconds for consistency
        
        # Update world and player
        self.world.update(current_time)
        
        # Update player with the current time for movement interpolation
        if hasattr(self, 'player_state') and self.player_state:
            self.player_state.update(current_time)
        
        # Update camera to follow player if player exists
        if hasattr(self, 'player_state') and self.player_state and self.player_state.player:
            self._update_camera()
    
    def _update_camera(self):
        """Update camera to follow player."""
        if not hasattr(self, 'player_state') or not self.player_state.player:
            return
            
        try:
            # Get player position in pixels
            player = self.player_state.player
            screen = pygame.display.get_surface()
            if not screen:
                return
                
            screen_width, screen_height = screen.get_size()
            
            # Ensure player position is valid
            if not hasattr(player, 'x') or not hasattr(player, 'y'):
                return
            
            # Calculate target camera position to center on player
            target_cam_x = int(player.x - screen_width // 2)
            target_cam_y = int(player.y - screen_height // 2)
            
            # Keep camera in bounds
            if hasattr(self.world, 'width') and hasattr(self.world, 'height') and hasattr(self.world, 'tile_size'):
                map_width = self.world.width * self.world.tile_size
                map_height = self.world.height * self.world.tile_size
                
                # Ensure camera stays within map bounds
                target_cam_x = max(0, min(target_cam_x, max(0, map_width - screen_width)))
                target_cam_y = max(0, min(target_cam_y, max(0, map_height - screen_height)))
            
            # If camera hasn't been initialized yet, set it directly to the target
            if not hasattr(self, 'camera_x') or not hasattr(self, 'camera_y'):
                self.camera_x = target_cam_x
                self.camera_y = target_cam_y
            else:
                # Smooth camera movement (lerp)
                # Use a consistent interpolation factor for both axes
                lerp_factor = 0.2  # Slightly faster than before for better responsiveness
                self.camera_x = int(self.camera_x + (target_cam_x - self.camera_x) * lerp_factor)
                self.camera_y = int(self.camera_y + (target_cam_y - self.camera_y) * lerp_factor)
                
        except Exception as e:
            # Reset camera to safe position on error
            self.camera_x, self.camera_y = 0, 0
    
    def draw(self, screen):
        """Draw the game state."""
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the world
        if hasattr(self, 'world'):
            self.world.draw(screen, self.camera_x, self.camera_y)
            
        # Draw the player if it exists
        if hasattr(self, 'player_state') and hasattr(self.player_state, 'player') and self.player_state.player:
            try:
                # Draw the player through the player state
                self.player_state.draw(screen, self.camera_x, self.camera_y)
                
                # Draw player debug info if enabled
                if hasattr(self, 'show_debug') and self.show_debug:
                    self._draw_debug_info(screen)
                    
                # Player is loaded, no need to show loading message
            except Exception as e:
                game_logger.error(f"Error drawing player: {e}")
        
        # Draw UI elements
        if hasattr(self, 'show_inventory') and self.show_inventory:
            self._draw_inventory(screen)
            
        # Draw debug info if enabled
        if hasattr(self, 'show_debug') and self.show_debug:
            self._draw_debug_info(screen)
    
    def _draw_inventory(self, screen):
        """Draw the inventory UI."""
        # Create a semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 180 alpha
        screen.blit(overlay, (0, 0))
        
        # Draw inventory window
        inventory_rect = pygame.Rect(200, 100, 400, 400)
        pygame.draw.rect(screen, (50, 50, 60), inventory_rect)
        pygame.draw.rect(screen, (100, 100, 120), inventory_rect, 2)
        
        # Draw inventory title
        title = self.debug_font.render("INVENTORY", True, (255, 255, 255))
        screen.blit(title, (inventory_rect.centerx - title.get_width() // 2, inventory_rect.y + 20))
        
        # TODO: Draw actual inventory items
        # For now, just draw a placeholder
        placeholder = self.debug_font.render("Inventory system coming soon!", True, (200, 200, 200))
        screen.blit(placeholder, (inventory_rect.centerx - placeholder.get_width() // 2, 
                                 inventory_rect.centery - placeholder.get_height() // 2))
    
    def _draw_debug_info(self, screen):
        """Draw debug information."""
        if not self.player_state.player:
            return
            
        debug_lines = [
            f"FPS: {int(pygame.time.Clock().get_fps())}",
            f"Player: ({self.player_state.player.grid_x}, {self.player_state.player.grid_y})",
            f"Camera: ({int(self.camera_x)}, {int(self.camera_y)})",
            f"Game Ticks: {self.world.game_ticks}",
            "",
            "F3: Toggle Debug",
            "F5: Quick Save",
            "F9: Quick Load",
            "I: Toggle Inventory"
        ]
        
        for i, line in enumerate(debug_lines):
            text = self.debug_font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 25))
    
    def save_game(self):
        """Save the current game state."""
        if hasattr(self.save_manager, 'save_character'):
            self.save_manager.save_character(self.player_state.player)
            self.world.save_state(self.save_manager)
            game_logger.info("Game saved successfully")
    
    def load_game(self):
        """Load the saved game state."""
        self.player_state.load_player()
        self.world.load_state(self.save_manager)
        game_logger.info("Game loaded successfully")
    
    def exit_state(self):
        """Called when state becomes inactive."""
        # Save game when exiting
        self.save_game()
    
    def resize(self, width, height):
        """Handle window resize."""
        # Update camera when window is resized
        if self.player_state and self.player_state.player:
            self._update_camera()

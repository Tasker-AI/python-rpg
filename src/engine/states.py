import pygame
from src.engine.game_state import GameState
from src.engine.asset_manager import AssetManager
from src.game.tilemap import TileMap, TileType
from src.game.player import Player
from src.engine.logger import game_logger

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
    def __init__(self, asset_manager):
        super().__init__()
        self.next_state = "menu"
        
        # Game tick system
        self.tick_rate = 0.6  # seconds per tick
        self.tick_timer = 0
        self.game_ticks = 0
        
        # Player reference (will be created in enter_state)
        self.player = None
        
        # Font for UI elements
        self.font = pygame.font.SysFont(None, 24)
        
        # UI elements
        self.menu_button = pygame.Rect(700, 10, 80, 30)
        
        # Click indicators
        self.click_indicators = []  # List of (x, y, time_remaining) tuples
        
        # Camera smoothing
        self.target_camera_x = 0
        self.target_camera_y = 0
        self.camera_x = 0
        self.camera_y = 0
        self.camera_smoothing = 0.15  # Increased smoothing factor for camera movement
        
        # Asset manager
        self.asset_manager = asset_manager
        
        # Create tilemap (expanded to 250x200 tiles)
        self.map_width = 250
        self.map_height = 200
        self.tile_size = 32
        self.tilemap = TileMap(self.map_width, self.map_height, self.tile_size)
        self.tilemap.set_asset_manager(self.asset_manager)
        self.tilemap.create_test_map()  # Create a large test map with various terrain
        
        # Camera position (top-left corner of the view)
        self.target_camera_x = 0
        self.target_camera_y = 0
        self.camera_x = 0
        self.camera_y = 0
        
        # Player (starts at grid position 5,5)
        self.player = None  # Will be initialized in enter_state
        
        # UI elements
        self.menu_button = pygame.Rect(700, 550, 80, 30)
        
    def enter_state(self):
        """Called when state becomes active"""
        game_logger.log_game_state("PlayState", "entering")
        
        # Load assets
        self.asset_manager.load_image("player", "player.png")
        self.asset_manager.load_image("grass", "grass.png")
        self.asset_manager.load_image("water", "water.png")
        self.asset_manager.load_image("tree", "tree.png")
        self.asset_manager.load_image("rock", "rock.png")
        
        # Initialize player if not already created
        if self.player is None:
            # Start at position (10, 10) which should be on grass, with some landmarks nearby
            self.player = Player(10, 10, self.tilemap, self.asset_manager)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug key for testing movement
                if event.key == pygame.K_t:
                    # Test movement to a specific tile (15, 15)
                    test_tile_x, test_tile_y = 15, 15
                    game_logger.info(f"TEST: Moving player to tile ({test_tile_x}, {test_tile_y})")
                    
                    # Clear any existing movement
                    self.player.movement_queue.clear()
                    self.player.pending_movements.clear()
                    
                    # Queue the test movement
                    self.player.queue_movement(test_tile_x, test_tile_y)
                    
                    # Log the test for verification
                    game_logger.info(f"TEST QUEUED: Moving to ({test_tile_x}, {test_tile_y}) from ({self.player.grid_x}, {self.player.grid_y})")
                    
                elif event.key == pygame.K_1:
                    # Test movement to tile (20, 20)
                    test_tile_x, test_tile_y = 20, 20
                    game_logger.info(f"TEST 1: Moving player to tile ({test_tile_x}, {test_tile_y})")
                    self.player.queue_movement(test_tile_x, test_tile_y)
                    
                elif event.key == pygame.K_2:
                    # Test movement to tile (5, 5)
                    test_tile_x, test_tile_y = 5, 5
                    game_logger.info(f"TEST 2: Moving player to tile ({test_tile_x}, {test_tile_y})")
                    self.player.queue_movement(test_tile_x, test_tile_y)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Log mouse event
                game_logger.log_mouse_event("BUTTONDOWN", event.pos, event.button)
                
                # Check if menu button was clicked
                if self.menu_button.collidepoint(event.pos):
                    game_logger.info("Menu button clicked")
                    self.done = True  # Return to menu
                else:
                    # Convert screen coordinates to world coordinates
                    # Since player is always centered, the clicked position is relative to player
                    screen_width, screen_height = pygame.display.get_surface().get_size()
                    screen_center_x, screen_center_y = screen_width // 2, screen_height // 2
                    
                    # Calculate offset from center (player position)
                    offset_x = event.pos[0] - screen_center_x
                    offset_y = event.pos[1] - screen_center_y
                    
                    # Apply offset to player's world position
                    world_x = self.player.x + offset_x
                    world_y = self.player.y + offset_y
                    
                    # Log click coordinates
                    game_logger.debug(f"Click at screen pos: {event.pos}, screen center: ({screen_center_x}, {screen_center_y})")
                    game_logger.debug(f"Offset: ({offset_x}, {offset_y}), World pos: ({world_x}, {world_y})")
                    
                    # Convert to tile coordinates
                    # Use floor division to ensure we get the correct tile
                    tile_x = int(world_x // self.tile_size)
                    tile_y = int(world_y // self.tile_size)
                    game_logger.debug(f"Target tile: ({tile_x}, {tile_y})")
                    
                    # Calculate the center pixel coordinates of the target tile for verification
                    center_x, center_y = self.tilemap.grid_to_pixel(tile_x, tile_y)
                    game_logger.debug(f"Target tile center: ({center_x}, {center_y})")
                    
                    # Check if the target tile is valid
                    if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
                        tile_type = self.tilemap.get_tile(tile_x, tile_y).tile_type
                        game_logger.debug(f"Target tile type: {tile_type}, walkable: {self.tilemap.is_walkable(tile_x, tile_y)}")
                        
                        # Add click indicator that will display for 2 seconds
                        indicator_x = tile_x * self.tile_size
                        indicator_y = tile_y * self.tile_size
                        self.click_indicators.append((indicator_x, indicator_y, 2.0))
                        game_logger.debug(f"Added click indicator at tile ({tile_x}, {tile_y})")
                        
                        # Queue up the movement to be processed on next tick
                        player_tile_x = int(self.player.x // self.tile_size)
                        player_tile_y = int(self.player.y // self.tile_size)
                        game_logger.log_player_movement((player_tile_x, player_tile_y), (tile_x, tile_y))
                        
                        # Queue the movement without starting it immediately
                        self.player.queue_movement(tile_x, tile_y)
                    else:
                        game_logger.warning(f"Click outside map bounds: ({tile_x}, {tile_y})")
            
            elif event.type == pygame.MOUSEMOTION:
                # Log mouse motion events at debug level
                game_logger.log_mouse_event("MOTION", event.pos)
    
    def update(self, delta_time):
        # Update game tick system
        tick_occurred = False
        self.tick_timer += delta_time
        if self.tick_timer >= self.tick_rate:
            self.game_ticks += 1
            self.tick_timer -= self.tick_rate
            tick_occurred = True
            # Process tick-based game logic here
            game_logger.log_tick(self.game_ticks, delta_time)
            
            # Process player movement on tick
            if self.player:
                self.player.process_movement_queue()
                
            # Debug: Log player position after tick
            if self.player and not self.player.moving and len(self.player.movement_queue) == 0:
                game_logger.info(f"Player final position: Tile ({self.player.grid_x}, {self.player.grid_y}), Pixel ({self.player.x}, {self.player.y})")
        
        # Update player
        self.player.update(delta_time, tick_occurred)
        
        # Update click indicators (fade out over time)
        for i in range(len(self.click_indicators) - 1, -1, -1):
            x, y, time_remaining = self.click_indicators[i]
            time_remaining -= delta_time
            if time_remaining <= 0:
                self.click_indicators.pop(i)
            else:
                self.click_indicators[i] = (x, y, time_remaining)
        
        # Set target camera position to keep player centered
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.target_camera_x = self.player.x - screen_width // 2
        self.target_camera_y = self.player.y - screen_height // 2
        
        # Smoothly interpolate camera position
        # This prevents jumps when movement starts or stops
        # Use a more consistent interpolation factor for smoother movement
        camera_speed = self.camera_smoothing * 60 * delta_time  # Scale with frame rate
        
        # Increase smoothing when player is not moving to prevent jerky final movement
        if not self.player.moving and len(self.player.movement_queue) == 0:
            camera_speed = min(camera_speed, 0.05)  # Slower, more gradual camera movement at the end
            
        self.camera_x += (self.target_camera_x - self.camera_x) * camera_speed
        self.camera_y += (self.target_camera_y - self.camera_y) * camera_speed
        
        # Log camera position for debugging
        game_logger.debug(f"Camera position: ({self.camera_x}, {self.camera_y}), Target: ({self.target_camera_x}, {self.target_camera_y})")
        
        # Keep camera within map bounds (but only if map is smaller than screen)
        map_pixel_width = self.map_width * self.tile_size
        map_pixel_height = self.map_height * self.tile_size
        
        if map_pixel_width <= screen_width:
            self.camera_x = max(0, min(self.camera_x, map_pixel_width - screen_width))
        if map_pixel_height <= screen_height:
            self.camera_y = max(0, min(self.camera_y, map_pixel_height - screen_height))
    
    def draw(self, screen):
        # Draw game world
        self.tilemap.draw(screen, self.camera_x, self.camera_y)
        
        # Draw click indicators
        for x, y, time_remaining in self.click_indicators:
            # Calculate screen position
            screen_x = int(x - self.camera_x)
            screen_y = int(y - self.camera_y)
            
            # Calculate alpha based on time remaining (fade out effect)
            alpha = min(255, int(time_remaining * 255 / 2.0))
            
            # Create a transparent surface for the indicator
            indicator = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            indicator.fill((0, 0, 0, 0))  # Transparent
            
            # Draw a pulsing circle with fading color
            radius = int(self.tile_size / 2 * (0.5 + 0.5 * (time_remaining % 0.5) * 2))
            pygame.draw.circle(indicator, (255, 255, 0, alpha), (self.tile_size // 2, self.tile_size // 2), radius, 2)
            
            # Draw a crosshair
            pygame.draw.line(indicator, (255, 0, 0, alpha), (self.tile_size // 2, 0), (self.tile_size // 2, self.tile_size), 1)
            pygame.draw.line(indicator, (255, 0, 0, alpha), (0, self.tile_size // 2), (self.tile_size, self.tile_size // 2), 1)
            
            # Blit to screen
            screen.blit(indicator, (screen_x, screen_y))
        
        # Draw player
        self.player.draw(screen, self.camera_x, self.camera_y)
        
        # Draw UI
        # Menu button
        pygame.draw.rect(screen, (100, 100, 100), self.menu_button)
        font = pygame.font.SysFont(None, 24)
        text = font.render("Menu", True, (255, 255, 255))
        screen.blit(text, (self.menu_button.x + 20, self.menu_button.y + 10))
        
        # Game ticks
        ticks_text = font.render(f"Ticks: {self.game_ticks}", True, (255, 255, 255))
        screen.blit(ticks_text, (10, 40))
        
        # Player position
        player_pos_text = font.render(f"Player: ({int(self.player.x // self.tile_size)}, {int(self.player.y // self.tile_size)})", True, (255, 255, 255))
        screen.blit(player_pos_text, (10, 70))
        
        # Camera position
        camera_text = font.render(f"Camera: ({int(self.camera_x)}, {int(self.camera_y)})", True, (255, 255, 255))
        screen.blit(camera_text, (10, 100))
        
        # Movement queue info
        queue_text = font.render(f"Movement Queue: {len(self.player.movement_queue)}", True, (255, 255, 255))
        screen.blit(queue_text, (10, 130))
        
        # Help text
        help_text = font.render("Click to move | Use simulator in console", True, (255, 255, 255))
        screen.blit(help_text, (10, 160))
        
        # Draw debug overlay for click simulator
        debug_text = font.render("Debug: Use 'simulator> click x y' in console", True, (255, 200, 0))
        screen.blit(debug_text, (screen.get_width() - 350, 10))

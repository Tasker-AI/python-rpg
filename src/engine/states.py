import pygame
from src.engine.game_state import GameState
from src.engine.asset_manager import AssetManager
from src.game.tilemap import TileMap, TileType
from src.game.player import Player

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
        self.game_ticks = 0
        self.tick_rate = 0.6  # seconds per tick
        self.tick_timer = 0
        
        # Asset manager
        self.asset_manager = AssetManager()
        
        # Create tilemap
        self.map_width = 25
        self.map_height = 20
        self.tile_size = 32
        self.tilemap = TileMap(self.map_width, self.map_height, self.tile_size)
        self.tilemap.set_asset_manager(self.asset_manager)
        self.tilemap.create_test_map()  # Create a test map with various terrain
        
        # Camera position (top-left corner of the view)
        self.camera_x = 0
        self.camera_y = 0
        
        # Player (starts at grid position 5,5)
        self.player = None  # Will be initialized in enter_state
        
        # UI elements
        self.menu_button = pygame.Rect(700, 550, 80, 30)
        
    def enter_state(self):
        """Called when state becomes active."""
        super().enter_state()
        
        # Load assets
        self.asset_manager.load_image("player", "player.png")
        self.asset_manager.load_image("grass", "grass.png")
        self.asset_manager.load_image("water", "water.png")
        self.asset_manager.load_image("tree", "tree.png")
        self.asset_manager.load_image("rock", "rock.png")
        
        # Initialize player if not already created
        if self.player is None:
            self.player = Player(5, 5, self.tilemap, self.asset_manager)
    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if menu button was clicked
                if self.menu_button.collidepoint(event.pos):
                    self.done = True  # Return to menu
                else:
                    # Convert screen coordinates to world coordinates
                    world_x = event.pos[0] + self.camera_x
                    world_y = event.pos[1] + self.camera_y
                    # Set target position for player to move to
                    self.player.move_to(world_x, world_y)
    
    def update(self, delta_time):
        # Update game tick system
        tick_occurred = False
        self.tick_timer += delta_time
        if self.tick_timer >= self.tick_rate:
            self.game_ticks += 1
            self.tick_timer -= self.tick_rate
            tick_occurred = True
            # Process tick-based game logic here
            print(f"Game tick: {self.game_ticks}")
        
        # Update player
        self.player.update(delta_time, tick_occurred)
        
        # Update camera to follow player
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.camera_x = self.player.x - screen_width // 2
        self.camera_y = self.player.y - screen_height // 2
        
        # Keep camera within map bounds
        self.camera_x = max(0, min(self.camera_x, self.map_width * self.tile_size - screen_width))
        self.camera_y = max(0, min(self.camera_y, self.map_height * self.tile_size - screen_height))
    
    def draw(self, screen):
        # Draw game world
        self.tilemap.draw(screen, self.camera_x, self.camera_y)
        
        # Draw player
        self.player.draw(screen, self.camera_x, self.camera_y)
        
        # Draw UI elements
        tick_text = self.font.render(f"Ticks: {self.game_ticks}", True, (255, 255, 255))
        player_pos_text = self.font.render(f"Position: ({self.player.grid_x}, {self.player.grid_y})", True, (255, 255, 255))
        help_text = self.font.render("Click to move, use buttons for actions", True, (255, 255, 255))
        
        # Draw menu button
        pygame.draw.rect(screen, (100, 100, 200), self.menu_button)
        menu_text = self.font.render("Menu", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)
        
        screen.blit(tick_text, (10, 10))
        screen.blit(player_pos_text, (10, 40))
        screen.blit(help_text, (10, 570))

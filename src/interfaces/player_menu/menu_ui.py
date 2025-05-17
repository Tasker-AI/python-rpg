import pygame
from math import pi

class MenuUI:
    """
    Base class for the game menu UI system.
    Handles the menu bar and tab switching functionality.
    """
    def __init__(self, screen_width, screen_height):
        # Screen dimensions for positioning
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Track which tab is currently active
        self.active_tab = "Inventory"
        
        # Panel settings
        self.panel_width = 144  # Will be calculated in subclasses
        self.panel_height = 252  # Will be calculated in subclasses
        
        # Position panel in bottom right with margins
        self.panel_x = screen_width - self.panel_width - 20  # 20px margin from right
        self.panel_y = screen_height - self.panel_height - 50 - 20  # 50px for menu bar, 20px margin from bottom
        
        # Menu bar settings
        self.menu_height = 50
        self.menu_x = self.panel_x
        self.menu_y = self.panel_y + self.panel_height + 10  # 10px gap between inventory and menu
        self.menu_width = self.panel_width
        
        # Store original dimensions for repositioning
        self.update_position(screen_width, screen_height)
        
        # Menu buttons
        self.buttons = [
            {"name": "Inventory", "active": True},
            {"name": "Armor", "active": False},
            {"name": "Stats", "active": False},
            {"name": "Prayers", "active": False},
            {"name": "Settings", "active": False}
        ]
        self.button_width = self.menu_width // len(self.buttons)
        
        # Colors
        self.panel_bg_color = (50, 50, 50, 200)  # Semi-transparent dark gray
        self.panel_border_color = (100, 100, 100)
        self.slot_bg_color = (70, 70, 70)
        self.slot_border_color = (100, 100, 100)
        self.menu_bg_color = (40, 40, 40)
        self.button_active_color = (60, 100, 200)
        self.button_inactive_color = (80, 80, 80)
        self.text_color = (255, 255, 255)
        
        # Font
        self.font = pygame.font.SysFont(None, 20)
    
    def update_position(self, screen_width, screen_height):
        """Update UI positions based on screen dimensions"""
        # Update stored screen dimensions
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Reposition panel in bottom right with margins
        self.panel_x = screen_width - self.panel_width - 20  # 20px margin from right
        self.panel_y = screen_height - self.panel_height - 50 - 20  # 50px for menu bar, 20px margin from bottom
        
        # Update menu bar position
        self.menu_x = self.panel_x
        self.menu_y = self.panel_y + self.panel_height + 10  # 10px gap between inventory and menu
    
    def draw(self, screen):
        """Draw the menu UI with the active tab content."""
        # Update position based on current screen size
        current_width, current_height = screen.get_size()
        if current_width != self.screen_width or current_height != self.screen_height:
            self.update_position(current_width, current_height)
            
        # Draw panel background
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)
        panel_surface = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.panel_bg_color)
        screen.blit(panel_surface, (self.panel_x, self.panel_y))
        pygame.draw.rect(screen, self.panel_border_color, panel_rect, 2, 3)
        
        # Draw content based on active tab
        self.draw_tab_content(screen)
        
        # Draw menu bar background
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(screen, self.menu_bg_color, menu_rect, 0, 3)
        pygame.draw.rect(screen, self.panel_border_color, menu_rect, 2, 3)
        
        # Draw menu buttons
        for i, button in enumerate(self.buttons):
            button_x = self.menu_x + i * self.button_width
            button_rect = pygame.Rect(button_x, self.menu_y, self.button_width, self.menu_height)
            
            # Draw button background (active or inactive)
            if button["active"]:
                pygame.draw.rect(screen, self.button_active_color, button_rect, 0, 0)
            else:
                pygame.draw.rect(screen, self.button_inactive_color, button_rect, 0, 0)
            
            # Draw button border
            pygame.draw.rect(screen, self.panel_border_color, button_rect, 1, 0)
            
            # Draw button icon based on name
            icon_size = min(self.button_width, self.menu_height) - 10
            icon_surface = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
            icon_surface.fill((0, 0, 0, 0))  # Transparent background
            
            if button["name"] == "Inventory":
                self._draw_inventory_icon(icon_surface)
            elif button["name"] == "Armor":
                self._draw_armor_icon(icon_surface)
            elif button["name"] == "Stats":
                self._draw_stats_icon(icon_surface)
            elif button["name"] == "Prayers":
                self._draw_prayers_icon(icon_surface)
            elif button["name"] == "Settings":
                self._draw_settings_icon(icon_surface)
            
            icon_rect = icon_surface.get_rect(center=button_rect.center)
            screen.blit(icon_surface, icon_rect)
    
    def draw_tab_content(self, screen):
        """Draw the content of the active tab. To be overridden by subclasses."""
        pass
    
    def handle_click(self, mouse_pos):
        """Handle mouse clicks on the menu UI."""
        # Check if any menu button was clicked
        for i, button in enumerate(self.buttons):
            button_x = self.menu_x + i * self.button_width
            button_rect = pygame.Rect(button_x, self.menu_y, self.button_width, self.menu_height)
            
            if button_rect.collidepoint(mouse_pos):
                # Set all buttons to inactive
                for b in self.buttons:
                    b["active"] = False
                # Set clicked button to active
                button["active"] = True
                # Update active tab
                self.active_tab = button["name"]
                return True  # Click was handled
        
        # Check if click was within the panel
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)
        if panel_rect.collidepoint(mouse_pos):
            # Handle tab-specific click logic
            return self.handle_tab_click(mouse_pos)
        
        # Check if click was within the menu bar
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        if menu_rect.collidepoint(mouse_pos):
            return True  # Click was within menu
        
        return False  # Click was not on the menu UI
    
    def handle_tab_click(self, mouse_pos):
        """Handle clicks within the active tab. To be overridden by subclasses."""
        return False
    
    def _draw_placeholder_tab(self, screen, message):
        """Draw a placeholder message for tabs that aren't implemented yet."""
        # Draw centered text message
        text_surface = self.font.render(message, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.panel_x + self.panel_width // 2, 
                                                self.panel_y + self.panel_height // 2))
        screen.blit(text_surface, text_rect)
    
    def _draw_inventory_icon(self, surface):
        """Draw a backpack icon for the Inventory tab"""
        width, height = surface.get_width(), surface.get_height()
        # Draw backpack outline
        color = (220, 220, 220)
        
        # Main backpack body
        pygame.draw.rect(surface, color, (width//4, height//4, width//2, height//2), 2, 2)
        
        # Backpack top flap
        pygame.draw.rect(surface, color, (width//4, height//6, width//2, height//8), 2, 2)
        
        # Backpack straps
        pygame.draw.line(surface, color, (width//4, height//3), (width//8, height//2), 2)
        pygame.draw.line(surface, color, (3*width//4, height//3), (7*width//8, height//2), 2)
    
    def _draw_armor_icon(self, surface):
        """Draw a shield icon for the Armor tab"""
        width, height = surface.get_width(), surface.get_height()
        color = (220, 220, 220)
        
        # Shield outline
        points = [
            (width//2, height//6),  # Top
            (width//6, height//3),  # Top left
            (width//6, 2*height//3),  # Bottom left
            (width//2, 5*height//6),  # Bottom
            (5*width//6, 2*height//3),  # Bottom right
            (5*width//6, height//3),  # Top right
        ]
        pygame.draw.polygon(surface, color, points, 2)
        
        # Shield emblem
        pygame.draw.circle(surface, color, (width//2, height//2), width//6, 2)
    
    def _draw_stats_icon(self, surface):
        """Draw a bar chart icon for the Stats tab"""
        width, height = surface.get_width(), surface.get_height()
        color = (220, 220, 220)
        
        # Base line
        pygame.draw.line(surface, color, (width//6, 3*height//4), (5*width//6, 3*height//4), 2)
        
        # Vertical axis
        pygame.draw.line(surface, color, (width//6, height//4), (width//6, 3*height//4), 2)
        
        # Bars
        bar_width = width//10
        pygame.draw.rect(surface, color, (width//4, height//2, bar_width, height//4), 2)
        pygame.draw.rect(surface, color, (width//2, height//3, bar_width, 5*height//12), 2)
        pygame.draw.rect(surface, color, (3*width//4, 2*height//3, bar_width, height//12), 2)
    
    def _draw_prayers_icon(self, surface):
        """Draw a star icon for the Prayers tab"""
        width, height = surface.get_width(), surface.get_height()
        color = (220, 220, 220)
        center = (width//2, height//2)
        radius = min(width, height) // 3
        
        # Draw a star
        points = []
        for i in range(10):
            angle = (2*pi * i) / 10
            r = radius if i % 2 == 0 else radius // 2
            x = center[0] + int(r * pygame.math.Vector2(1, 0).rotate(angle * 180 / pi).x)
            y = center[1] + int(r * pygame.math.Vector2(1, 0).rotate(angle * 180 / pi).y)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points, 2)
    
    def _draw_settings_icon(self, surface):
        """Draw a gear icon for the Settings tab"""
        width, height = surface.get_width(), surface.get_height()
        color = (220, 220, 220)
        center = (width//2, height//2)
        outer_radius = min(width, height) // 3
        inner_radius = outer_radius // 1.6
        teeth = 8
        
        # Draw gear teeth
        points = []
        for i in range(teeth * 2):
            angle = (2*pi * i) / (teeth * 2)
            r = outer_radius if i % 2 == 0 else inner_radius
            x = center[0] + int(r * pygame.math.Vector2(1, 0).rotate(angle * 180 / pi).x)
            y = center[1] + int(r * pygame.math.Vector2(1, 0).rotate(angle * 180 / pi).y)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points, 2)
        
        # Draw center circle
        pygame.draw.circle(surface, color, center, outer_radius // 3, 2)

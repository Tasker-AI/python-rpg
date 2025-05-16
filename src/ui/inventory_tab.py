import pygame
from src.ui.menu_ui import MenuUI

class InventoryUI(MenuUI):
    """
    Inventory UI that displays in the bottom right of the screen.
    Contains 28 inventory slots and a menu bar with buttons.
    """
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        
        # Inventory-specific settings
        self.slot_size = 32
        self.slot_padding = 4
        self.slots_per_row = 4
        self.num_rows = 7  # 7 rows of 4 slots (28 slots total)
        
        # Calculate panel size based on slots and padding
        self.panel_width = (self.slot_size + self.slot_padding) * self.slots_per_row + self.slot_padding
        self.panel_height = (self.slot_size + self.slot_padding) * self.num_rows + self.slot_padding
        
        # Update panel position
        self.panel_x = screen_width - self.panel_width - 20  # 20px margin from right
        self.panel_y = screen_height - self.panel_height - 50 - 20  # 50px for menu bar, 20px margin from bottom
        
        # Update menu bar position
        self.menu_x = self.panel_x
        self.menu_y = self.panel_y + self.panel_height + 10  # 10px gap between inventory and menu
        self.menu_width = self.panel_width
        
        # Create inventory slots (7 rows, 4 columns)
        self.slots = []
        for row in range(7):
            for col in range(4):
                x = self.panel_x + col * (self.slot_size + self.slot_padding) + self.slot_padding
                y = self.panel_y + row * (self.slot_size + self.slot_padding) + self.slot_padding
                self.slots.append({
                    "rect": pygame.Rect(x, y, self.slot_size, self.slot_size),
                    "item": None
                })
    
    def draw_tab_content(self, screen):
        """Draw the content based on the active tab."""
        if self.active_tab == "Inventory":
            self._draw_inventory_tab(screen)
        elif self.active_tab == "Armor":
            from src.ui.armor_tab import draw_armor_tab
            draw_armor_tab(self, screen)
        elif self.active_tab == "Stats":
            from src.ui.stats_tab import draw_stats_tab
            draw_stats_tab(self, screen)
        elif self.active_tab == "Prayers":
            from src.ui.prayers_tab import draw_prayers_tab
            draw_prayers_tab(self, screen)
        elif self.active_tab == "Settings":
            from src.ui.settings_tab import draw_settings_tab
            draw_settings_tab(self, screen)
    
    def _draw_inventory_tab(self, screen):
        """Draw the inventory slots."""
        for slot in self.slots:
            pygame.draw.rect(screen, self.slot_bg_color, slot["rect"], 0, 2)
            pygame.draw.rect(screen, self.slot_border_color, slot["rect"], 1, 2)
            
            # If the slot has an item, draw it (to be implemented later)
            if slot["item"]:
                pass  # Will draw item icon here
    
    def handle_tab_click(self, mouse_pos):
        """Handle clicks within the active tab."""
        if self.active_tab == "Inventory":
            # Check if any inventory slot was clicked
            for slot in self.slots:
                if slot["rect"].collidepoint(mouse_pos):
                    # Handle slot click (to be implemented later)
                    return True  # Click was handled
        elif self.active_tab == "Settings":
            from src.ui.settings_tab import handle_settings_click
            result = handle_settings_click(self, mouse_pos)
            if result:
                return result
        
        # If we got here, click was within panel but not handled by any specific element
        return True

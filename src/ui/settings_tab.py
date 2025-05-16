import pygame

def draw_settings_tab(ui, screen):
    """Draw the settings tab content with a Log out button."""
    # Create a Log out button
    button_width = ui.panel_width - 40  # 20px margin on each side
    button_height = 40
    button_x = ui.panel_x + 20
    button_y = ui.panel_y + 20
    
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Store the button for click detection
    ui.return_button_rect = button_rect
    
    # Draw button
    pygame.draw.rect(screen, (80, 80, 150), button_rect, 0, 5)  # Blue button with rounded corners
    pygame.draw.rect(screen, (100, 100, 180), button_rect, 2, 5)  # Lighter border
    
    # Draw button text
    text_surface = ui.font.render("Log out", True, ui.text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def handle_settings_click(ui, mouse_pos):
    """Handle clicks in the settings tab."""
    if hasattr(ui, 'return_button_rect') and ui.return_button_rect.collidepoint(mouse_pos):
        # Signal that the user wants to return to character select
        return "return_to_character_select"
    return True

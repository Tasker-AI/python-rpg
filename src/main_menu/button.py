import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=None, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or self._adjust_color(color, 1.2)
        self.text_color = text_color
        self.radius = 5
    
    def _adjust_color(self, color, factor):
        """Make color lighter or darker"""
        return tuple(min(255, max(0, int(c * factor))) for c in color)
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen, font):
        """Draw the button"""
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect, border_radius=self.radius)
        
        # Draw button text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

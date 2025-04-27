import pygame
import os
import sys

def create_placeholder_assets():
    """
    Creates placeholder assets for development.
    This is a utility function to generate simple placeholder graphics.
    """
    # Ensure the asset directories exist
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    image_dir = os.path.join(base_dir, "assets", "images")
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # Create player placeholder
    player_img = pygame.Surface((32, 32))
    player_img.fill((255, 0, 0))  # Red square
    pygame.draw.circle(player_img, (200, 0, 0), (16, 16), 12)  # Darker red circle
    pygame.image.save(player_img, os.path.join(image_dir, "player.png"))
    
    # Create terrain placeholders
    # Grass
    grass_img = pygame.Surface((32, 32))
    grass_img.fill((0, 150, 0))
    for i in range(5):
        x = 5 + i * 5
        y = 20 + (i % 3) * 4
        pygame.draw.line(grass_img, (0, 200, 0), (x, y), (x, y - 10), 1)
    pygame.image.save(grass_img, os.path.join(image_dir, "grass.png"))
    
    # Water
    water_img = pygame.Surface((32, 32))
    water_img.fill((0, 0, 180))
    for i in range(4):
        y = 8 + i * 8
        pygame.draw.line(water_img, (100, 100, 255), (0, y), (32, y), 2)
    pygame.image.save(water_img, os.path.join(image_dir, "water.png"))
    
    # Tree
    tree_img = pygame.Surface((32, 64))
    tree_img.fill((0, 0, 0, 0))
    tree_img.set_colorkey((0, 0, 0))
    # Trunk
    pygame.draw.rect(tree_img, (139, 69, 19), (12, 32, 8, 32))
    # Leaves
    pygame.draw.circle(tree_img, (0, 100, 0), (16, 20), 16)
    pygame.draw.circle(tree_img, (0, 120, 0), (16, 16), 12)
    pygame.image.save(tree_img, os.path.join(image_dir, "tree.png"))
    
    # Rock
    rock_img = pygame.Surface((32, 32))
    rock_img.fill((0, 0, 0, 0))
    rock_img.set_colorkey((0, 0, 0))
    pygame.draw.circle(rock_img, (100, 100, 100), (16, 16), 12)
    pygame.draw.circle(rock_img, (120, 120, 120), (14, 14), 4)
    pygame.image.save(rock_img, os.path.join(image_dir, "rock.png"))
    
    # UI Elements
    # Button
    button_img = pygame.Surface((80, 30))
    button_img.fill((80, 80, 180))
    pygame.draw.rect(button_img, (100, 100, 200), (2, 2, 76, 26))
    pygame.image.save(button_img, os.path.join(image_dir, "button.png"))
    
    # Button (hover)
    button_hover_img = pygame.Surface((80, 30))
    button_hover_img.fill((100, 100, 220))
    pygame.draw.rect(button_hover_img, (120, 120, 240), (2, 2, 76, 26))
    pygame.image.save(button_hover_img, os.path.join(image_dir, "button_hover.png"))
    
    # Health bar
    health_bar_img = pygame.Surface((100, 10))
    health_bar_img.fill((200, 0, 0))
    pygame.image.save(health_bar_img, os.path.join(image_dir, "health_bar.png"))
    
    # Health bar background
    health_bar_bg_img = pygame.Surface((100, 10))
    health_bar_bg_img.fill((100, 100, 100))
    pygame.image.save(health_bar_bg_img, os.path.join(image_dir, "health_bar_bg.png"))
    
    print("Placeholder assets created successfully!")

if __name__ == "__main__":
    pygame.init()
    create_placeholder_assets()
    pygame.quit()

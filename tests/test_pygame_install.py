import sys

def test_pygame_install():
    try:
        import pygame
        print(f"Pygame successfully installed. Version: {pygame.version.ver}")
        return True
    except ImportError:
        print("Pygame is not installed. Please install it using 'pip install pygame'")
        return False

if __name__ == "__main__":
    test_pygame_install()

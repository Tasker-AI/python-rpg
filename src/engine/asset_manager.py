import os
import pygame

class AssetManager:
    """
    Manages game assets like images and sounds.
    Provides a centralized way to load and access assets.
    """
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        self.image_path = os.path.join(self.base_path, "images")
        self.sound_path = os.path.join(self.base_path, "sounds")
    
    def load_image(self, name, filename, colorkey=None, scale=1):
        """
        Load an image and store it in the images dictionary.
        
        Args:
            name: Key to store the image under
            filename: Filename of the image to load
            colorkey: Color to use as transparency (None for no transparency)
            scale: Scale factor for the image
        
        Returns:
            The loaded image
        """
        if name in self.images:
            return self.images[name]
            
        fullpath = os.path.join(self.image_path, filename)
        try:
            image = pygame.image.load(fullpath)
            
            if scale != 1:
                original_size = image.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                image = pygame.transform.scale(image, new_size)
                
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)
                
            # Convert for faster blitting
            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert()
                
            self.images[name] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
            # Return a placeholder image (red square)
            placeholder = pygame.Surface((32, 32))
            placeholder.fill((255, 0, 0))
            self.images[name] = placeholder
            return placeholder
    
    def load_sound(self, name, filename):
        """
        Load a sound and store it in the sounds dictionary.
        
        Args:
            name: Key to store the sound under
            filename: Filename of the sound to load
            
        Returns:
            The loaded sound
        """
        if name in self.sounds:
            return self.sounds[name]
            
        fullpath = os.path.join(self.sound_path, filename)
        try:
            sound = pygame.mixer.Sound(fullpath)
            self.sounds[name] = sound
            return sound
        except pygame.error as e:
            print(f"Error loading sound {filename}: {e}")
            # Return a dummy sound object
            class DummySound:
                def play(self): pass
                def stop(self): pass
                def set_volume(self, volume): pass
            
            dummy = DummySound()
            self.sounds[name] = dummy
            return dummy
    
    def load_font(self, name, filename, size):
        """
        Load a font and store it in the fonts dictionary.
        
        Args:
            name: Key to store the font under
            filename: Filename of the font to load
            size: Size of the font
            
        Returns:
            The loaded font
        """
        key = f"{name}_{size}"
        if key in self.fonts:
            return self.fonts[key]
            
        # Check if it's a system font or a custom font
        if filename.endswith('.ttf') or filename.endswith('.otf'):
            fullpath = os.path.join(self.base_path, "fonts", filename)
            try:
                font = pygame.font.Font(fullpath, size)
            except pygame.error as e:
                print(f"Error loading font {filename}: {e}")
                font = pygame.font.Font(None, size)  # Default font
        else:
            # Use system font
            try:
                font = pygame.font.SysFont(filename, size)
            except pygame.error:
                font = pygame.font.Font(None, size)  # Default font
                
        self.fonts[key] = font
        return font
    
    def get_image(self, name):
        """Get a previously loaded image by name."""
        return self.images.get(name)
    
    def get_sound(self, name):
        """Get a previously loaded sound by name."""
        return self.sounds.get(name)
    
    def get_font(self, name, size):
        """Get a previously loaded font by name and size."""
        key = f"{name}_{size}"
        return self.fonts.get(key)
    
    def preload_assets(self):
        """
        Preload commonly used assets at startup.
        This helps avoid loading delays during gameplay.
        """
        # This will be filled in as we add actual game assets
        pass

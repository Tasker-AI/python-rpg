"""
Asset Manager for loading and managing game assets like images, sounds, and fonts.
"""
import os
import pygame
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple

class AssetManager:
    """
    Manages loading and accessing game assets such as images, sounds, and fonts.
    Handles caching to avoid loading the same asset multiple times.
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize the AssetManager.
        
        Args:
            base_path: Base directory path for assets. If None, defaults to 'assets' in the project root.
        """
        # Set base path for assets
        if base_path is None:
            # Default to 'assets' directory in the project root
            self.base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        else:
            self.base_path = base_path
            
        # Asset caches
        self._images: Dict[str, pygame.Surface] = {}
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        self._json_data: Dict[str, Any] = {}
        
        # Default font settings
        self._default_font = None
        self._default_font_size = 24
        
        # Initialize pygame mixer if not already initialized
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
    
    def _get_asset_path(self, *path_parts: str) -> str:
        """
        Construct an absolute path to an asset.
        
        Args:
            *path_parts: Parts of the path to join with the base path.
            
        Returns:
            str: Absolute path to the asset.
        """
        return os.path.join(self.base_path, *path_parts)
    
    def load_image(self, name: str, path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
        """
        Load an image and store it in the cache.
        
        Args:
            name: Unique identifier for the image.
            path: Relative path to the image file from the assets directory.
            convert_alpha: Whether to use convert_alpha() for images with transparency.
            
        Returns:
            Loaded pygame.Surface or None if loading failed.
        """
        if name in self._images:
            return self._images[name]
            
        try:
            full_path = self._get_asset_path(path)
            if not os.path.exists(full_path):
                print(f"Image not found: {full_path}")
                return None
                
            if convert_alpha:
                image = pygame.image.load(full_path).convert_alpha()
            else:
                image = pygame.image.load(full_path).convert()
                
            self._images[name] = image
            return image
            
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def get_image(self, name: str) -> Optional[pygame.Surface]:
        """
        Get a loaded image by name.
        
        Args:
            name: Name of the image to retrieve.
            
        Returns:
            The loaded pygame.Surface or None if not found.
        """
        return self._images.get(name)
    
    def load_sound(self, name: str, path: str) -> Optional[pygame.mixer.Sound]:
        """
        Load a sound effect and store it in the cache.
        
        Args:
            name: Unique identifier for the sound.
            path: Relative path to the sound file from the assets directory.
            
        Returns:
            Loaded pygame.mixer.Sound or None if loading failed.
        """
        if name in self._sounds:
            return self._sounds[name]
            
        try:
            full_path = self._get_asset_path(path)
            if not os.path.exists(full_path):
                print(f"Sound not found: {full_path}")
                return None
                
            sound = pygame.mixer.Sound(full_path)
            self._sounds[name] = sound
            return sound
            
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            return None
    
    def get_sound(self, name: str) -> Optional[pygame.mixer.Sound]:
        """
        Get a loaded sound by name.
        
        Args:
            name: Name of the sound to retrieve.
            
        Returns:
            The loaded pygame.mixer.Sound or None if not found.
        """
        return self._sounds.get(name)
    
    def load_font(self, name: str, path: str, size: int = 24) -> Optional[pygame.font.Font]:
        """
        Load a font and store it in the cache.
        
        Args:
            name: Base name for the font.
            path: Relative path to the font file from the assets directory.
            size: Size of the font.
            
        Returns:
            Loaded pygame.font.Font or None if loading failed.
        """
        cache_key = (name, size)
        if cache_key in self._fonts:
            return self._fonts[cache_key]
            
        try:
            full_path = self._get_asset_path(path)
            if not os.path.exists(full_path):
                # Try to use a system font as fallback
                font = pygame.font.SysFont(name, size)
                if font.name.lower() != name.lower():
                    print(f"Font {name} not found, using fallback: {font.name}")
            else:
                font = pygame.font.Font(full_path, size)
                
            self._fonts[cache_key] = font
            return font
            
        except Exception as e:
            print(f"Error loading font {path}: {e}")
            return None
    
    def get_font(self, name: str, size: int = 24) -> Optional[pygame.font.Font]:
        """
        Get a loaded font by name and size.
        
        Args:
            name: Name of the font to retrieve.
            size: Size of the font.
            
        Returns:
            The loaded pygame.font.Font or None if not found.
        """
        return self._fonts.get((name, size))
    
    def load_json(self, name: str, path: str) -> Optional[Dict[str, Any]]:
        """
        Load a JSON file and store it in the cache.
        
        Args:
            name: Unique identifier for the JSON data.
            path: Relative path to the JSON file from the assets directory.
            
        Returns:
            Parsed JSON data as a dictionary or None if loading failed.
        """
        if name in self._json_data:
            return self._json_data[name]
            
        try:
            full_path = self._get_asset_path(path)
            if not os.path.exists(full_path):
                print(f"JSON file not found: {full_path}")
                return None
                
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self._json_data[name] = data
            return data
            
        except Exception as e:
            print(f"Error loading JSON {path}: {e}")
            return None
    
    def get_json(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get loaded JSON data by name.
        
        Args:
            name: Name of the JSON data to retrieve.
            
        Returns:
            The loaded JSON data as a dictionary or None if not found.
        """
        return self._json_data.get(name)
    
    def set_default_font(self, name: str, size: int = 24) -> bool:
        """
        Set the default font to use for text rendering.
        
        Args:
            name: Name of the font to set as default.
            size: Size of the font.
            
        Returns:
            True if the font was set successfully, False otherwise.
        """
        font = self.get_font(name, size)
        if font:
            self._default_font = font
            self._default_font_size = size
            return True
        return False
    
    def get_default_font(self) -> Tuple[Optional[pygame.font.Font], int]:
        """
        Get the default font and size.
        
        Returns:
            A tuple of (font, size). If no default is set, returns (None, default_size).
        """
        if self._default_font is None:
            # Try to load a default system font
            self._default_font = pygame.font.SysFont('Arial', self._default_font_size)
        return self._default_font, self._default_font_size
    
    def create_text_surface(self, text: str, color: Tuple[int, int, int] = (0, 0, 0), 
                          font_name: str = None, font_size: int = None) -> pygame.Surface:
        """
        Create a surface with rendered text.
        
        Args:
            text: Text to render.
            color: RGB color tuple for the text.
            font_name: Name of the font to use. If None, uses the default font.
            font_size: Size of the font. If None, uses the default size.
            
        Returns:
            A pygame.Surface with the rendered text.
        """
        if font_name is not None or font_size is not None:
            size = font_size if font_size is not None else self._default_font_size
            name = font_name if font_name is not None else 'Arial'
            font = self.get_font(name, size)
            if font is None:
                font = pygame.font.SysFont(name, size)
        else:
            font, _ = self.get_default_font()
        
        return font.render(text, True, color)
    
    def clear_cache(self, cache_type: str = None):
        """
        Clear the specified cache or all caches.
        
        Args:
            cache_type: Type of cache to clear ('images', 'sounds', 'fonts', 'json').
                       If None, clears all caches.
        """
        if cache_type is None or cache_type == 'images':
            self._images.clear()
        if cache_type is None or cache_type == 'sounds':
            self._sounds.clear()
        if cache_type is None or cache_type == 'fonts':
            self._fonts.clear()
        if cache_type is None or cache_type == 'json':
            self._json_data.clear()

# Create a global instance for easy access
asset_manager = AssetManager()

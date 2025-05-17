"""
Engine module containing core game engine components.
"""

# Import key components to make them available at the package level
from .asset_manager import AssetManager, asset_manager

# This makes it possible to import like: from src.engine import asset_manager
__all__ = ['AssetManager', 'asset_manager']

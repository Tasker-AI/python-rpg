from .resource import Resource, ResourceType
import random

class Tree(Resource):
    """A tree resource that can be harvested for wood."""
    
    def __init__(self, x: int, y: int):
        """
        Initialize a tree resource.
        
        Args:
            x: Grid x-coordinate
            y: Grid y-coordinate
        """
        super().__init__(x, y, ResourceType.TREE, harvest_time=2, walkable=False)  # Trees block movement
        
    def get_rewards(self) -> dict:
        """
        Get the rewards for harvesting this tree.
        
        Returns:
            dict: Dictionary of item types and quantities
        """
        # 1-3 wood per tree
        return {"wood": random.randint(1, 3)}

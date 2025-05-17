from .resource import Resource, ResourceType
import random

class Rock(Resource):
    """A rock resource that can be harvested for stone."""
    
    def __init__(self, x: int, y: int):
        """
        Initialize a rock resource.
        
        Args:
            x: Grid x-coordinate
            y: Grid y-coordinate
        """
        super().__init__(x, y, ResourceType.ROCK, harvest_time=3, walkable=False)  # Rocks block movement
        
    def get_rewards(self) -> dict:
        """
        Get the rewards for harvesting this rock.
        
        Returns:
            dict: Dictionary of item types and quantities
        """
        # 1-2 stone per rock, with a chance of flint
        rewards = {"stone": random.randint(1, 2)}
        if random.random() < 0.3:  # 30% chance for flint
            rewards["flint"] = 1
        return rewards

class GameState:
    """Base class for all game states"""
    def __init__(self):
        self.done = False
        self.next_state = None
        
    def handle_events(self, events):
        """Handle pygame events. Override in child classes."""
        pass
        
    def update(self, delta_time):
        """Update game state. Override in child classes."""
        pass
        
    def draw(self, screen):
        """Draw state to the screen. Override in child classes."""
        pass
        
    def enter_state(self):
        """Called when state becomes active."""
        self.done = False
        
    def exit_state(self):
        """Called when state becomes inactive."""
        pass


class GameStateManager:
    """Manages different game states and transitions between them"""
    def __init__(self):
        self.states = {}
        self.current_state = None
        
    def add_state(self, state_name, state):
        """Add a state to the state manager."""
        # TODO: Implement this method
        pass
        
    def change_state(self, state_name):
        """Change to a different state."""
        # TODO: Implement this method
        pass
        
    def update(self, delta_time):
        """Update current state and handle state changes."""
        # TODO: Implement this method
        pass
        
    def draw(self, screen):
        """Draw current state to the screen."""
        # TODO: Implement this method
        pass
        
    def handle_events(self, events):
        """Pass events to current state."""
        # TODO: Implement this method
        pass

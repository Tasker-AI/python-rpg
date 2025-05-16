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
    """Manages different game states"""
    
    _instance = None
    
    @classmethod
    def instance(cls):
        """Get the singleton instance of GameStateManager"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.states = {}
        self.current_state = None
        
        # Set this instance as the singleton instance
        GameStateManager._instance = self
        
    def add_state(self, state_name, state):
        """Add a state to the manager"""
        self.states[state_name] = state
        state.manager = self
        
    def get_state(self, state_name):
        """Get a state by name"""
        return self.states.get(state_name)
        
    def change_state(self, state_name):
        """Change to a different state."""
        if state_name in self.states:
            # Exit current state if it exists
            if self.current_state:
                self.states[self.current_state].exit_state()
            
            # Change to new state
            self.current_state = state_name
            self.states[self.current_state].enter_state()
        
    def update(self, delta_time):
        """Update current state and handle state changes."""
        if self.current_state:
            current = self.states[self.current_state]
            current.update(delta_time)
            
            # Check if state is done and needs to transition
            if current.done and current.next_state:
                next_state_name = current.next_state
                current.done = False  # Reset done flag to prevent infinite transitions
                self.change_state(next_state_name)
        
    def draw(self, screen):
        """Draw current state to the screen."""
        if self.current_state:
            self.states[self.current_state].draw(screen)
        
    def handle_events(self, events):
        """Pass events to current state."""
        if self.current_state:
            self.states[self.current_state].handle_events(events)

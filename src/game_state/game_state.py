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
        
    def resize(self, width, height):
        """Called when the screen is resized. Override in child classes."""
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
        
    def change_state(self, state_name, state_args=None):
        """
        Change to a different state.
        
        Args:
            state_name: Name of the state to change to, or a tuple of (state_name, state_args)
            state_args: Optional dictionary of arguments to pass to the state's enter_state method
        """
        # Handle case where state_name is a tuple of (state_name, state_args)
        if isinstance(state_name, tuple) and len(state_name) == 2 and isinstance(state_name[1], dict):
            state_name, state_args = state_name
        
        if state_name in self.states:
            # Exit current state if it exists
            if self.current_state:
                self.states[self.current_state].exit_state()
            
            # Change to new state
            self.current_state = state_name
            
            # Call enter_state with provided arguments if any
            if state_args:
                self.states[self.current_state].enter_state(**state_args)
            else:
                self.states[self.current_state].enter_state()
        
    def update(self, delta_time):
        """Update current state and handle state changes."""
        if self.current_state:
            current = self.states[self.current_state]
            current.update(delta_time)
            
            # Check if state is done and needs to transition
            if current.done and current.next_state:
                next_state = current.next_state
                current.done = False  # Reset done flag to prevent infinite transitions
                
                # If next_state is a tuple, unpack it for the change_state method
                if isinstance(next_state, tuple) and len(next_state) == 2 and isinstance(next_state[1], dict):
                    self.change_state(next_state[0], next_state[1])
                else:
                    self.change_state(next_state)
        
    def draw(self, screen):
        """Draw current state to the screen."""
        if self.current_state:
            self.states[self.current_state].draw(screen)
        
    def handle_events(self, events):
        """Pass events to current state.
        
        Args:
            events: List of pygame events
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        if self.current_state:
            self.states[self.current_state].handle_events(events)
            
    def resize(self, width, height):
        """Notify the current state that the screen was resized.
        
        Args:
            width: New screen width
            height: New screen height
        """
        if self.current_state:
            self.states[self.current_state].resize(width, height)

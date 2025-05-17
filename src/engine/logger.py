"""
Logger module for the game.
Provides detailed logging of game events, input handling, and errors.
"""
import os
import logging
import datetime
from enum import Enum

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class GameLogger:
    """
    Game logger class that handles logging of game events.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with file and console handlers."""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Generate log filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"logs/game_{timestamp}.log"
        
        # Configure root logger
        self.logger = logging.getLogger('game')
        self.logger.setLevel(logging.DEBUG)  # Set to DEBUG level for more detailed logging
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create file handler
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)  # Changed from DEBUG to INFO
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Show all messages in console
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.debug("Logger initialized")
    
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)
    
    def log_mouse_event(self, event_type, position, button=None):
        """Log mouse events with detailed information."""
        if button:
            self.debug(f"Mouse {event_type}: pos={position}, button={button}")
        else:
            self.debug(f"Mouse {event_type}: pos={position}")
    
    def log_player_movement(self, start_pos, target_pos, path=None):
        """Log player movement with start, target, and path."""
        if path:
            self.debug(f"Player movement: from {start_pos} to {target_pos}, path length: {len(path)}")
            self.debug(f"Path: {path}")
        else:
            self.debug(f"Player movement: from {start_pos} to {target_pos}, no path found")
    
    def log_game_state(self, state_name, action):
        """Log game state changes."""
        self.info(f"Game state {action}: {state_name}")
    
    def log_tick(self, tick_number, delta_time):
        """Log game tick information."""
        self.debug(f"Game tick {tick_number}: delta_time={delta_time:.4f}s")

# Create a global logger instance
game_logger = GameLogger()

"""
Click Simulator module for testing and debugging.
Allows simulating mouse clicks and other events from the console.
"""
import pygame
import threading
import time
import cmd
from src.engine.logger import game_logger

class ClickSimulator(cmd.Cmd):
    """
    Console-based click simulator for testing and debugging.
    Allows simulating mouse clicks and other events without user input.
    """
    prompt = 'simulator> '
    intro = 'Click Simulator started. Type "help" for commands.'
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.events_queue = []
        self.thread = None
    
    def start(self):
        """Start the simulator in a separate thread"""
        self.thread = threading.Thread(target=self.cmdloop)
        self.thread.daemon = True  # Allow the thread to exit when main program exits
        self.thread.start()
        game_logger.info("Click simulator started")
    
    def stop(self):
        """Stop the simulator"""
        self.running = False
        game_logger.info("Click simulator stopped")
    
    def get_events(self):
        """Get and clear the events queue"""
        events = self.events_queue.copy()
        self.events_queue.clear()
        return events
    
    def do_click(self, arg):
        """
        Simulate a mouse click at the specified coordinates.
        Usage: click x y [button=1]
        """
        args = arg.split()
        if len(args) < 2:
            print("Error: Need at least x and y coordinates")
            return
        
        try:
            x = int(args[0])
            y = int(args[1])
            button = int(args[2]) if len(args) > 2 else 1
            
            # Create a mouse down event
            event_dict = {
                'type': pygame.MOUSEBUTTONDOWN,
                'pos': (x, y),
                'button': button
            }
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, event_dict)
            self.events_queue.append(event)
            
            game_logger.info(f"Simulated click at ({x}, {y}) with button {button}")
            print(f"Click at ({x}, {y}) with button {button} simulated")
        except ValueError:
            print("Error: Coordinates and button must be integers")
    
    def do_move(self, arg):
        """
        Simulate mouse movement to the specified coordinates.
        Usage: move x y
        """
        args = arg.split()
        if len(args) < 2:
            print("Error: Need x and y coordinates")
            return
        
        try:
            x = int(args[0])
            y = int(args[1])
            
            # Create a mouse motion event
            event_dict = {
                'type': pygame.MOUSEMOTION,
                'pos': (x, y),
                'rel': (0, 0),
                'buttons': (0, 0, 0)
            }
            event = pygame.event.Event(pygame.MOUSEMOTION, event_dict)
            self.events_queue.append(event)
            
            game_logger.info(f"Simulated mouse move to ({x}, {y})")
            print(f"Mouse moved to ({x}, {y})")
        except ValueError:
            print("Error: Coordinates must be integers")
    
    def do_key(self, arg):
        """
        Simulate a key press.
        Usage: key keycode
        """
        try:
            keycode = int(arg)
            event = pygame.event.Event(pygame.KEYDOWN, {'key': keycode})
            self.events_queue.append(event)
            
            game_logger.info(f"Simulated key press with keycode {keycode}")
            print(f"Key press with keycode {keycode} simulated")
        except ValueError:
            print("Error: Keycode must be an integer")
    
    def do_quit(self, arg):
        """Exit the simulator"""
        game_logger.info("Click simulator quit command received")
        print("Exiting simulator...")
        return True
    
    def do_exit(self, arg):
        """Exit the simulator"""
        return self.do_quit(arg)
    
    def do_help(self, arg):
        """Show help message"""
        if not arg:
            print("Available commands:")
            print("  click x y [button] - Simulate a mouse click at (x,y)")
            print("  move x y - Simulate mouse movement to (x,y)")
            print("  key keycode - Simulate a key press")
            print("  quit/exit - Exit the simulator")
            print("  help [command] - Show help for a command")
        else:
            super().do_help(arg)

# Create a global simulator instance
click_simulator = ClickSimulator()

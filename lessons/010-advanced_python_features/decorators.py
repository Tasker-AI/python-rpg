### Lesson - Decorators in Python ###

# Purpose: Decorators allow you to modify or enhance functions without changing their code
# When to use: Logging, timing, access control, caching results, or adding game mechanics
# Example: Adding cooldowns to abilities, tracking high scores, logging player actions

import time
import functools

### Exercise 1 ###
# Create a decorator that:
# 1. Records and prints how long a function takes to execute
# 2. Returns the original function result
# 3. Displays time in milliseconds (ms)

# Decorator syntax:
# def decorator_name(func):
#     def wrapper(*args, **kwargs):
#         # Do something before
#         result = func(*args, **kwargs)
#         # Do something after
#         return result
#     return wrapper


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration_ms = (end_time - start_time) * 1000  # Convert seconds to milliseconds
        
        print(f"{func.__name__} took {duration_ms:.2f} ms to execute")
        return result
    return wrapper

# Apply your decorator to this slow function:
@timer_decorator
def slow_player_lookup(player_id):
    """Simulates a slow database lookup for a player"""
    time.sleep(0.2)  # Simulate slow operation
    return f"Player {player_id}"


### Exercise 2 ###
# Create a decorator with parameters that:
# 1. Enforces a cooldown period between function calls
# 2. If called too soon, prints "Ability on cooldown" and returns None
# 3. Otherwise executes the function normally
# 
# Example of decorator with parameters:
# def decorator_with_args(param):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             # Use param and func here
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator


def cooldown(seconds):
    # This outer function takes the parameter (cooldown duration)
    def decorator(func):
        
        # Store the last time the function was called
        last_called = 0  # Start with 0 (epoch time)
        
        def wrapper(*args, **kwargs):
        
            nonlocal last_called  # Use the variable from outer scope
            current_time = time.time()
        
            # Check if enough time has passed
            if current_time - last_called < seconds:
                print("Ability on cooldown")
                return None
            
            # If enough time has passed, update last_called and run the function
            last_called = current_time
            return func(*args, **kwargs)
        
        
        return wrapper
    return decorator


@cooldown(2)  # 2 second cooldown
def fireball():
    """A powerful spell with a cooldown"""
    return "Fireball cast!"


### Exercise 3 ###
# Create a context manager that:
# 1. Measures time taken for a block of code
# 2. Prints "Starting game level..." at the start
# 3. Prints "Level completed in X.XX seconds" at the end
#
# Context manager syntax:
# class ContextName:
#     def __init__(self, parameters):
#         self.parameter = parameters
#     
#     def __enter__(self):
#         # Setup code
#         return something
#     
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         # Cleanup code
#         pass


class LevelTimer:
    def __init__(self):
        # 1. Measures time taken for a block of code
        self.start_time = 0    # Initialize, but set actual time in __enter__
        
    def __enter__(self):
        # Record start time when the context is entered
        self.start_time = time.time() 
        
        # 2. Prints "Starting game level..." at the start
        print("Starting game level...")
        
        # Context managers should return self
        return self 
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 3. Prints "Level completed in X.XX seconds" at the end
        end_time = time.time()
        time_taken = (end_time - self.start_time) * 1000
        print(f"level completed in {time_taken:.2f}")
    
    




# Tests #
def runtests():
    # Test Exercise 1: Timer decorator
    print("Test 1: Timer decorator")
    result = slow_player_lookup(123)
    print(f"Function returned: {result}")
    print("Test passed if you see timing information and correct result above")
    
    # Test Exercise 2: Cooldown decorator
    print("\nTest 2: Cooldown decorator")
    print("First call:", fireball())
    print("Second call (should be on cooldown):", fireball())
    time.sleep(2.1)  # Wait for cooldown to finish
    print("After waiting:", fireball())
    print("Test passed if second call shows cooldown message")
    
    # Test Exercise 3: Context manager
    print("\nTest 3: Context manager")
    with LevelTimer() as timer:
        print("  Running level code...")
        time.sleep(0.5)  # Simulate level execution
        print("  Spawning enemies...")
        time.sleep(0.3)
    
    print("Test passed if you see the starting and completion messages")
    
    # Bonus: Create a function for demonstration only
    def slow_function(iterations):
        total = 0
        for i in range(iterations):
            total += i
            time.sleep(0.001)
        return total
    
    # Combining multiple concepts - this is just for demonstration
    print("\nBonus: Combining concepts")
    
    @timer_decorator
    @cooldown(1)
    def optimized_lookup(player_id, iterations=1000):
        return f"Player {player_id}, Score: {slow_function(iterations)}"
    
    print(optimized_lookup(456))
    print(optimized_lookup(456))  # Should be on cooldown
    time.sleep(1.1)
    
    with LevelTimer() as t:
        print(optimized_lookup(789))

runtests()

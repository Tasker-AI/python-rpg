### Lesson - Error Handling in Python ###

# Purpose: Handle unexpected inputs and edge cases gracefully
# When to use: When user input or external data might be invalid
# Example: Validating player commands, parsing game files, network operations

### Exercise 1 ###
# Create a function that safely divides two numbers:
# 1. Takes two parameters: numerator and denominator
# 2. Returns the result of division
# 3. Handles ZeroDivisionError by returning None
# 4. Handles TypeError by returning None

def safe_divide(numerator, denominator):
    """Safely divide two numbers, handling possible errors"""
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return None
    except TypeError:
        return None
    


### Exercise 2 ###
# Create a function that loads player stats from a dictionary:
# 1. Extract name, health, and level from the player data dictionary
# 2. Use default values if fields are missing (name="Unknown", health=100, level=1)
# 3. Validate that health and level are positive numbers
# 4. If validation fails, raise ValueError with a helpful message

def load_player_stats(player_data):
    """Load and validate player statistics from a dictionary"""
    name = player_data.get("name", "Unknown")
    health = player_data.get("health", 100)
    level = player_data.get("level", 1)
    
    if health <= 0 or level <= 0:
        raise ValueError("name or level is not a positive number")
    
    return {"name": name, "health": health, "level": level}

### Exercise 3 ###
# Create a function that safely parses player commands:
# 1. Take a command string like "move north" or "attack goblin"
# 2. Split it into action and target parts
# 3. Return a tuple of (action, target)
# 4. Handle empty strings, missing parts, and other edge cases
# 5. Always return lowercase values

def parse_command(command_string):
    """Parse a player command into action and target components"""
    
    # Trim whitespace and convert to lowercase
    command_string = command_string.strip().lower()
    
    if not command_string:
        return ("", "")
    
    # Split by first space
    parts = command_string.split(" ", 1)  # Split on first space only
    
    if len(parts) == 1:
        # Only action, no target
        return (parts[0], "")
    else:
        # Both action and target
        return (parts[0], parts[1].strip())  # Also strip the target part


# Tests #
def runtests():
    # Test Exercise 1: Safe Division
    print("Test 1: Safe Division")
    
    # Normal case
    result = safe_divide(10, 2)
    print(f"10 / 2 = {result}")
    test1_1 = result == 5
    
    # Division by zero
    result = safe_divide(10, 0)
    print(f"10 / 0 = {result}")
    test1_2 = result is None
    
    # Type error
    result = safe_divide(10, "two")
    print(f"10 / 'two' = {result}")
    test1_3 = result is None
    
    print(f"Test passed: {test1_1 and test1_2 and test1_3}")
    
    # Test Exercise 2: Player Stats Loading
    print("\nTest 2: Player Stats Loading")
    
    # Complete data
    player1 = {"name": "Hero", "health": 150, "level": 5}
    try:
        stats = load_player_stats(player1)
        print(f"Valid player: {stats}")
        test2_1 = stats == {"name": "Hero", "health": 150, "level": 5}
    except Exception as e:
        print(f"Error: {e}")
        test2_1 = False
    
    # Missing data (should use defaults)
    player2 = {"name": "Rookie"}
    try:
        stats = load_player_stats(player2)
        print(f"Partial player: {stats}")
        test2_2 = stats == {"name": "Rookie", "health": 100, "level": 1}
    except Exception as e:
        print(f"Error: {e}")
        test2_2 = False
    
    # Invalid data (should raise ValueError)
    player3 = {"name": "Cheater", "health": -50, "level": 999}
    try:
        stats = load_player_stats(player3)
        print(f"Invalid player: {stats}")
        test2_3 = False
    except ValueError as e:
        print(f"Correctly rejected invalid player: {e}")
        test2_3 = True
    
    print(f"Test passed: {test2_1 and test2_2 and test2_3}")
    
    # Test Exercise 3: Command Parsing
    print("\nTest 3: Command Parsing")
    
    # Normal command
    cmd_result = parse_command("attack goblin")
    print(f"'attack goblin' -> {cmd_result}")
    test3_1 = cmd_result == ("attack", "goblin")
    
    # Single word command
    cmd_result = parse_command("inventory")
    print(f"'inventory' -> {cmd_result}")
    test3_2 = cmd_result == ("inventory", "")
    
    # Command with extra spaces
    cmd_result = parse_command("  move   north  ")
    print(f"'  move   north  ' -> {cmd_result}")
    test3_3 = cmd_result == ("move", "north")
    
    # Empty command
    cmd_result = parse_command("")
    print(f"'' -> {cmd_result}")
    test3_4 = cmd_result == ("", "")
    
    # Mixed case
    cmd_result = parse_command("Pick Up Sword")
    print(f"'Pick Up Sword' -> {cmd_result}")
    test3_5 = cmd_result == ("pick", "up sword")
    
    print(f"Test passed: {test3_1 and test3_2 and test3_3 and test3_4 and test3_5}")

runtests()

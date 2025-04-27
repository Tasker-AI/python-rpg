### Lesson: Exception Handling (try/except/finally) ###

# Purpose: Handle errors gracefully instead of crashing your program
# When to use: When operations might fail (file operations, network requests, user input)
# Example: Handling various errors in a game without ruining the player's experience

### Exercise 1 ### 
# Let's create a function to safely convert player input to an integer
# It should handle cases where the input is not a valid number
# Return the converted number or None if conversion fails

# In Python, you can catch specific exceptions:
# try:
#     result = int(some_value)
#     return result
# except ValueError:
#     return None

def safe_int_conversion(user_input):
    try:
        result = int(user_input)
        return result
    except ValueError:
        return None


### Exercise 2 ### 
# Create a function to safely divide attack_power by defense
# Return the result of attack_power / defense
# If defense is 0, return "Blocked!" instead of crashing
# If any other error occurs, return "Error calculating damage!"

# In Python, you can catch multiple exception types:
# try:
#     # Code that might raise exceptions
# except ZeroDivisionError:
#     # Handle division by zero
# except Exception:
#     # Handle any other exceptions

def calculate_attack_damage(attack_power, defense):
    try:
        result = attack_power / defense
        return result
    except ZeroDivisionError:
        return "Blocked!"
    except Exception:
        return "Error calculating damage!"


### Exercise 3 ### 
# Implement a function to load a player's inventory from a file
# If the file exists, return the items as a list
# If the file doesn't exist, create it with default items and return those
# Use finally to ensure a message is printed regardless of success/failure

# In Python, try/except/finally follows this pattern:
# try:
#     # Risky code
# except SomeException:
#     # Handle specific exception
# finally:
#     # Code that runs regardless of success/failure

def load_player_inventory(player_name):
    try:
        with open("player.txt", "r") as file:
            players = file.read(file).split(",")
            for player in players:
                if player_name in player:
                    return player
    except FileNotFoundError:
        #create new file syntax?
        with open("player.txt", "w") as file:
            file.write("default values")
            return list(file) 
    finally:
        print("always send this message")


# Tests #
def runtests():
    import os
    # Clean up any test files before starting
    if os.path.exists("test_inventory.txt"):
        os.remove("test_inventory.txt")
    
    print("\n=== Testing safe_int_conversion function ===")
    # Test with valid input
    result = safe_int_conversion("42")
    print(f"Converting '42': {result}")
    assert result == 42, f"Expected 42, got {result}"
    
    # Test with invalid input
    result = safe_int_conversion("level-up")
    print(f"Converting 'level-up': {result}")
    assert result is None, f"Expected None, got {result}"
    print("Integer conversion test passed!")
    
    print("\n=== Testing calculate_attack_damage function ===")
    # Test normal case
    result = calculate_attack_damage(100, 25)
    print(f"Attack: 100, Defense: 25, Result: {result}")
    assert result == 4, f"Expected 4, got {result}"
    
    # Test division by zero
    result = calculate_attack_damage(100, 0)
    print(f"Attack: 100, Defense: 0, Result: {result}")
    assert result == "Blocked!", f"Expected 'Blocked!', got {result}"
    
    # Test other error (try with strings)
    try:
        result = calculate_attack_damage("sword", "shield")
        print(f"Attack: 'sword', Defense: 'shield', Result: {result}")
        assert result == "Error calculating damage!", f"Expected 'Error calculating damage!', got {result}"
    except Exception as e:
        print(f"Your function didn't handle the error correctly: {e}")
        assert False, "Function should handle all errors without crashing"
    print("Damage calculation test passed!")
    
    print("\n=== Testing load_player_inventory function ===")
    # Test loading non-existent inventory (should create default)
    inventory = load_player_inventory("test_player")
    print(f"Loading non-existent inventory: {inventory}")
    assert isinstance(inventory, list), f"Expected a list, got {type(inventory)}"
    assert len(inventory) > 0, "Expected default items, got empty list"
    
    # Check that the file was created
    assert os.path.exists("test_inventory.txt"), "Inventory file wasn't created"
    
    # Test loading existing inventory
    with open("test_inventory.txt", "w") as f:
        f.write("Magic Sword,Health Potion,Dragon Scale")
    
    inventory = load_player_inventory("test_player")
    print(f"Loading existing inventory: {inventory}")
    assert "Magic Sword" in inventory, "Expected to find 'Magic Sword' in inventory"
    assert "Health Potion" in inventory, "Expected to find 'Health Potion' in inventory"
    print("Inventory loading test passed!")
    
    # Clean up test files
    if os.path.exists("test_inventory.txt"):
        os.remove("test_inventory.txt")
    
    print("\nAll tests passed! You've successfully handled exceptions.")

runtests()

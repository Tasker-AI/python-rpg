### Lesson: Writing & Importing Modules ###

# Purpose: Modules help organize code into reusable, separate files
# When to use: When your code gets too large or when functionality can be reused
# Example: Separating game components (player, enemies, items) into different files

### Exercise 1 ### 
# Let's create our first game module! 
# Create a function called create_player that takes name and class_type parameters
# It should return a dictionary with those values plus default health=100 and level=1

# In Python, you can create functions that return dictionaries like this:
# def function_name(param1, param2):
#     return {"key1": param1, "key2": param2, "key3": default_value}

def create_player(name, class_type):
    player = {}
    player["name"] = name
    player["class_type"] = class_type
    player["health"] = 100
    player["level"] = 1

    return player


### Exercise 2 ### 
# Create a function called calculate_damage that takes weapon_power and player_level
# It should return the weapon_power multiplied by (1 + player_level/10)
# This will be our basic damage formula

# In Python, you can perform calculations with parameters:
# def calculate_something(a, b):
#     return a * (1 + b/10)

def calculate_damage(weapon_power, player_level):
    damage = weapon_power * (1 + player_level/10)
    
    return damage


### Exercise 3 ### 
# Add the special if __name__ == "__main__": block
# Inside it, create a test player and print their details
# Then calculate and print damage for a weapon with power 20

# In Python, this special block runs code only when the file is executed directly:
# if __name__ == "__main__":
#     # Code here runs when the file is executed directly
#     # But not when the file is imported as a module

# Write your code here:
# Tests #
def runtests():
    print("\n=== Testing create_player function ===")
    test_player = create_player("Aragorn", "Warrior")
    expected_player = {"name": "Aragorn", "class_type": "Warrior", "health": 100, "level": 1}
    print(f"Your result: {test_player}")
    print(f"Expected: {expected_player}")
    assert test_player == expected_player, f"Player creation failed: {test_player} != {expected_player}"
    print("Player creation test passed!")
    
    print("\n=== Testing calculate_damage function ===")
    damage = calculate_damage(25, 5)
    expected_damage = 25 * (1 + 5/10)
    print(f"Your result: {damage}")
    print(f"Expected: {expected_damage}")
    assert damage == expected_damage, f"Damage calculation failed: {damage} != {expected_damage}"
    print("Damage calculation test passed!")
    
    # Testing that __name__ logic works when imported
    # This test will pass silently if your code is correct
    assert __name__ == "__main__", "This test should only run when the file is executed directly"
    print("__name__ check passed!")
    
    print("\nAll tests passed! Your module is working correctly.")

# This code only runs when the file is executed directly, not when imported
if __name__ == "__main__":
    # Create a test player and print details
    test_player = create_player("Harry", "Warrior")
    print(test_player)
    
    # Calculate and print damage
    damage = calculate_damage(20, test_player["level"])
    print(damage)
    
    # Run the tests
    runtests()

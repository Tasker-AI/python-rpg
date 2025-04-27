# This file demonstrates how to import and use modules

# To import functions from another module:
# from module_name import function1, function2

# Import the functions from our writing_importing_modules.py file:

### Exercise 1 ###
# Import the create_player and calculate_damage functions from writing_importing_modules
# Syntax: from module_name import function1, function2

# Write your import statement here:
from writing_importing_modules import create_player, calculate_damage

### Exercise 2 ###
# Create a new player using the imported create_player function
# Then create a weapon dictionary with a name and power

# Create variables like this:
# my_variable = imported_function(param1, param2)
# my_dict = {"key1": value1, "key2": value2}

# Write your code here:
player = create_player("Harry", "Monk")
weapon = {"name": "Staff", "power": 25}

### Exercise 3 ###
# Calculate and display the damage for your player and weapon
# Use a formatted string to show: "{player_name}'s {weapon_name} deals {damage} damage!"

# Format strings like this:
# print(f"{variable1}'s {variable2} deals {calculation} damage!")

# Write your code here:
damage = calculate_damage(weapon["power"], player["level"])
print(f"{player['name']}'s {weapon['name']} deals {damage} damage!")

# Tests #
def runtests():
    print("\n=== Testing module import ===")
    # Check if functions were imported correctly
    try:
        # Get the module names from the imported functions
        create_player_module = create_player.__module__
        calculate_damage_module = calculate_damage.__module__
        
        print(f"create_player imported from: {create_player_module}")
        print(f"calculate_damage imported from: {calculate_damage_module}")
        
        # Check if both functions are from the correct module
        assert "writing_importing_modules" in create_player_module, "create_player not imported from writing_importing_modules"
        assert "writing_importing_modules" in calculate_damage_module, "calculate_damage not imported from writing_importing_modules"
        
        print("Module import test passed!")
    except NameError:
        print("FAILED: Functions not correctly imported. Check your import statement.")
        return
    
    # Check if variables were defined correctly
    try:
        print("\n=== Testing player and weapon creation ===")
        # Check player dictionary
        required_keys = ["name", "class_type", "health", "level"]
        for key in required_keys:
            assert key in player, f"Player missing '{key}' key"
        
        # Check weapon dictionary
        assert "name" in weapon, "Weapon missing 'name' key"
        assert "power" in weapon, "Weapon missing 'power' key"
        assert isinstance(weapon["power"], (int, float)), "Weapon power should be a number"
        
        print(f"Player: {player}")
        print(f"Weapon: {weapon}")
        print("Player and weapon creation test passed!")
    except NameError:
        print("FAILED: Player or weapon variables not defined. Check your code.")
        return
    
    print("\nAll tests passed! You've successfully imported and used your module.")

runtests()

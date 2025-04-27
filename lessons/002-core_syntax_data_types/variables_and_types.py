"""
PYTHON BASICS: VARIABLES AND DATA TYPES
=======================================

In this lesson, we'll learn about Python variables and basic data types.
Coming from JavaScript, you'll notice some similarities and differences!

SYNTAX EXAMPLES:
---------------
# Variables in Python (no let, const, or var needed!)
player_name = "Dragonslayer"  # String
player_level = 10             # Integer
player_health = 95.5          # Float
is_game_over = False          # Boolean (note the capital F!)

# Python uses snake_case by convention, not camelCase

# Multiple assignment
x, y, z = 10, 20, 30  # Assigns 10 to x, 20 to y, and 30 to z

# Type checking
print(type(player_name))  # <class 'str'>
print(type(player_level)) # <class 'int'>
"""

# EXERCISE:
# ---------
# 1. Create variables for a game character with:
#    - A string for the character's name
#    - An integer for the character's age
#    - A float for the character's power level
#    - A boolean for whether the character has special abilities
#
# 2. Print each variable and its type
#
# Write your code below:

# Your code here
character_name = "Harry"
character_age = 29
power_level = 70.5
special_abilities = True

print(f"Name: {character_name} is of type: {type(character_name)}")
print(f"Age: {character_age} is of type: {type(character_age)}")
print(f"Power Level: {power_level} is of type: {type(power_level)}")
print(f"Special abilities: {special_abilities} is of type: {type(special_abilities)}")



# TEST CASES:
# -----------

def run_tests():
    # These tests will check if your variables exist and have the correct types
    
    # Test 1: Check if character_name exists and is a string
    try:
        if not isinstance(character_name, str):
            print("FAILED: Test 1 - character_name should be a string")
            print(f"   Actual: {type(character_name)}")
            print(f"   Expected: {type('example')}")
        else:
            print("PASSED: Test 1 - character_name is a string!")
            print(f"   Value: {character_name}")
    except NameError:
        print("FAILED: Test 1 - character_name variable not found")
    
    # Test 2: Check if character_age exists and is an integer
    try:
        if not isinstance(character_age, int):
            print("FAILED: Test 2 - character_age should be an integer")
            print(f"   Actual: {type(character_age)}")
            print(f"   Expected: {type(10)}")
        else:
            print("PASSED: Test 2 - character_age is an integer!")
            print(f"   Value: {character_age}")
    except NameError:
        print("FAILED: Test 2 - character_age variable not found")
    
    # Test 3: Check if power_level exists and is a float
    try:
        if not isinstance(power_level, float):
            print("FAILED: Test 3 - power_level should be a float")
            print(f"   Actual: {type(power_level)}")
            print(f"   Expected: {type(9000.0)}")
        else:
            print("PASSED: Test 3 - power_level is a float!")
            print(f"   Value: {power_level}")
    except NameError:
        print("FAILED: Test 3 - power_level variable not found")
    
    # Test 4: Check if special_abilities exists and is a boolean
    try:
        if not isinstance(special_abilities, bool):
            print("FAILED: Test 4 - special_abilities should be a boolean")
            print(f"   Actual: {type(special_abilities)}")
            print(f"   Expected: {type(True)}")
        else:
            print("PASSED: Test 4 - special_abilities is a boolean!")
            print(f"   Value: {special_abilities}")
    except NameError:
        print("FAILED: Test 4 - special_abilities variable not found")

# Run the tests
run_tests()

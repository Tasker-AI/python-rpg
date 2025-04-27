"""
PYTHON LISTS: THE BASICS
========================

In this lesson, we'll learn about Python lists, which are similar to arrays in JavaScript.
Lists are ordered collections that can store different types of data.

SYNTAX EXAMPLES:
---------------
# Creating lists
weapons = ["sword", "bow", "staff"]  # A list of strings
damage_values = [10, 8, 15]          # A list of integers
mixed_list = ["potion", 50, True]    # Lists can contain different data types

# Accessing list elements (zero-indexed, just like JavaScript arrays)
first_weapon = weapons[0]            # "sword"
last_weapon = weapons[-1]            # "staff" (negative indices count from the end)

# List length
inventory_count = len(weapons)       # 3

# Modifying lists
weapons.append("axe")                # Add an item to the end: ["sword", "bow", "staff", "axe"]
weapons.insert(1, "dagger")          # Insert at index 1: ["sword", "dagger", "bow", "staff", "axe"]
removed_item = weapons.pop()         # Remove and return the last item: "axe"
weapons.remove("bow")                # Remove a specific item: ["sword", "dagger", "staff"]

# Checking if an item exists in a list
has_sword = "sword" in weapons       # True - use the 'in' operator to check

# Finding the index of an item in a list
sword_index = weapons.index("sword")  # Returns 0 (the position of "sword")

# List slicing (similar to string slicing)
first_two = weapons[0:2]             # ["sword", "dagger"]
"""

# EXERCISE: You're creating an inventory system for a game. Complete the following tasks:

# 1. Create a list called 'inventory' with these items: "health potion", "map", "gold coin"
inventory = [
    "health potion",
    "map",
    "gold coin",
]

# 2. Add "dagger" to the end of the inventory
inventory.append("dagger")

# 3. Add "torch" at the beginning of the inventory
inventory.insert(0, "torch")

# 4. Replace "gold coin" with "silver coin" (Hint: First find the index of "gold coin")
inventory[inventory.index("gold coin")] = "silver coin"

# 5. Create a variable 'item_count' with the number of items in the inventory
item_count = len(inventory)

# 6. Create a variable 'has_map' that checks if "map" is in the inventory
has_map = "map" in inventory



# TEST CASES:
# -----------

def run_tests():
    # Test 1: Check if inventory exists and is a list
    try:
        if not isinstance(inventory, list):
            print("FAILED: Test 1 - inventory should be a list")
            print(f"   Actual: {type(inventory)}")
            print(f"   Expected: {type([])}")
        else:
            print("PASSED: Test 1 - inventory is a list!")
            print(f"   Value: {inventory}")
    except NameError:
        print("FAILED: Test 1 - inventory variable not found")
    
    # Test 2: Check if inventory has the correct items
    try:
        expected_items = ["torch", "health potion", "map", "silver coin", "dagger"]
        if inventory != expected_items:
            print("FAILED: Test 2 - inventory has incorrect items")
            print(f"   Actual: {inventory}")
            print(f"   Expected: {expected_items}")
        else:
            print("PASSED: Test 2 - inventory has the correct items!")
    except NameError:
        print("FAILED: Test 2 - inventory variable not found")
    
    # Test 3: Check if item_count exists and has the correct value
    try:
        expected_count = 5
        if item_count != expected_count:
            print("FAILED: Test 3 - item_count has incorrect value")
            print(f"   Actual: {item_count}")
            print(f"   Expected: {expected_count}")
        else:
            print("PASSED: Test 3 - item_count is correct!")
    except NameError:
        print("FAILED: Test 3 - item_count variable not found")
    
    # Test 4: Check if has_map exists and is a boolean with correct value
    try:
        if not isinstance(has_map, bool):
            print("FAILED: Test 4 - has_map should be a boolean")
            print(f"   Actual: {type(has_map)}")
            print(f"   Expected: {type(True)}")
        elif has_map != True:
            print("FAILED: Test 4 - has_map has incorrect value")
            print(f"   Actual: {has_map}")
            print(f"   Expected: True")
        else:
            print("PASSED: Test 4 - has_map is correct!")
    except NameError:
        print("FAILED: Test 4 - has_map variable not found")

# Run the tests
run_tests()

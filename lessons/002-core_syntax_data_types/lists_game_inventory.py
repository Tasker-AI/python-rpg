### Lesson: List Handling ###

# Purpose: Learn how to manipulate lists in Python
# When to use: When you need to store and manage collections of items in your game

### Task ###

# Step 1 To Do: Create a list called 'player_inventory' with at least 3 items
# Add a 'Map' to the inventory if it doesn't exist already
# Your inventory should have at least 3 items including a 'Map'

player_inventory = ["Gold", "Scimitar", "Helmet"]

# Now add the Map if it's not already in the inventory
if "Map" not in player_inventory:
    player_inventory.append("Map")

# Step 1 Syntax: List methods for adding and removing items
# append() - adds an item to the end of the list
# inventory.append("Health Potion")
#
# insert() - adds an item at a specific position
# inventory.insert(0, "Sword")  # Insert at beginning
#
# remove() - removes the first occurrence of a value
# inventory.remove("Health Potion")
#
# pop() - removes item at specified index and returns it
# weapon = inventory.pop(0)  # Remove first item
#
# in - check if an item exists in the list
# if "Sword" in inventory:
#     print("You have a sword!")


# Step 2 To Do: Create a sorted copy of the inventory called 'sorted_inventory'

# Create a sorted copy of player_inventory
sorted_inventory = sorted(player_inventory)

# List of items with their values
item_values = [('Magic Sword', 150), ('Shield', 75), ('Dagger', 40), ('Health Potion', 25), ('Map', 10), ('Bow', 100)]

# Find the most valuable item in item_values
item_values.sort(key=lambda item: item[1], reverse=True)
most_valuable_item = item_values[0]


# Step 2 Syntax: Sorting lists
# sort() - sorts the list in place
# inventory.sort()  # Alphabetical order
# inventory.sort(reverse=True)  # Reverse alphabetical
#
# sorted() - returns a new sorted list without modifying the original
# sorted_inventory = sorted(inventory)
#
# Custom sorting with key function
# items = [("Sword", 100), ("Shield", 85), ("Potion", 15)]
# items.sort(key=lambda item: item[1])  # Sort by the second value (price)
#
# Finding min/max values
# most_expensive = max(items, key=lambda item: item[1])


# Step 3 To Do: Create a list called 'weapons_only' containing only weapon items ('Magic Sword', 'Dagger', 'Bow')
# Create a list called 'affordable_items' containing only items that cost 50 or less

# Filter out only the weapons from item_values
weapons_only = []
for item in item_values:
    if item[0] in ["Magic Sword", "Dagger", "Bow"]:
        weapons_only.append(item[0])

# Filter out only the affordable items (50 or less) from item_values
affordable_items = []
for item in item_values:
    if item[1] <= 50:
        affordable_items.append(item)


# Step 3 Syntax: List comprehensions
# [expression for item in iterable if condition]
#
# Filter items
# weapons = [item for item in inventory if item.endswith("sword")]
#
# Transform items
# item_names = [item[0] for item in items]  # Extract first element from each tuple
#
# Combining operations
# expensive_weapons = [item for item in items if item[1] > 50 and "sword" in item[0].lower()]


# Tests #
def run_tests():
    # Test 1: Basic inventory operations
    try:
        # Check if player_inventory exists and has the right items
        if 'player_inventory' in globals():
            # Check if the required operations were performed
            if len(player_inventory) >= 3 and "Map" in player_inventory:
                print("Test 1 passed: Inventory created and modified correctly")
            else:
                print(f"Test 1 failed: Inventory doesn't have the expected items: {player_inventory}")
        else:
            print("Test 1 failed: player_inventory variable not found")
    except Exception as e:
        print(f"Test 1 error: {e}")

    # Test 2: Sorting inventory
    try:
        # Check if sorted_inventory exists
        if 'sorted_inventory' in globals():
            # Check if it's properly sorted
            expected = sorted(player_inventory)
            if sorted_inventory == expected:
                print("Test 2 passed: Inventory sorted correctly")
            else:
                print(f"Test 2 failed: Expected {expected}, got {sorted_inventory}")
                
            # Check if most_valuable_item exists
            if 'most_valuable_item' in globals():
                if most_valuable_item[0] == "Magic Sword" and most_valuable_item[1] == 150:
                    print("Test 2 passed: Found the most valuable item")
                else:
                    print(f"Test 2 failed: Expected ('Magic Sword', 150), got {most_valuable_item}")
            else:
                print("Test 2 failed: most_valuable_item variable not found")
        else:
            print("Test 2 failed: sorted_inventory variable not found")
    except Exception as e:
        print(f"Test 2 error: {e}")

    # Test 3: List comprehensions
    try:
        # Check if weapons_only exists
        if 'weapons_only' in globals():
            expected_weapons = ["Magic Sword", "Dagger", "Bow"]
            if set(weapons_only) == set(expected_weapons):  # Using set to ignore order
                print("Test 3 passed: Correctly filtered weapons")
            else:
                print(f"Test 3 failed: Expected weapons {expected_weapons}, got {weapons_only}")
                
            # Check if affordable_items exists
            if 'affordable_items' in globals():
                if len(affordable_items) >= 2 and all(item[1] <= 50 for item in affordable_items):
                    print("Test 3 passed: Correctly filtered affordable items")
                else:
                    print(f"Test 3 failed: Affordable items don't match criteria: {affordable_items}")
            else:
                print("Test 3 failed: affordable_items variable not found")
        else:
            print("Test 3 failed: weapons_only variable not found")
    except Exception as e:
        print(f"Test 3 error: {e}")

run_tests() # Tests should be uncommented by default

### Lesson Finding Substrings ###

# Purpose: Learning how to find and work with substrings in Python
# When to use: When you need to locate specific text within a larger string,
# such as parsing game dialogue, checking for keywords, or extracting information

### Task ###

# To Do: Create a function that checks if a substring exists in a string
# This function should return True if the substring is found, False otherwise

# Syntax required: 
# substring in string - checks if substring exists in string

def contains_item(inventory_description, item_name):
    
    if item_name in inventory_description:   
        return True
    else:
        return False

# To Do: Create a function that finds the position of a substring
# This function should return the index where the substring starts,
# or -1 if the substring is not found

# Syntax required:
# string.find(substring) - returns index or -1 if not found

def find_enemy_position(game_text, enemy_name):
    return game_text.find(enemy_name)


# To Do: Create a function that counts how many times a substring appears in a string
# This is useful for analyzing text or counting specific occurrences

# Syntax required:
# string.count(substring) - counts occurrences of substring

def count_damage_hits(battle_log, damage_type):
    return battle_log.count(damage_type)


# Tests #
def runtests():
    print("Testing contains_item...")
    inventory = "You are carrying: a sword, a shield, 3 health potions, and a map"
    test_cases = [
        ("sword", True),
        ("bow", False),
        ("health potion", True),
        ("gold coins", False)
    ]
    
    for item, expected in test_cases:
        result = contains_item(inventory, item)
        print(f"Inventory: '{inventory}'")
        print(f"Searching for: '{item}'")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    print("\nTesting find_enemy_position...")
    game_text = "The dragon appeared from the cave. The dragon breathed fire at you!"
    test_cases = [
        ("dragon", 4),  # "The dragon appeared..." - dragon starts at index 4
        ("cave", 29),
        ("goblin", -1),  # Not found
        ("fire", 44)
    ]
    
    for enemy, expected in test_cases:
        result = find_enemy_position(game_text, enemy)
        print(f"Game text: '{game_text}'")
        print(f"Searching for: '{enemy}'")
        print(f"Expected position: {expected}")
        print(f"Result position: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    print("\nTesting count_damage_hits...")
    battle_log = "Player hits for 10 fire damage. Monster hits for 5 physical damage. Player hits for 15 fire damage. Player misses. Monster hits for 8 physical damage."
    test_cases = [
        ("fire damage", 2),
        ("physical damage", 2),
        ("poison damage", 0),
        ("Player hits", 2)
    ]
    
    for damage_type, expected in test_cases:
        result = count_damage_hits(battle_log, damage_type)
        print(f"Battle log: '{battle_log}'")
        print(f"Counting: '{damage_type}'")
        print(f"Expected count: {expected}")
        print(f"Result count: {result}")
        print(f"Test passed: {result == expected}")
        print()

runtests() # Tests should be uncommented by default

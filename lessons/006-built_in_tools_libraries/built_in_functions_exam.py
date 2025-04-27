### Exam: Built-in Functions ###

# Task: Complete the functions below using map(), filter(), zip(), and sorted()
# based on the requirements given in the comments.

### Exercise 1: Power Up Items ###
# Requirement: You have a list of item dictionaries. Use map() to create a *new* list
# where the 'power' of each 'weapon' item is increased by 10.
# Other item types should remain unchanged.

items = [
    {'type': 'weapon', 'name': 'Sword', 'power': 50},
    {'type': 'armor', 'name': 'Shield', 'power': 0},
    {'type': 'weapon', 'name': 'Axe', 'power': 60},
    {'type': 'potion', 'name': 'Health Potion', 'power': 0},
]

def increase_weapon_power(item_dict):
    if item_dict["type"] == "weapon":
        # Return a *new* dictionary with power increased
        # The ** operator here is called dictionary unpacking. Used to avoid modifying the original dictionary.
        # {**item_dict}  creates a new dictionary that's a copy: {'type': 'weapon', 'name': 'Sword', 'power': 50}.
        return {**item_dict, 'power': item_dict['power'] + 10}
    
        # this could also be expressed as the following:
        # new_dict = dict(item_dict) # make a copy of the original
        # new_dict["power"] = new_dict["power"] + 10
        # return new_dict

    else:
        # Return the original dictionary unchanged
        return item_dict


def power_up_weapons(item_list):
    # Use map() to process the items
    # Remember map returns an iterator, convert it to a list

    return list(map(increase_weapon_power, item_list))       

powered_up_items = power_up_weapons(items)


### Exercise 2: Filter Rare Items ###
# Requirement: You have a list of item dictionaries with a 'rarity' score.
# Use filter() to create a *new* list containing only items with a rarity score of 80 or higher.

loot = [
    {'name': 'Common Sword', 'rarity': 20},
    {'name': 'Epic Shield', 'rarity': 85},
    {'name': 'Legendary Staff', 'rarity': 95},
    {'name': 'Rare Boots', 'rarity': 60},
]

def filter_rare_loot(item_list):
    # Use filter() to select rare items
    # Remember filter returns an iterator, convert it to a list
    return list(filter(lambda x: x["rarity"] >= 80, item_list))

rare_items = filter_rare_loot(loot)


### Exercise 3: Combine Player Stats ###
# Requirement: You have three lists: player names, their levels, and their scores.
# Use zip() to combine these lists into a list of tuples, where each tuple contains
# (name, level, score) for a player.

names = ['Hero', 'Wizard', 'Rogue']
levels = [10, 12, 9]
scores = [5000, 6200, 4800]

def combine_stats(names_list, levels_list, scores_list):
    # Use zip() to combine the lists
    # Remember zip returns an iterator, convert it to a list
    return list(zip(names_list, levels_list, scores_list))

player_stats = combine_stats(names, levels, scores)


### Exercise 4: Sort Players by Score ###
# Requirement: You have the list of player dictionaries created in Exercise 1 (powered_up_items).
# However, for this exercise, let's use a predefined list of players with scores.
# Sort this list of player dictionaries by 'score' in *descending* order (highest score first).

players_with_scores = [
    {'name': 'Alice', 'score': 1500, 'level': 15},
    {'name': 'Bob', 'score': 2200, 'level': 10},
    {'name': 'Charlie', 'score': 1800, 'level': 20}
]

def sort_by_score(player_list):
    # Use sorted() with a key and reverse parameter
    return sorted(player_list, key=lambda x: x["score"], reverse=True)

sorted_players = sort_by_score(players_with_scores)


# Tests #
def run_tests():
    global powered_up_items, rare_items, player_stats, sorted_players # Allow tests to modify global vars if needed for setup

    # Assign results from functions for testing
    # Handle potential None returns from placeholder 'pass' functions gracefully
    try:
        powered_up_items = power_up_weapons(items)
    except Exception as e:
        print(f"Error calling power_up_weapons: {e}")
        powered_up_items = []
    try:
        rare_items = filter_rare_loot(loot)
    except Exception as e:
        print(f"Error calling filter_rare_loot: {e}")
        rare_items = []
    try:
        player_stats = combine_stats(names, levels, scores)
    except Exception as e:
        print(f"Error calling combine_stats: {e}")
        player_stats = []
    try:
        sorted_players = sort_by_score(players_with_scores)
    except Exception as e:
        print(f"Error calling sort_by_score: {e}")
        sorted_players = []

    print("Running Exam Tests...\n")

    # Test Exercise 1
    expected_powered_up = [
        {'type': 'weapon', 'name': 'Sword', 'power': 60},
        {'type': 'armor', 'name': 'Shield', 'power': 0},
        {'type': 'weapon', 'name': 'Axe', 'power': 70},
        {'type': 'potion', 'name': 'Health Potion', 'power': 0},
    ]
    print("--- Testing Exercise 1: Power Up Items (map) ---")
    if powered_up_items == expected_powered_up:
        print("Exercise 1: Passed")
    else:
        print(f"Exercise 1: Failed")
        print(f"  Expected: {expected_powered_up}")
        print(f"  Got:      {powered_up_items}")
    print("-" * 20)

    # Test Exercise 2
    expected_rare = [
        {'name': 'Epic Shield', 'rarity': 85},
        {'name': 'Legendary Staff', 'rarity': 95},
    ]
    print("--- Testing Exercise 2: Filter Rare Items (filter) ---")
    if rare_items == expected_rare:
        print("Exercise 2: Passed")
    else:
        print(f"Exercise 2: Failed")
        print(f"  Expected: {expected_rare}")
        print(f"  Got:      {rare_items}")
    print("-" * 20)

    # Test Exercise 3
    expected_stats = [('Hero', 10, 5000), ('Wizard', 12, 6200), ('Rogue', 9, 4800)]
    print("--- Testing Exercise 3: Combine Player Stats (zip) ---")
    if player_stats == expected_stats:
        print("Exercise 3: Passed")
    else:
        print(f"Exercise 3: Failed")
        print(f"  Expected: {expected_stats}")
        print(f"  Got:      {player_stats}")
    print("-" * 20)

    # Test Exercise 4
    expected_sorted_players = [
        {'name': 'Bob', 'score': 2200, 'level': 10},
        {'name': 'Charlie', 'score': 1800, 'level': 20},
        {'name': 'Alice', 'score': 1500, 'level': 15}
    ]
    print("--- Testing Exercise 4: Sort Players by Score (sorted) ---")
    if sorted_players == expected_sorted_players:
        print("Exercise 4: Passed")
    else:
        print(f"Exercise 4: Failed")
        print(f"  Expected: {expected_sorted_players}")
        print(f"  Got:      {sorted_players}")
    print("-" * 20)

    print("\nExam Tests Finished.")

# Make sure to call the test function!
run_tests()

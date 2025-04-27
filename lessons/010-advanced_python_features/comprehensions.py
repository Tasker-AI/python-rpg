### Lesson - List Comprehensions and Advanced Comprehensions ###

# Purpose: Comprehensions allow you to create lists, dictionaries, and sets concisely
# When to use: When transforming or filtering data collections in your game
# Example: Creating item lists, filtering enemies, or generating game levels

### Exercise 1 ###
# Create a function that uses a list comprehension to:
# 1. Take a list of item names
# 2. Return a new list with "Legendary " added to each item name
# 3. Only include items with names longer than 3 characters

# Standard loop approach:
# def mark_legendary_items(items):
#     legendary_items = []
#     for item in items:
#         if len(item) > 3:
#             legendary_items.append("Legendary " + item)
#     return legendary_items

# List comprehension approach:
# [expression for item in iterable if condition]

from operator import itemgetter


def mark_legendary_items(items):
    return ["Legendary " + item for item in items if len(item) >= 3]


### Exercise 2 ###
# Create a function that uses a dictionary comprehension to:
# 1. Take a list of item names
# 2. Create a dictionary where keys are item names and values are item lengths
# 3. Only include items with lengths between 4 and 10 characters

# Dictionary comprehension syntax:
# {key_expr: value_expr for item in iterable if condition}

def create_item_length_dict(items):
    return {item: len(item) for item in items if 3 <= len(item) <= 10}


### Exercise 3 ###
# Create a function that uses nested comprehensions to:
# 1. Take a list of players where each player is [name, level, [items]]
# 2. Return a list of all items owned by players above level 10
# 3. Avoid duplicate items in the result

# Example data:
# players = [
#    ["Alex", 12, ["Sword", "Shield", "Potion"]],
#    ["Jess", 8, ["Dagger", "Potion"]],
#    ["Sam", 15, ["Sword", "Wand", "Potion"]]
# ]

    # item_list = []
    # for name, level, items in players:
    #     if level >= 10:
    #         for item in items:
    #             if item not in item_list:
    #                 item_list.append(item)
    # return [item for item in item_list]

def get_high_level_player_items(players):
    return list({
        item
        for name, level, items in players
        if level >= 10
        for item in items        
    })


# Tests #
def runtests():
    # Test Exercise 1: List comprehension
    items = ["Sword", "Axe", "Map", "Legendary Bow", "Key", "Gem", "Hi"]
    legendary_items = mark_legendary_items(items)
    
    print("Test 1: List comprehension")
    print(f"Original items: {items}")
    print(f"Legendary items: {legendary_items}")
    expected_items = ["Legendary Sword", "Legendary Axe", "Legendary Map", 
                      "Legendary Legendary Bow", "Legendary Key", "Legendary Gem"]
    list_comp_test = all(item in legendary_items for item in expected_items) and len(legendary_items) == len(expected_items)
    print(f"Test passed: {list_comp_test}")
    
    # Test Exercise 2: Dictionary comprehension
    items = ["Sword", "Axe", "Map", "Bow", "Key", "Gem", "Amulet", "Staff", "SuperRareItem"]
    item_lengths = create_item_length_dict(items)
    
    print("\nTest 2: Dictionary comprehension")
    print(f"Item lengths: {item_lengths}")
    expected_dict = {"Sword": 5, "Axe": 3, "Map": 3, "Bow": 3, "Key": 3, "Gem": 3, "Amulet": 6, "Staff": 5}
    dict_comp_test = (item_lengths == {k: len(k) for k in items if 3 <= len(k) <= 10})
    print(f"Test passed: {dict_comp_test}")
    
    # Test Exercise 3: Nested comprehension
    players = [
        ["Alex", 12, ["Sword", "Shield", "Potion"]],
        ["Jess", 8, ["Dagger", "Potion"]],
        ["Sam", 15, ["Sword", "Wand", "Potion"]]
    ]
    high_level_items = get_high_level_player_items(players)
    
    print("\nTest 3: Nested comprehension")
    print(f"High level player items: {high_level_items}")
    expected_items = ["Sword", "Shield", "Potion", "Wand"]
    nested_test = sorted(high_level_items) == sorted(expected_items)
    print(f"Test passed: {nested_test}")
    
    # Performance comparison
    import time
    
    # Create a large list for testing
    large_items = ["Item" + str(i) for i in range(10000)]
    
    # Standard loop approach
    start = time.time()
    result_loop = []
    for item in large_items:
        if len(item) > 5:
            result_loop.append(item.upper())
    loop_time = (time.time() - start) * 1000
    
    # Comprehension approach
    start = time.time()
    result_comp = [item.upper() for item in large_items if len(item) > 5]
    comp_time = (time.time() - start) * 1000
    
    print("\nPerformance Comparison:")
    print(f"Standard loop time: {loop_time:.2f} ms")
    print(f"List comprehension time: {comp_time:.2f} ms")
    print(f"Comprehension is {loop_time/comp_time:.2f}x faster")
    print(f"Both approaches give same result: {result_loop == result_comp}")

runtests()

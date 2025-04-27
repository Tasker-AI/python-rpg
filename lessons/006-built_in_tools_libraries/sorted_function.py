### Lesson sorted() ###

# Purpose: The sorted() function returns a *new* sorted list from the items in an iterable (like lists, tuples, dictionaries, etc.).
# It does *not* modify the original iterable. This is different from the list's .sort() method, which sorts the list in-place.

# When to use it:
# - When you need a sorted sequence but want to keep the original sequence unchanged.
# - When you need to sort iterables that are not lists (e.g., tuples, strings, dictionary keys/values).
# - When you need custom sorting logic using the 'key' or 'reverse' parameters.

# Example Use Case: Sorting a list of player high scores from highest to lowest, or sorting inventory items alphabetically.


### Exercise 1: Simple Ascending Sort ###
# Task: You have a list of game scores. Use sorted() to create a *new* list with the scores sorted from lowest to highest.
# Syntax: new_list = sorted(iterable)

scores = [150, 85, 200, 10, 120]
sorted_scores = sorted(scores)

### Exercise 2: Sorting Strings ###
# Task: You have a list of player names. Sort them alphabetically.
# Syntax: new_list = sorted(iterable)

player_names = ["Zelda", "Mario", "Link", "Sonic"]
sorted_names = sorted(player_names)

### Exercise 3: Descending Sort ###
# Task: Sort the game scores from *highest* to lowest.
# Hint: Use the 'reverse' parameter.
# Syntax: new_list = sorted(iterable, reverse=True)

scores_desc = [150, 85, 200, 10, 120] # Use a different variable name to avoid conflict with Ex1
sorted_scores_descending = sorted(scores_desc, reverse=True)

### Exercise 4: Sorting Tuples with a Key ###
# Task: You have a list of inventory items represented as tuples (item_name, item_value).
# Sort the items based on their *value* (the second element of the tuple) in ascending order.
# Hint: Use the 'key' parameter with a lambda function to specify which part of the tuple to sort by.
# Syntax: new_list = sorted(iterable, key=lambda x: x[index_to_sort_by])

inventory = [('potion', 50), ('sword', 500), ('shield', 250), ('gold coin', 10)]
sorted_inventory_by_value = sorted(inventory, key=lambda x: x[1])

### Exercise 5: Sorting Dictionaries with a Key ###
# Task: You have a list of player dictionaries. Sort the players based on their 'level' in ascending order.
# Hint: Use the 'key' parameter with a lambda function to access the dictionary value.
# Syntax: new_list = sorted(iterable, key=lambda d: d['key_to_sort_by'])

players = [
    {'name': 'Alice', 'level': 15},
    {'name': 'Bob', 'level': 10},
    {'name': 'Charlie', 'level': 20}
]
sorted_players_by_level = sorted(players, key=lambda x: x["level"])


# Tests #
def run_tests():
    print("Running Tests...\n")

    # Test Exercise 1
    # Redefine scores inside the test to ensure it uses the original intended list for testing
    original_scores_ex1 = [150, 85, 200, 10, 120]
    expected_scores = [10, 85, 120, 150, 200]
    if sorted_scores == expected_scores:
        print("Exercise 1: Passed - Scores sorted correctly (ascending).")
    else:
        print(f"Exercise 1: Failed - Expected {expected_scores}, but got {sorted_scores}")

    # Verify original list (defined outside tests) is unchanged
    # Use the initial 'scores' variable defined globally for Exercise 1
    global scores
    if scores == original_scores_ex1:
         print("Exercise 1: Passed - Original 'scores' list unchanged.")
    else:
        print(f"Exercise 1: Failed - Original 'scores' list was modified: {scores}")
    print("-" * 20)

    # Test Exercise 2
    expected_names = ['Link', 'Mario', 'Sonic', 'Zelda']
    if sorted_names == expected_names:
        print("Exercise 2: Passed - Names sorted alphabetically.")
    else:
        print(f"Exercise 2: Failed - Expected {expected_names}, but got {sorted_names}")
    print("-" * 20)

    # Test Exercise 3
    # Use the separate scores_desc variable defined for Exercise 3
    expected_scores_desc = [200, 150, 120, 85, 10]
    if sorted_scores_descending == expected_scores_desc:
        print("Exercise 3: Passed - Scores sorted correctly (descending).")
    else:
        print(f"Exercise 3: Failed - Expected {expected_scores_desc}, but got {sorted_scores_descending}")
    print("-" * 20)

    # Test Exercise 4
    expected_inventory = [('gold coin', 10), ('potion', 50), ('shield', 250), ('sword', 500)]
    if sorted_inventory_by_value == expected_inventory:
        print("Exercise 4: Passed - Inventory sorted correctly by value.")
    else:
        print(f"Exercise 4: Failed - Expected {expected_inventory}, but got {sorted_inventory_by_value}")
    print("-" * 20)

    # Test Exercise 5
    expected_players = [
        {'name': 'Bob', 'level': 10},
        {'name': 'Alice', 'level': 15},
        {'name': 'Charlie', 'level': 20}
    ]
    if sorted_players_by_level == expected_players:
        print("Exercise 5: Passed - Players sorted correctly by level.")
    else:
        print(f"Exercise 5: Failed - Expected {expected_players}, but got {sorted_players_by_level}")
    print("-" * 20)

    print("\nTests Finished.")

run_tests()

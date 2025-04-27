### Lesson: random Library ###

# Purpose: The `random` library provides functions for generating pseudo-random numbers
# and making random choices, which is crucial for games to add elements of chance and variability.

# When to use it:
# - Simulating dice rolls or coin flips.
# - Choosing a random item from a list (e.g., loot drop, enemy type).
# - Shuffling a sequence (e.g., card deck, turn order).
# - Generating random events or probabilities (e.g., chance of critical hit).

# Example Use Case: Deciding which monster appears, determining if an attack is a critical hit,
# randomly picking a starting player, or shuffling item rewards.

# Note: Like 'math', you need to import the 'random' library first.
# import random

import random # Import the library for the exercises

### Exercise 1: Random Loot Drop ###
# Task: You have a list of possible loot items. Use `random.choice()` to select
# one item randomly from the list to simulate a monster drop.
# Syntax: random.choice(sequence) # sequence can be a list, tuple, etc.

possible_loot = ['Gold Coins', 'Health Potion', 'Rusty Sword', 'Leather Armor']
dropped_item = random.choice(possible_loot)


### Exercise 2: Dice Roll Simulation ###
# Task: Simulate rolling a standard six-sided die (D6). Use `random.randint()`
# to generate a random integer between 1 and 6 (inclusive).
# Syntax: random.randint(a, b) # Returns a random integer N such that a <= N <= b.

die_roll = random.randint(1, 6)


### Exercise 3: Shuffling Player Turn Order ###
# Task: You have a list representing the initial turn order of players.
# Use `random.shuffle()` to shuffle this list *in-place* to randomize the turn order.
# Note: `random.shuffle()` modifies the original list directly and returns `None`.
# Syntax: random.shuffle(sequence)

initial_turn_order = ['Hero', 'Wizard', 'Rogue', 'Cleric']
random.shuffle(initial_turn_order)
# The variable initial_turn_order itself will be modified.


# Tests #
# Note: Because these tests involve randomness, we can't check for exact values.
# Instead, we check if the results are of the expected type and within the expected range/set.

def run_tests():
    print("Running Tests...\n")
    global dropped_item, die_roll, initial_turn_order # Allow tests to access these variables

    # Re-run random functions within tests if needed for validation
    # For simplicity here, we'll just check the state after the user's code runs.

    # Test Exercise 1
    print("--- Testing Exercise 1: Random Loot Drop ---")
    is_valid_loot = dropped_item in possible_loot
    print(f"Dropped item: {dropped_item}")
    if is_valid_loot:
        print("Exercise 1: Passed (Item is one of the possible loot items)")
    else:
        print(f"Exercise 1: Failed - '{dropped_item}' is not in the possible_loot list: {possible_loot}")
    print("-" * 20)

    # Test Exercise 2
    print("--- Testing Exercise 2: Dice Roll Simulation ---")
    is_valid_roll = 1 <= die_roll <= 6
    print(f"Die roll: {die_roll}")
    if isinstance(die_roll, int) and is_valid_roll:
        print("Exercise 2: Passed (Roll is an integer between 1 and 6)")
    elif not isinstance(die_roll, int):
         print(f"Exercise 2: Failed - Roll should be an integer, but got type {type(die_roll)}")
    else:
        print(f"Exercise 2: Failed - Roll {die_roll} is outside the valid range [1, 6]")
    print("-" * 20)

    # Test Exercise 3
    print("--- Testing Exercise 3: Shuffling Player Turn Order ---")
    original_order = ['Hero', 'Wizard', 'Rogue', 'Cleric']
    # Check if the list has the same elements (just possibly different order)
    has_same_elements = sorted(initial_turn_order) == sorted(original_order)
    # Check if the list was actually modified (it's *possible* shuffle results in the same order, but unlikely)
    was_shuffled = initial_turn_order != original_order # This is not a perfect test, but good enough
    print(f"Shuffled order: {initial_turn_order}")
    if isinstance(initial_turn_order, list) and len(initial_turn_order) == len(original_order) and has_same_elements:
        print("Exercise 3: Passed (List contains the correct players and seems shuffled)")
        if not was_shuffled:
            print("(Note: Shuffled order happened to be the same as the original - re-run if unsure)")
    elif not isinstance(initial_turn_order, list):
         print(f"Exercise 3: Failed - Expected a list, but got type {type(initial_turn_order)}")
    elif len(initial_turn_order) != len(original_order):
         print(f"Exercise 3: Failed - List length changed from {len(original_order)} to {len(initial_turn_order)}")
    else:
        print(f"Exercise 3: Failed - List elements changed. Expected elements derived from {original_order}, got {initial_turn_order}")
    print("-" * 20)

    print("\nTests Finished.")

# IMPORTANT: Call the shuffle function here *before* running tests
# because random.shuffle() modifies the list in place.
# If you don't call it here, the test will run on the un-shuffled list.
random.shuffle(initial_turn_order)
run_tests()

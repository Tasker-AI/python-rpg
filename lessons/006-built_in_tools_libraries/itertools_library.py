### Lesson: itertools Library (chain, product) ###

# Purpose: The `itertools` library provides functions for creating and working
# with iterators in a memory-efficient way.
# - `chain`: Treats consecutive sequences as a single sequence.
# - `product`: Computes the Cartesian product of input iterables.

# When to use it:
# - `chain`: Processing items from multiple sources (e.g., player inventory + stash)
#   as if they were one list, without actually merging them first.
# - `product`: Generating all possible combinations (e.g., all pairs of players for a duel,
#   all possible equipment combinations, all coordinates on a grid).

# Example Use Case:
# - `chain`: Loop through all weapons a player has, whether in their backpack or weapon rack.
# - `product`: Generate all possible (attacker, defender) pairs from two lists of characters.

# Note: You need to import the specific functions from the itertools library.
# from itertools import chain, product

from itertools import chain, product
import itertools # Import for exercises

### Exercise 1: Combining Inventories ###
# Task: A player has items in their backpack and in a storage chest.
# Use `itertools.chain()` to create a single iterator that yields items from
# the backpack first, then from the chest. Convert the result to a list to see all items.
# Syntax: combined_iterator = chain(iterable1, iterable2, ...)
#         combined_list = list(combined_iterator)

backpack = ['sword', 'potion', 'shield']
chest = ['gold', 'gem', 'potion', 'armor']

combined_items_iterator = itertools.chain(backpack, chest) # Assign the result of chain() here
all_items_list = list(combined_items_iterator) # Convert the iterator to a list here


### Exercise 2: Generating Attack Pairings ###
# Task: You have a list of attacking monsters and defending heroes.
# Use `itertools.product()` to generate all possible (attacker, defender) pairs.
# The result will be an iterator yielding tuples. Convert it to a list to view all pairs.
# Syntax: pairings_iterator = product(iterable1, iterable2, ...)
#         pairings_list = list(pairings_iterator)

attackers = ['Goblin', 'Orc']
defenders = ['Hero', 'Wizard', 'Cleric']

pairing_iterator = itertools.product(attackers, defenders)
all_pairings_list = list(pairing_iterator) # Convert the iterator to a list here
print(all_pairings_list)


# Tests #
def run_tests():
    print("Running Tests...\n")
    global all_items_list, all_pairings_list # Allow tests access

    # Test Exercise 1
    print("--- Testing Exercise 1: chain ---")
    expected_items = ['sword', 'potion', 'shield', 'gold', 'gem', 'potion', 'armor']
    if all_items_list == expected_items:
        print("Exercise 1: Passed")
    else:
        print(f"Exercise 1: Failed - Item list mismatch.")
        print(f"  Expected: {expected_items}")
        print(f"  Got:      {all_items_list}")
    print("-" * 20)

    # Test Exercise 2
    print("--- Testing Exercise 2: product ---")
    expected_pairings = [
        ('Goblin', 'Hero'), ('Goblin', 'Wizard'), ('Goblin', 'Cleric'),
        ('Orc', 'Hero'), ('Orc', 'Wizard'), ('Orc', 'Cleric')
    ]
    # Sort both lists before comparing to handle potential order differences if user implementation varies
    if sorted(all_pairings_list) == sorted(expected_pairings):
        print("Exercise 2: Passed")
    else:
        print(f"Exercise 2: Failed - Pairing list mismatch.")
        print(f"  Expected (order may vary): {expected_pairings}")
        print(f"  Got:                       {all_pairings_list}")
    print("-" * 20)

    print("\nTests Finished.")

# Run tests after user code block
run_tests()

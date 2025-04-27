### Lesson: Hashmaps (Python Dictionaries) ###     

# Purpose: To conceptually understand Hashmaps (Hash Tables) and recognize
# Python's `dict` as their implementation. Focus on *why* they are fast
# and when to use them.

# Key Concepts Recap:
# - Stores data as Key-Value pairs.
# - Uses a hash function to quickly locate where values are stored based on their keys.
# - Provides very fast average time complexity for:
#   - Insertion: `my_dict[key] = value`   (Average O(1))
#   - Deletion: `del my_dict[key]`        (Average O(1))
#   - Lookup: `value = my_dict[key]`    (Average O(1))
# - Keys must be "hashable" (immutable types like strings, numbers, tuples usually work).

# Contrast with Lists/Linked Lists:
# - Finding an item in a list/linked list requires checking items one by one (O(n)).
# - Hashmaps/Dictionaries jump (almost) directly to the item via the key (Average O(1)).

# Python's `dict` *is* a highly optimized hashmap implementation.

### Exercise 1: Use Case Identification ###
# Task: Consider storing game character stats (health, mana, strength).
# Which data structure is generally best for quickly accessing a specific stat
# (e.g., 'health') by its name? List, Tuple, Set, or Dictionary (Hashmap)?
# Assign your answer (the type name as a string) to the variable below.

best_structure_for_stats = "Dictionary" # e.g., "List", "Dictionary", etc.


### Exercise 2: Performance Thought ###
# Task: Imagine you have a HUGE list of 1 million monster names, and a dictionary
# mapping each monster name (key) to its description (value).
# Which operation would likely be significantly faster:
# A) Finding the description for 'Goblin' in the dictionary.
# B) Searching the list to see if 'Goblin' is present.
# Assign 'A' or 'B' to the variable below.

faster_operation = "A" # 'A' or 'B'


# Tests #
def run_tests():
    print("Running Hashmap Concept Tests...\n")
    global best_structure_for_stats, faster_operation
    passed_count = 0
    total_tests = 2

    # Test Exercise 1
    print("--- Testing Exercise 1: Use Case ---")
    correct_structure = "Dictionary" # Or "dict" is acceptable too maybe? Let's stick to general term
    if best_structure_for_stats.strip().capitalize() == correct_structure:
        print("Exercise 1: Passed (Dictionary/Hashmap is ideal for key-based lookup)")
        passed_count += 1
    else:
        print(f"Exercise 1: Failed - Re-think which structure uses keys for direct access.")
        print(f"  Expected something like: {correct_structure}")
        print(f"  Got:                     {best_structure_for_stats}")
    print("-" * 20)

    # Test Exercise 2
    print("--- Testing Exercise 2: Performance ---")
    correct_operation = 'A'
    if faster_operation.strip().upper() == correct_operation:
        print("Exercise 2: Passed (Dictionary lookup is much faster on average than list search)")
        passed_count += 1
    else:
        print(f"Exercise 2: Failed - Recall the average time complexity difference.")
        print(f"  Expected: {correct_operation}")
        print(f"  Got:      {faster_operation}")
    print("-" * 20)

    print(f"\nTests Finished. Passed {passed_count}/{total_tests}.")

# Run tests
run_tests()

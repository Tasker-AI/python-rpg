### Lesson: Stacks (using Lists) ###

# Purpose: To understand and implement the Stack data structure (LIFO - Last-In, First-Out)
# using Python lists. Stacks are fundamental for managing sequential operations like
# undo history or processing nested structures.

# When to use it:
# - Managing undo/redo functionality.
# - Reversing sequences of items.
# - Parsing expressions (like matching parentheses).
# - Tracking function calls (the call stack).

# How Python lists simulate a Stack:
# - `append()`: Adds an item to the end (top) of the list (push).
# - `pop()`: Removes and returns the item from the end (top) of the list (pop).
# - Accessing `my_list[-1]`: Views the item at the end (top) without removing it (peek).

### Exercise 1: Push items onto the Stack ###
# Task: Simulate adding spells to a spell-casting sequence stack.
# Start with an empty list `spell_stack`. Push 'Fireball', then 'Ice Shard', then 'Heal'.
# Syntax: stack_list.append(item)

spell_stack = []
# Push 'Fireball'
spell_stack.append("Fireball")
# Push 'Ice Shard'
spell_stack.append("Ice Shard")
# Push 'Heal'
spell_stack.append("Heal")


### Exercise 2: Pop items from the Stack ###
# Task: Simulate casting (removing) the last spell added.
# Pop one spell from the `spell_stack` created in Exercise 1. Store the popped spell
# in a variable `last_cast_spell`.
# Syntax: popped_item = stack_list.pop()

last_cast_spell = spell_stack.pop()


### Exercise 3: Peek at the top item ###
# Task: See which spell is currently at the top of the stack without casting it.
# Access the last element of the `spell_stack` (after the pop in Exercise 2) and
# store it in `next_spell_to_cast`. Check if the stack is empty first!
# Syntax: if stack_list: top_item = stack_list[-1]

next_spell_to_cast = spell_stack[-1] # Peek at spell_stack[-1] if not empty


# Tests #
def run_tests():
    print("Running Stack Tests...\n")
    # Note: These tests assume exercises are run sequentially and modify the same stack
    global spell_stack, last_cast_spell, next_spell_to_cast

    # Test Exercise 1 Results (before pop)
    print("--- Testing Exercise 1: Push ---")
    # Reconstruct expected stack after pushes
    expected_stack_after_push = ['Fireball', 'Ice Shard', 'Heal']
    # We need to check the state *after* the pushes but *before* the pop
    # A bit tricky as the variables are global. We infer the state.
    current_stack_before_pop = spell_stack + ([last_cast_spell] if last_cast_spell is not None else [])

    if current_stack_before_pop == expected_stack_after_push:
        print("Exercise 1: Passed (Stack after pushes seems correct)")
    else:
        # This check might be inaccurate if Ex2/Ex3 were attempted incorrectly before Ex1 was right
        print(f"Exercise 1: Failed - Stack state after pushes is unexpected.")
        print(f"  Expected after pushes: {expected_stack_after_push}")
        print(f"  Inferred state based on current stack and popped item: {current_stack_before_pop}")
        print(f"  (Current stack is: {spell_stack}, Last popped was: {last_cast_spell})")
    print("-" * 20)


    # Test Exercise 2 Results
    print("--- Testing Exercise 2: Pop ---")
    expected_popped_item = 'Heal'
    if last_cast_spell == expected_popped_item:
        print("Exercise 2: Passed")
    else:
        print(f"Exercise 2: Failed - Popped item mismatch.")
        print(f"  Expected popped: {expected_popped_item}")
        print(f"  Got:             {last_cast_spell}")
    print("-" * 20)

    # Test Exercise 3 Results
    print("--- Testing Exercise 3: Peek ---")
    expected_stack_after_pop = ['Fireball', 'Ice Shard']
    expected_peek_item = 'Ice Shard' # Top item after 'Heal' was popped

    if spell_stack != expected_stack_after_pop:
         print(f"Exercise 3: Failed - Stack state after pop is incorrect.")
         print(f"  Expected stack: {expected_stack_after_pop}")
         print(f"  Current stack:  {spell_stack}")
    elif not spell_stack: # Check if stack became unexpectedly empty
        print(f"Exercise 3: Failed - Stack is empty, cannot peek.")
    elif next_spell_to_cast == expected_peek_item:
        print("Exercise 3: Passed")
    else:
        print(f"Exercise 3: Failed - Peek item mismatch.")
        print(f"  Expected peek: {expected_peek_item}")
        print(f"  Got:           {next_spell_to_cast}")
    print("-" * 20)

    print("\nTests Finished.")

# Run tests
run_tests()

### Lesson: Type Conversion & Introspection ###

# Purpose: Learn how to convert data between different types (e.g., string to integer) 
#          and how to inspect variables to understand their type and capabilities.
# When to use:
# Type Conversion: Handling user input (often comes as string), preparing data for calculations, changing data structures.
# Introspection: Debugging, understanding unfamiliar objects, exploring module contents.
# Example use cases:
# - Converting player's typed score (string) into a number (int) to save it.
# - Checking if an item is a 'weapon' (string) or 'armor' (string) before equipping.
# - Finding out what methods are available for a list variable using dir().


### Exercise 1: String to Integer ###
# Task: A player enters their level as text. Convert the `level_text` string to an integer 
#       and store it in `level_number`.
# Syntax: integer_variable = int(string_variable)

level_text = "50"
level_number = int(level_text) 
# Convert level_text to an integer below


### Exercise 2: Number to String ###
# Task: Prepare a message displaying the player's gold. Convert the `gold_amount` integer 
#       to a string and store it in `gold_message`.
# Syntax: string_variable = str(numeric_variable)

gold_amount = 1500
gold_message = str(gold_amount)
# Convert gold_amount to a string below


### Exercise 3: Checking Type with `type()` ###
# Task: We received `mystery_item`. Check its data type and store the type object 
#       (not the type name as a string) in `item_type`.
# Syntax: type_object = type(variable)

mystery_item = ['Sword', 'Shield'] # This could be anything in a real scenario!
item_type = type(mystery_item)
# Get the type of mystery_item below


### Exercise 4: Using `bool()` Conversion ###
# Task: Determine if the player's `inventory` list is empty or not using boolean conversion. 
#       Store the result (True if not empty, False if empty) in `has_items`.
#       Hint: Non-empty sequences (lists, strings, tuples, dicts) evaluate to True.
# Syntax: boolean_result = bool(variable_to_check)

inventory = [] # Could be ['potion', 'coin'] or empty
has_items = bool(inventory)
# Convert inventory to a boolean below


### Exercise 5: Exploring with `dir()` (Conceptual) ###
# Task: This is a thought exercise - no code needed here, but understand the concept.
#       Imagine you have a list variable `player_skills = ['Archery', 'Stealth']`.
#       How would you find out what methods (like append, sort, pop) you can use with this list?
# Concept: `dir(player_skills)` would return a list of all attributes and methods available for that list object.
#          This is useful for exploration in the REPL or debugging.

# No code needed for this exercise, just understand the purpose of dir().


# --- Tests --- #
def run_tests():
    print("Running Type Conversion & Introspection Tests...")
    passed_tests = 0
    total_tests = 4 # Exercise 5 is conceptual

    # Test Exercise 1
    try:
        # Explicitly call the conversion within the try block
        # Assuming level_number is assigned by the user
        if 'level_number' in globals() and level_number == 50 and isinstance(level_number, int):
            print("Exercise 1: Passed - String '50' correctly converted to integer 50.")
            passed_tests += 1
        elif 'level_number' not in globals():
             print("Exercise 1: Failed - Variable 'level_number' not assigned.")
        elif not isinstance(level_number, int):
             print(f"Exercise 1: Failed - level_number is not an integer. Type: {type(level_number)}")
        else:
             print(f"Exercise 1: Failed - Incorrect integer value.")
             print(f"  Expected: 50")
             print(f"  Got:      {level_number}")
    except Exception as e:
        print(f"Exercise 1: Failed with error - {e}")
        
    # Test Exercise 2
    try:
        # Assuming gold_message is assigned by the user
        if 'gold_message' in globals() and gold_message == "1500" and isinstance(gold_message, str):
            print("Exercise 2: Passed - Integer 1500 correctly converted to string '1500'.")
            passed_tests += 1
        elif 'gold_message' not in globals():
             print("Exercise 2: Failed - Variable 'gold_message' not assigned.")
        elif not isinstance(gold_message, str):
             print(f"Exercise 2: Failed - gold_message is not a string. Type: {type(gold_message)}")
        else:
            print(f"Exercise 2: Failed - Incorrect string value.")
            print(f"  Expected: '1500'")
            print(f"  Got:      '{gold_message}'")
    except Exception as e:
        print(f"Exercise 2: Failed with error - {e}")

    # Test Exercise 3
    try:
        # Assuming item_type is assigned by the user
        expected_type = type(mystery_item)
        if 'item_type' in globals() and item_type is expected_type:
            print(f"Exercise 3: Passed - Correct type ({expected_type.__name__}) identified for mystery_item.")
            passed_tests += 1
        elif 'item_type' not in globals():
             print("Exercise 3: Failed - Variable 'item_type' not assigned.")
        else:
            print(f"Exercise 3: Failed - Incorrect type identified.")
            print(f"  Expected type object for: {mystery_item}")
            print(f"  Got type object:          {item_type}")
    except Exception as e:
         print(f"Exercise 3: Failed with error - {e}")
        
    # Test Exercise 4
    try:
        # Test with both empty and non-empty list possibilities
        # Test 1: Empty list
        inventory_test = []
        has_items_test_empty = bool(inventory_test)
        # Test 2: Non-empty list
        inventory_test = ['potion']
        has_items_test_nonempty = bool(inventory_test)
        
        # Check the user's assignment based on the initial empty inventory
        expected_bool = False # For the initial empty inventory = []
        if 'has_items' in globals() and has_items == expected_bool and isinstance(has_items, bool):
             print("Exercise 4: Passed - Correct boolean conversion for empty inventory.")
             passed_tests += 1
        elif 'has_items' not in globals():
            print("Exercise 4: Failed - Variable 'has_items' not assigned.")
        else:
            print(f"Exercise 4: Failed - Incorrect boolean conversion for the initial empty inventory.")
            print(f"  Expected: {expected_bool}")
            print(f"  Got:      {has_items}")
            
    except Exception as e:
         print(f"Exercise 4: Failed with error - {e}")

    print(f"\nType Conversion & Introspection Tests Finished. Passed {passed_tests}/{total_tests}.")

# Run tests
run_tests()

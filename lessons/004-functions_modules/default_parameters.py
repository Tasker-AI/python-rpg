### Lesson: Default Parameters ###

# Default parameters allow you to assign a default value to a function argument.
# If a value is not provided for that argument when the function is called, the default value is used.
# This makes functions more flexible, allowing some arguments to be optional.

# Use Case: Setting a default difficulty level in a game function, or a default greeting message.

### Exercise 1: Basic Default Parameter ###
# Define a function `greet_player` that takes a `name` and an optional `greeting`.
# The `greeting` should default to "Welcome".
# The function should return a formatted string: "<greeting>, <name>!"

# Syntax: def function_name(param1, param2="default_value"):
#             # function body
#             return f"{param2}, {param1}!"

greet_player = None # Define the function here

### Exercise 2: Multiple Default Parameters ###
# Define a function `create_monster` that takes `monster_type`.
# It should also take optional `health` (default 100) and `attack_power` (default 10).
# The function should return a dictionary representing the monster.

# Syntax: def function_name(param1, param2=default1, param3=default2):
#             return {"type": param1, "hp": param2, "atk": param3}

create_monster = None # Define the function here

### Exercise 3: Calling with and without Defaults ###
# Call `greet_player` once with just a name ("Hero") and once with a name ("Villain") and a custom greeting ("Beware").
# Call `create_monster` once with just the type ("Goblin") and once with type ("Dragon"), health (500), and attack_power (50).
# Store the results in the variables provided.

greeting_default = None # Call greet_player("Hero")
greeting_custom = None # Call greet_player("Villain", "Beware")
monster_default = None # Call create_monster("Goblin")
monster_custom = None # Call create_monster("Dragon", 500, 50)

# --- Tests --- #
def run_tests():
    print("--- Running Function Definition Tests ---")
    # Test Exercise 1: greet_player definition
    try:
        test1_result = greet_player("Tester")
        assert test1_result == "Welcome, Tester!", f"Test 1 Failed: Expected 'Welcome, Tester!', got '{test1_result}'"
        print("Test 1 Passed (greet_player defined correctly)")
    except Exception as e:
        print(f"Test 1 Failed: Error defining or calling greet_player - {e}")

    # Test Exercise 2: create_monster definition
    try:
        test2_result = create_monster("Imp")
        expected2 = {"type": "Imp", "hp": 100, "atk": 10}
        assert test2_result == expected2, f"Test 2 Failed: Expected {expected2}, got {test2_result}"
        print("Test 2 Passed (create_monster defined correctly with defaults)")
    except Exception as e:
        print(f"Test 2 Failed: Error defining or calling create_monster - {e}")

    print("\n--- Running Function Call Tests ---")
    # Test Exercise 3: Calling greet_player
    try:
        assert greeting_default == "Welcome, Hero!", f"Test 3a Failed: Expected 'Welcome, Hero!', got '{greeting_default}'"
        print("Test 3a Passed (greet_player default call)")
        assert greeting_custom == "Beware, Villain!", f"Test 3b Failed: Expected 'Beware, Villain!', got '{greeting_custom}'"
        print("Test 3b Passed (greet_player custom call)")
    except AssertionError as e:
        print(f"Test 3 Failed: {e}")
    except Exception as e:
        print(f"Test 3 Failed: Error calling greet_player - {e}")

    # Test Exercise 3: Calling create_monster
    try:
        expected_monster_default = {"type": "Goblin", "hp": 100, "atk": 10}
        assert monster_default == expected_monster_default, f"Test 4a Failed: Expected {expected_monster_default}, got {monster_default}"
        print("Test 4a Passed (create_monster default call)")
        expected_monster_custom = {"type": "Dragon", "hp": 500, "atk": 50}
        assert monster_custom == expected_monster_custom, f"Test 4b Failed: Expected {expected_monster_custom}, got {monster_custom}"
        print("Test 4b Passed (create_monster custom call)")
    except AssertionError as e:
        print(f"Test 4 Failed: {e}")
    except Exception as e:
        print(f"Test 4 Failed: Error calling create_monster - {e}")

run_tests()

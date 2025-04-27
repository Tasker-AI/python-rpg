### Lesson: *args and **kwargs ###

# *args allows a function to accept any number of non-keyword (positional) arguments.
# These arguments are collected into a tuple inside the function.
# **kwargs allows a function to accept any number of keyword arguments.
# These arguments are collected into a dictionary inside the function.
# They are often used when you don't know in advance how many arguments might be passed to your function.

# Use Case: Creating functions that can handle flexible inputs, like a sum function that adds any number of values, or a function that logs various attributes.

### Exercise 1: Using *args ###
# Define a function `calculate_total_score` that takes any number of score arguments using *args.
# The function should sum all the scores passed to it and return the total.

# Syntax: def function_name(*args):
#             total = 0
#             for arg in args:
#                 total += arg
#             return total

def calculate_total_score(*args):
    # Define the function here
    total = 0
    for arg in args:
        total += arg
    return total

### Exercise 2: Using **kwargs ###
# Define a function `create_character_profile` that takes a `name` argument.
# It should also accept any number of keyword arguments (**kwargs) representing character attributes (e.g., strength=10, intelligence=8).
# The function should return a dictionary containing the name and all the attributes passed via kwargs.

# Syntax: def function_name(param1, **kwargs):
#             profile = {'name': param1}
#             profile.update(kwargs) # Merge kwargs dictionary into profile
#             return profile

def create_character_profile(param1, **kwargs):
    # Define the function here
    profile = {'name': param1}
    profile.update(kwargs) # Merge kwargs dictionary into profile
    return profile

### Exercise 3: Combining *args and **kwargs ###
# Define a function `log_event` that takes an `event_type` string.
# It should also accept any number of positional arguments (*args) representing event details
# and any number of keyword arguments (**kwargs) representing metadata.
# The function should return a formatted string: "Event: <event_type> | Details: <args_tuple> | Metadata: <kwargs_dict>"

# Syntax: def function_name(param1, *args, **kwargs):
#             return f"Event: {param1} | Details: {args} | Metadata: {kwargs}"

def log_event(param1, *data, **keywordargs):
    # Define the function here
    return f"Event: {param1} | Details: {tuple(data)} | Metadata: {keywordargs}"

# --- Tests --- #
def run_tests():
    print("--- Running *args Tests ---")
    # Test Exercise 1: calculate_total_score
    try:
        score1 = calculate_total_score(10, 20, 30)
        assert score1 == 60, f"Test 1a Failed: Expected 60, got {score1}"
        print("Test 1a Passed (10, 20, 30)")
        score2 = calculate_total_score(5, -2, 15, 0)
        assert score2 == 18, f"Test 1b Failed: Expected 18, got {score2}"
        print("Test 1b Passed (5, -2, 15, 0)")
        score3 = calculate_total_score()
        assert score3 == 0, f"Test 1c Failed: Expected 0, got {score3}"
        print("Test 1c Passed (no args)")
    except Exception as e:
        print(f"Test 1 Failed: Error testing calculate_total_score - {e}")

    print("\n--- Running **kwargs Tests ---")
    # Test Exercise 2: create_character_profile
    try:
        profile1 = create_character_profile("Gandalf", wisdom=20, magic=18)
        expected1 = {'name': 'Gandalf', 'wisdom': 20, 'magic': 18}
        assert profile1 == expected1, f"Test 2a Failed: Expected {expected1}, got {profile1}"
        print("Test 2a Passed (Gandalf)")
        profile2 = create_character_profile("Conan", strength=18, constitution=16, dexterity=14)
        expected2 = {'name': 'Conan', 'strength': 18, 'constitution': 16, 'dexterity': 14}
        assert profile2 == expected2, f"Test 2b Failed: Expected {expected2}, got {profile2}"
        print("Test 2b Passed (Conan)")
        profile3 = create_character_profile("Lara")
        expected3 = {'name': 'Lara'}
        assert profile3 == expected3, f"Test 2c Failed: Expected {expected3}, got {profile3}"
        print("Test 2c Passed (Lara, no kwargs)")
    except Exception as e:
        print(f"Test 2 Failed: Error testing create_character_profile - {e}")

    print("\n--- Running Combined *args/**kwargs Tests ---")
    # Test Exercise 3: log_event
    try:
        log1 = log_event("PlayerLogin", "user123", "192.168.1.100", timestamp="2024-01-01T10:00:00", status="Success")
        expected_log1 = "Event: PlayerLogin | Details: ('user123', '192.168.1.100') | Metadata: {'timestamp': '2024-01-01T10:00:00', 'status': 'Success'}"
        assert log1 == expected_log1, f"Test 3a Failed: Expected '{expected_log1}', got '{log1}'"
        print("Test 3a Passed (Login event)")

        log2 = log_event("ItemPickup", "Sword of Destiny", location="Dragon's Lair")
        expected_log2 = "Event: ItemPickup | Details: ('Sword of Destiny',) | Metadata: {'location': 'Dragon's Lair'}"
        assert log2 == expected_log2, f"Test 3b Failed: Expected '{expected_log2}', got '{log2}'"
        print("Test 3b Passed (Item pickup)")

        log3 = log_event("ServerStart")
        expected_log3 = "Event: ServerStart | Details: () | Metadata: {}"
        assert log3 == expected_log3, f"Test 3c Failed: Expected '{expected_log3}', got '{log3}'"
        print("Test 3c Passed (Server start, no args/kwargs)")
    except Exception as e:
        print(f"Test 3 Failed: Error testing log_event - {e}")

run_tests()

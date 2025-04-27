### Lesson: Defining and Calling Functions ###

# Purpose: Learn the syntax for defining your own Python functions and how to call them.
# Functions allow you to group code into reusable blocks, making programs more organized and efficient.
# When to use: Whenever you have a piece of code you might need to run multiple times or want to give a descriptive name to.
# Example use case: Creating a function to calculate damage based on player stats and enemy defense.


### Exercise 1: Define a Simple Greeting Function ###
# Task: Define a function called `greet_player` that takes no arguments and prints the message "Welcome, brave adventurer!"
# Syntax:
# def function_name():
#     # code block indented
#     print("Something")

# Define the function greet_player below


### Exercise 2: Call the Greeting Function ###
# Task: Call the `greet_player` function you just defined to make it execute.
# Syntax: function_name()

# Call greet_player below


### Exercise 3: Define a Function with an Argument ###
# Task: Define a function called `display_health` that takes one argument, `current_health`, 
#       and prints a message like "Current Health: [value]".
# Syntax:
# def function_name(parameter1):
#     print(f"Value is: {parameter1}")

# Define the function display_health below


### Exercise 4: Call Function with an Argument ###
# Task: Call the `display_health` function, passing the player's health value `player_hp` as the argument.
# Syntax: function_name(argument_value)

player_hp = 85
# Call display_health with player_hp below


### Exercise 5: Define a Function That Returns a Value ###
# Task: Define a function called `calculate_attack_power` that takes `strength` and `weapon_bonus` 
#       as arguments and returns their sum.
# Syntax:
# def function_name(param1, param2):
#     result = param1 + param2
#     return result

# Define the function calculate_attack_power below


### Exercise 6: Call Function and Use Return Value ###
# Task: Call `calculate_attack_power` with `player_strength` and `sword_bonus`. 
#       Store the returned value in a variable called `total_power`.
# Syntax: returned_data = function_name(arg1, arg2)

player_strength = 15
sword_bonus = 5
total_power = 0
# Call calculate_attack_power and store the result in total_power below


# --- Tests --- #
# Note: Testing print output requires capturing stdout, which is a bit more complex.
# For simplicity, these tests will focus on return values and basic calls.
# We will manually check print outputs if needed.

def run_tests():
    print("Running Defining and Calling Functions Tests...")
    passed_tests = 0
    total_tests = 4 # Exercises 1/2 (print) & 3/4 (print) checked conceptually/manually
    
    # Test Exercise 1 & 2: Check if greet_player exists and is callable
    # We can't easily test the print output here without more advanced techniques.
    # We assume if it exists and runs without error, it's likely correct for this stage.
    greeting_passed = False
    try:
        if 'greet_player' in globals() and callable(globals()['greet_player']):
            print("Exercise 1: `greet_player` function defined.")
            # Try calling it
            greet_player() # This call is part of the test setup now
            print("Exercise 2: `greet_player` called successfully (output should appear above). Check manually.")
            # If we reach here without error, consider it conceptually passed for now
            greeting_passed = True
        else:
            print("Exercise 1/2: Failed - `greet_player` function not found or not callable.")
    except Exception as e:
        print(f"Exercise 1/2: Failed during call - {e}")
        
    # Test Exercise 3 & 4: Check if display_health exists and is callable with an argument
    health_display_passed = False
    try:
        if 'display_health' in globals() and callable(globals()['display_health']):
            print("Exercise 3: `display_health` function defined.")
            # Try calling it with the value used in Exercise 4
            display_health(85) # This call is part of the test setup now
            print("Exercise 4: `display_health` called successfully with argument 85 (output should appear above). Check manually.")
             # If we reach here without error, consider it conceptually passed for now
            health_display_passed = True
        else:
            print("Exercise 3/4: Failed - `display_health` function not found or not callable.")
    except TypeError as e:
        print(f"Exercise 3/4: Failed - Likely called `display_health` without the required argument or with wrong type: {e}")
    except Exception as e:
        print(f"Exercise 3/4: Failed during call - {e}")

    # Test Exercise 5: Check if calculate_attack_power exists
    calc_exists_passed = False
    try:
        if 'calculate_attack_power' in globals() and callable(globals()['calculate_attack_power']):
             print("Exercise 5: `calculate_attack_power` function defined.")
             passed_tests += 1
             calc_exists_passed = True
        else:
            print("Exercise 5: Failed - `calculate_attack_power` function not found or not callable.")
    except Exception as e:
         print(f"Exercise 5: Failed with error - {e}")
         
    # Test Exercise 6: Check return value of calculate_attack_power
    if calc_exists_passed:
        calc_return_passed = False
        try:
            # Use the values from Exercise 6
            strength_test = 15
            bonus_test = 5
            expected_power = 20
            # We check the user's assignment `total_power` which should hold the result
            if 'total_power' in globals() and total_power == expected_power:
                print(f"Exercise 6: Passed - Function returned correct value ({expected_power}) and assigned to total_power.")
                passed_tests += 1
                calc_return_passed = True
            elif 'total_power' not in globals():
                 print("Exercise 6: Failed - Variable 'total_power' not assigned.")
            else:
                 print(f"Exercise 6: Failed - Incorrect value assigned to total_power.")
                 print(f"  Expected return value: {expected_power}")
                 print(f"  Got assigned value:    {total_power}")
        except TypeError as e:
             print(f"Exercise 6: Failed - Likely called `calculate_attack_power` with wrong number/type of arguments: {e}")
        except Exception as e:
             print(f"Exercise 6: Failed during call or check - {e}")
    else:
        print("Exercise 6: Skipped - Prerequisite Exercise 5 failed.")

    # Adjust final count based on conceptual passes if necessary
    # For now, we count based on testable logic (Exercises 5 & 6)
    print(f"\nDefining and Calling Functions Tests Finished.")
    print(f"Passed {passed_tests} specific tests out of {total_tests} applicable test checks.")
    print("Exercises 1-4 involve print statements - please verify their output manually above.")

# Run tests
run_tests()

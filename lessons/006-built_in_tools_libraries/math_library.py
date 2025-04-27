### Lesson: math Library ###

# Purpose: The `math` library provides access to common mathematical functions
# beyond basic arithmetic, like square roots, rounding, powers, trigonometric functions, etc.

# When to use it:
# - When you need more advanced mathematical operations than standard operators (+, -, *, /).
# - Calculating distances (using square roots).
# - Rounding numbers up or down (e.g., for damage calculation, resource counting).
# - Calculating powers or logarithms (e.g., for experience curves, scaling).

# Example Use Case: Calculating the distance between two players on a 2D map,
# determining how many full health potions a player can afford, or calculating attack power scaling.

# Note: To use functions from the math library, you first need to import it:
# import math

import math # Import the library for the exercises

### Exercise 1: Calculating Distance ###
# Task: You have the coordinates (x, y) of two players, player A (x1, y1) and player B (x2, y2).
# Calculate the Euclidean distance between them using the formula: sqrt((x2-x1)^2 + (y2-y1)^2).
# Use math.sqrt() for the square root and the ** operator for squaring.
# Syntax: math.sqrt(number)
# Syntax: base ** exponent

x1, y1 = 2, 3  # Player A coordinates
x2, y2 = 5, 7  # Player B coordinates

distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)


### Exercise 2: Rounding Up Resources ###
# Task: A player needs 2.3 units of wood per arrow. They want to craft 5 arrows.
# Calculate the total wood needed and use math.ceil() to round *up* to the nearest whole number,
# because you can't collect partial units of wood.
# Syntax: math.ceil(number)

wood_per_arrow = 2.3
arrows_to_craft = 5
total_wood_needed = wood_per_arrow * arrows_to_craft
rounded_wood_needed = math.ceil(total_wood_needed)


### Exercise 3: Rounding Down Damage ###
# Task: A monster attack deals 18.7 damage. For display purposes or game mechanics,
# you need to round the damage *down* to the nearest whole number using math.floor().
# Syntax: math.floor(number)

raw_damage = 18.7
applied_damage = math.floor(raw_damage)


### Exercise 4: Calculating Scaled Monster HP ###
# Task: A monster's base HP is 100. 
# Its HP scales with the game level according to the formula: HP = base_hp * (1.1 ^ level).
# Calculate the monster's HP at level 5. Use math.pow() for the exponentiation.
# Syntax: math.pow(base, exponent)

base_hp = 100
level = 5
scaling_factor = 1.1
monster_hp = base_hp * math.pow(scaling_factor, level)


# Tests #
def run_tests():
    print("Running Tests...\n")

    # Test Exercise 1
    expected_distance = 5.0
    print("--- Testing Exercise 1: Calculating Distance ---")
    # Use math.isclose() for floating-point comparisons
    if math.isclose(distance, expected_distance):
        print("Exercise 1: Passed")
    else:
        print(f"Exercise 1: Failed - Expected distance {expected_distance}, but got {distance}")
    print("-" * 20)

    # Test Exercise 2
    expected_total_wood = 11.5
    expected_rounded_wood = 12
    print("--- Testing Exercise 2: Rounding Up Resources ---")
    passed2 = True
    if not math.isclose(total_wood_needed, expected_total_wood):
         print(f"Exercise 2: Failed - Incorrect raw total wood. Expected {expected_total_wood}, got {total_wood_needed}")
         passed2 = False
    if rounded_wood_needed != expected_rounded_wood:
        print(f"Exercise 2: Failed - Incorrect rounded wood. Expected {expected_rounded_wood}, got {rounded_wood_needed}")
        passed2 = False
    if passed2:
        print("Exercise 2: Passed")
    print("-" * 20)

    # Test Exercise 3
    expected_applied_damage = 18
    print("--- Testing Exercise 3: Rounding Down Damage ---")
    if applied_damage == expected_applied_damage:
        print("Exercise 3: Passed")
    else:
        print(f"Exercise 3: Failed - Expected applied damage {expected_applied_damage}, but got {applied_damage}")
    print("-" * 20)

    # Test Exercise 4
    expected_hp = 161.051
    print("--- Testing Exercise 4: Calculating Scaled Monster HP ---")
    # Use math.isclose() for floating-point comparison, especially after math.pow
    if math.isclose(monster_hp, expected_hp):
        print("Exercise 4: Passed")
    else:
        print(f"Exercise 4: Failed - Expected HP {expected_hp:.3f}, but got {monster_hp:.3f}") # Format output for clarity
    print("-" * 20)

    print("\nTests Finished.")

run_tests()

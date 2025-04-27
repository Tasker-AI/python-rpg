### Lesson: Arithmetic Operations in Python ###

# Purpose: Learn how to perform arithmetic calculations in Python
# When to use: When you need to perform mathematical operations in your game

### Task 1: Basic Arithmetic ###

## Syntax examples ##

# Python supports all basic arithmetic operations:
# Addition: a + b
# Subtraction: a - b
# Multiplication: a * b
# Division: a / b (always returns a float)
# Integer Division: a // b (returns an integer, truncates decimal part)
# Modulo (remainder): a % b
# Exponentiation: a ** b

# Order of operations follows PEMDAS:
# Parentheses, Exponents, Multiplication/Division, Addition/Subtraction
# result = (10 + 5) * 2  # Parentheses first, then multiplication

## To Do ##

weapon_power = 75
strength_multiplier = 1.5
enemy_defense = 20
# 1. Calculate a player's damage based on these formulas:
base_damage = weapon_power * strength_multiplier
critical_hit = base_damage * 2
# 3. Store the final damage in a variable called 'player_damage'
player_damage = critical_hit - enemy_defense



# Task 1 test #
def test_task1():
    try:
        # Check if player_damage exists
        if 'player_damage' not in globals():
            print("Test failed: player_damage variable not found")
            return False
            
        # Check the calculation
        weapon_power = 75
        strength_multiplier = 1.5
        enemy_defense = 20
        
        expected = (weapon_power * strength_multiplier * 2) - enemy_defense
        
        if player_damage == expected:
            print(f"Test passed: player_damage is correct: {player_damage}")
            return True
        else:
            print(f"Test failed: Expected {expected}, got {player_damage}")
            return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 2: Integer Division and Modulo ###

## Syntax examples ##

# Integer division (//) divides and rounds down to the nearest integer:
# 10 // 3 = 3
# -10 // 3 = -4  (rounds down, not toward zero)

# Modulo (%) returns the remainder after division:
# 10 % 3 = 1
# 15 % 5 = 0 (no remainder)

# Common uses:
# - Check if a number is even: x % 2 == 0
# - Cycle through values: index % array_length
# - Convert between units: seconds % 60 (seconds in a minute)

## To Do ##

# 1. A game has a day/night cycle that repeats every 24 in-game hours
# 3. The game has been running for 'total_seconds' seconds
# 6. Use total_seconds = 8427
total_seconds = 8427
# 2. Each real-world second represents 10 in-game minutes (1/6 of an hour)
total_minutes = total_seconds * 10
# Convert total_minutes to hours
total_hours = total_minutes / 60
# 4. Calculate the current in-game hour (0-23) and store in 'game_hour'
game_hour = int(total_hours % 24)

# 5. Calculate whether it's currently day or night and store in 'is_daytime'
#      (day is between 6am and 6pm, i.e., hours 6-17)

if game_hour >= 6 and game_hour < 18:
    is_daytime = True
else:
    is_daytime = False



## Task 2 test ##
def test_task2():
    try:
        # Check if variables exist
        if 'game_hour' not in globals():
            print("Test failed: game_hour variable not found")
            return False
        if 'is_daytime' not in globals():
            print("Test failed: is_daytime variable not found")
            return False
            
        # Check calculations
        total_seconds = 8427
        in_game_minutes = total_seconds * 10
        in_game_hours = in_game_minutes / 60
        expected_hour = int(in_game_hours % 24)
        expected_daytime = expected_hour >= 6 and expected_hour < 18
        
        if game_hour == expected_hour:
            print(f"Test passed: game_hour is correct: {game_hour}")
        else:
            print(f"Test failed: Expected hour {expected_hour}, got {game_hour}")
            return False
            
        if is_daytime == expected_daytime:
            print(f"Test passed: is_daytime is correct: {is_daytime}")
        else:
            print(f"Test failed: Expected is_daytime {expected_daytime}, got {is_daytime}")
            return False
            
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 3: Complex Calculations ###

## Syntax examples ##

# You can combine multiple operations:
# result = (a + b) * c / d

# Python has built-in math functions:
# abs(-5)      # Absolute value: 5
# round(3.7)   # Round to nearest integer: 4
# min(5, 10)   # Minimum value: 5
# max(5, 10)   # Maximum value: 10

# For more advanced math, import the math module:
# import math
# math.sqrt(16)    # Square root: 4.0
# math.floor(3.7)  # Round down: 3
# math.ceil(3.2)   # Round up: 4

## To Do ##

# 1. Calculate a character's health percentage after taking damage:

max_health = 1000
current_health = 560
damage_taken = 120
healing_potion = 75

new_health = current_health - damage_taken + healing_potion

health_percentage = new_health / max_health * 100

if health_percentage < 25:
    is_critical = True
else:
    is_critical = False

## Task 3 test ##
def test_task3():
    try:
        # Check if variables exist
        if 'new_health' not in globals():
            print("Test failed: new_health variable not found")
            return False
        if 'health_percentage' not in globals():
            print("Test failed: health_percentage variable not found")
            return False
        if 'is_critical' not in globals():
            print("Test failed: is_critical variable not found")
            return False
            
        # Check calculations
        max_health = 1000
        current_health = 560
        damage_taken = 120
        healing_potion = 75
        
        expected_new_health = current_health - damage_taken + healing_potion
        expected_percentage = (expected_new_health / max_health) * 100
        expected_critical = expected_percentage < 25
        
        if new_health == expected_new_health:
            print(f"Test passed: new_health is correct: {new_health}")
        else:
            print(f"Test failed: Expected new_health {expected_new_health}, got {new_health}")
            return False
            
        if abs(health_percentage - expected_percentage) < 0.01:  # Allow small floating point differences
            print(f"Test passed: health_percentage is correct: {health_percentage}%")
        else:
            print(f"Test failed: Expected health_percentage {expected_percentage}%, got {health_percentage}%")
            return False
            
        if is_critical == expected_critical:
            print(f"Test passed: is_critical is correct: {is_critical}")
        else:
            print(f"Test failed: Expected is_critical {expected_critical}, got {is_critical}")
            return False
            
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


# Run all tests
def run_tests():
    print("\n=== Running Tests ===")
    task1_passed = test_task1()
    task2_passed = test_task2()
    task3_passed = test_task3()
    
    if task1_passed and task2_passed and task3_passed:
        print("\nAll tests passed! Your game math is working!")
    else:
        print("\nSome tests failed. Check your code and try again!")

run_tests()

### Lesson: User Input in Python ###

# Purpose: Learn how to get input from users in Python
# When to use: When you need to interact with users and collect their input during program execution

### Task 1: Basic User Input ###

## Syntax examples ##

# In Python, you can get user input with the input() function
# name = input("What is your name? ")

# The input() function always returns a string
# age_string = input("How old are you? ")
# To convert to a number, you need to use int() or float()
# age = int(age_string)

## To Do ##

# Create a simple character creation prompt that:
# 1. Asks for the player's name
player_name = input("What is your name? ")

# 2. Stores it in a variable called 'player_name'
# 3. Prints a welcome message using the name
print(f"Welcome, {player_name}")

# Task 1 test #
def test_task1():
    # This test requires manual input, so we'll just check if the variables exist
    try:
        # Check if player_name exists
        if 'player_name' in locals() or 'player_name' in globals():
            print("Test passed: player_name variable exists")
        else:
            print("Test failed: player_name variable not found")
            return False
        
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 2: Converting Input ###

## Syntax examples ##

# Remember that input() always returns a string
# To use numeric input in calculations, you need to convert it:
# 
# For integers (whole numbers):
# level = int(input("What level are you? "))
#
# For floating point (decimal numbers):
# health = float(input("How much health do you have? "))
#
# You can also handle errors with try/except:
# try:
#     age = int(input("Enter your age: "))
# except ValueError:
#     print("That's not a valid number!")

## To Do ##

# 1. Ask the user for their character's level (should be an integer)
# 2. Store it in a variable called 'player_level'
player_level = int(input("what is your level? "))

# 3. Ask the user for their character's health points (can be a decimal)
# 4. Store it in a variable called 'player_health'
player_health = float(input("What is your health? "))

# 5. Calculate and print the character's power (level × health)
power = player_level * player_health
print(power)


## Task 2 test ##
def test_task2():
    try:
        # Check if player_level exists and is an integer
        if 'player_level' in locals() or 'player_level' in globals():
            if isinstance(player_level, int):
                print(f"Test passed: player_level exists and is an integer: {player_level}")
            else:
                print(f"Test failed: player_level is not an integer: {type(player_level)}")
                return False
        else:
            print("Test failed: player_level variable not found")
            return False
            
        # Check if player_health exists and is a number
        if 'player_health' in locals() or 'player_health' in globals():
            if isinstance(player_health, (int, float)):
                print(f"Test passed: player_health exists and is a number: {player_health}")
            else:
                print(f"Test failed: player_health is not a number: {type(player_health)}")
                return False
        else:
            print("Test failed: player_health variable not found")
            return False
            
        # Check if power calculation exists
        power = player_level * player_health
        print(f"Character power calculation: {power}")
        
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 3: Input Validation ###

## Syntax examples ##

# It's important to validate user input to prevent errors
# 
# Basic validation with a while loop:
# valid_input = False
# while not valid_input:
#     try:
#         age = int(input("Enter your age: "))
#         if age > 0 and age < 120:
#             valid_input = True
#         else:
#             print("Age must be between 1 and 119")
#     except ValueError:
#         print("Please enter a valid number")

## To Do ##

# 1. Ask the user to choose a character class (warrior, mage, or archer)
# 2. Store it in a variable called 'character_class'
character_class = input("Choose a character (warrior, mage, archer): ")

# 3. Validate that the input is one of the three options (case-insensitive)
valid_input = False
character_class = character_class.capitalize()
# 4. If invalid, keep asking until a valid class is entered
while not valid_input:
    try:
        if character_class in ["Archer", "Warrior", "Mage"]:
            valid_input = True
        else: print("Character class must be a warrior, mage, or archer")
    except ValueError:
        print("Please enter a valid string")

# 5. Print a message about the chosen class's special ability:
#    - Warrior: "Warriors have extra strength!"
#    - Mage: "Mages can cast powerful spells!"
#    - Archer: "Archers have superior accuracy!"
if character_class == "Warrior":
    print("Warriors have extra strength!")
elif character_class == "Mage":
    print("Mages can cast powerful spells!")
elif character_class == "Archer":
    print("Archers have superior accuracy!")



## Task 3 test ##
def test_task3():
    try:
        # Check if character_class exists
        if 'character_class' in locals() or 'character_class' in globals():
            # Convert to lowercase for case-insensitive comparison
            class_lower = character_class.lower()
            
            # Check if it's one of the valid options
            if class_lower in ['warrior', 'mage', 'archer']:
                print(f"Test passed: character_class is valid: {character_class}")
            else:
                print(f"Test failed: character_class is not valid: {character_class}")
                return False
        else:
            print("Test failed: character_class variable not found")
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
        print("\nAll tests passed! Your character is ready for adventure!")
    else:
        print("\nSome tests failed. Check your code and try again!")

# Uncomment to run the tests
run_tests()

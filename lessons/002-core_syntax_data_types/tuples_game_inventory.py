### Lesson Description: ###
# Purpose: Tuples are immutable ordered collections that cannot be changed after creation
# When to use: Use tuples when you need a fixed collection of data that shouldn't change, like coordinates, RGB colors, or character stats


### Task 1 ###

## Syntax examples ##
# character_stats = ("Warrior", 100, 75.5)  # A tuple with mixed data types
# empty_tuple = ()                          # An empty tuple
# single_item = ("Sword",)                  # Note the comma for a single-item tuple

## To Do ##
# Create a tuple called 'character' with: character name (string), level (integer), and is_magic_user (boolean)
character = (
    "Harry",
    50,
    True
)

# Task 1 test
def test_task1():
    try:
        if not isinstance(character, tuple):
            print("FAILED: character should be a tuple")
            print(f"   Actual: {type(character)}")
            print(f"   Expected: {type(())}")
            return False
        elif len(character) != 3:
            print("FAILED: character should have 3 items")
            print(f"   Actual length: {len(character)}")
            print(f"   Expected length: 3")
            return False
        elif not isinstance(character[0], str):
            print("FAILED: First item should be a string (character name)")
            print(f"   Actual: {type(character[0])}")
            print(f"   Expected: {type('')}")
            return False
        elif not isinstance(character[1], int):
            print("FAILED: Second item should be an integer (level)")
            print(f"   Actual: {type(character[1])}")
            print(f"   Expected: {type(0)}")
            return False
        elif not isinstance(character[2], bool):
            print("FAILED: Third item should be a boolean (is_magic_user)")
            print(f"   Actual: {type(character[2])}")
            print(f"   Expected: {type(True)}")
            return False
        else:
            print("PASSED: character tuple is correctly structured")
            print(f"   Value: {character}")
            return True
    except NameError:
        print("FAILED: character variable not found")
        return False

print("\nRunning Task 1 test...")
test_task1()

### Task 2 ###

# Syntax examples ##
# weapon_tuple = ("Axe", "Shield")        # A tuple with multiple items

## To Do ##
# Create a tuple called 'weapons' with at least two weapon strings
weapons = ("Axe", "Bow")

# Task 2 test
def test_task2():
    try:
        if not isinstance(weapons, tuple):
            print("FAILED: weapons should be a tuple")
            print(f"   Actual: {type(weapons)}")
            print(f"   Expected: {type(())}")
            return False
        elif len(weapons) < 2:
            print("FAILED: weapons should have at least 2 items")
            print(f"   Actual length: {len(weapons)}")
            print(f"   Expected length: at least 2")
            return False
        else:
            print("PASSED: weapons is a tuple with at least 2 items")
            print(f"   Value: {weapons}")
            return True
    except NameError:
        print("FAILED: weapons variable not found")
        return False

print("\nRunning Task 2 test...")
test_task2()

### Task 3 ###

## Syntax examples ##
# full_character = character_stats + weapon_tuple  # Combines two tuples

## To Do ##
# Combine the 'character' and 'weapons' tuples into a new tuple called 'character_profile'
character_profile = character + weapons

# Task 3 test
def test_task3():
    try:
        expected_profile = character + weapons
        if not isinstance(character_profile, tuple):
            print("FAILED: character_profile should be a tuple")
            print(f"   Actual: {type(character_profile)}")
            print(f"   Expected: {type(())}")
            return False
        elif character_profile != expected_profile:
            print("FAILED: character_profile should be character + weapons")
            print(f"   Actual: {character_profile}")
            print(f"   Expected: {expected_profile}")
            return False
        else:
            print("PASSED: character_profile is correct!")
            print(f"   Value: {character_profile}")
            return True
    except NameError:
        print("FAILED: character_profile variable not found")
        return False

print("\nRunning Task 3 test...")
test_task3()

### Task 4 ###

## Syntax examples ##
# class_name, hp, power = character_stats   # Assigns each value to a variable

## To Do ##
# Unpack the 'character' tuple into three variables: name, level, and magic_user
name, level, magic_user = character

# Task 4 test
def test_task4():
    try:
        if name != character[0]:
            print("FAILED: name should be the first item in character")
            print(f"   Actual: {name}")
            print(f"   Expected: {character[0]}")
            return False
        elif level != character[1]:
            print("FAILED: level should be the second item in character")
            print(f"   Actual: {level}")
            print(f"   Expected: {character[1]}")
            return False
        elif magic_user != character[2]:
            print("FAILED: magic_user should be the third item in character")
            print(f"   Actual: {magic_user}")
            print(f"   Expected: {character[2]}")
            return False
        else:
            print("PASSED: tuple unpacking is correct!")
            print(f"   name: {name}, level: {level}, magic_user: {magic_user}")
            return True
    except NameError:
        print("FAILED: One or more unpacked variables not found")
        return False

print("\nRunning Task 4 test...")
test_task4()

### Task 5 ###

## Syntax examples ##
# has_warrior = "Warrior" in character_stats  # True if "Warrior" is in the tuple
# stat_count = len(character_stats)           # Returns the number of items

## To Do ## 
# 1. Create a variable 'has_bow' that checks if "bow" is in the 'weapons' tuple
has_bow = "bow" in weapons

# 2. Create a variable 'total_items' with the total number of items in 'character_profile'
total_items = len(character_profile)

# Task 5 test
def test_task5():
    # Test has_bow
    try:
        if not isinstance(has_bow, bool):
            print("FAILED: has_bow should be a boolean")
            print(f"   Actual: {type(has_bow)}")
            print(f"   Expected: {type(True)}")
            return False
        else:
            print("PASSED: has_bow is a boolean!")
            print(f"   Value: {has_bow}")
    except NameError:
        print("FAILED: has_bow variable not found")
        return False
        
    # Test total_items
    try:
        expected_count = len(character_profile)
        if total_items != expected_count:
            print("FAILED: total_items has incorrect value")
            print(f"   Actual: {total_items}")
            print(f"   Expected: {expected_count}")
            return False
        else:
            print("PASSED: total_items is correct!")
            print(f"   Value: {total_items}")
            return True
    except NameError:
        print("FAILED: total_items variable not found")
        return False

print("\nRunning Task 5 test...")
test_task5()

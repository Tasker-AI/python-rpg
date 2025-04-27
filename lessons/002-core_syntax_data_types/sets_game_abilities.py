### Lesson Description: ###
# Purpose of the concept: Sets are unordered collections of unique elements
# When to use it: Use sets when you need to store unique values and check for membership quickly

### Task 1 ###

## Syntax examples ##
# Creating sets
# warrior_skills = {"Slash", "Block", "Charge"}  # Set with string elements
# empty_set = set()  # Empty set (can't use {} as that creates an empty dictionary)
# numbers = {1, 2, 3, 4, 5}  # Set with integer elements

# # Sets automatically remove duplicates
# repeated_items = {1, 1, 2, 2, 3}  # Results in {1, 2, 3}

## To Do ##
# Create a set called 'character_abilities' with at least 3 unique string abilities
# (like "Fireball", "Heal", "Stealth", etc.)
character_abilities = {"Fireball", "Heal", "Stealth"}


# Task 1 test #
def test_task1():
    try:
        if not isinstance(character_abilities, set):
            print("FAILED: character_abilities should be a set")
            print(f"   Actual: {type(character_abilities)}")
            print(f"   Expected: {type(set())}")
            return False
            
        if len(character_abilities) < 3:
            print("FAILED: character_abilities should have at least 3 items")
            print(f"   Actual length: {len(character_abilities)}")
            print(f"   Expected length: at least 3")
            return False
            
        for ability in character_abilities:
            if not isinstance(ability, str):
                print(f"FAILED: All abilities should be strings")
                print(f"   Found non-string value: {ability} of type {type(ability)}")
                return False
                
        print("PASSED: character_abilities is a set with at least 3 string abilities")
        print(f"   Value: {character_abilities}")
        return True
    except NameError:
        print("FAILED: character_abilities variable not found")
        return False

print("\nRunning Task 1 test...")
test_task1()

### Task 2 ###

# Store original abilities for comparison in Task 2
original_abilities = character_abilities.copy()

## Syntax examples ##
# Adding items to a set
# warrior_skills.add("Taunt")  # Adds a single item

# # Removing items from a set
# warrior_skills.remove("Block")  # Removes an item (raises error if not found)
# warrior_skills.discard("Shield")  # Removes an item if present (no error if not found)

# # Getting set length
# skill_count = len(warrior_skills)  # Returns number of items in the set

## To Do ##
# 1. Add a new ability to your character_abilities set
character_abilities.add("Taunt")
character_abilities.add("ability5")


# 2. Try to add an ability that's already in the set (notice it won't create a duplicate)
character_abilities.add("Stealth")

# 3. Remove one ability using the remove() method
character_abilities.remove("Taunt")

# 4. Create a variable 'ability_count' with the number of abilities after these operations
ability_count = len(character_abilities)

# Task 2 test #
def test_task2():
    try:
        global original_abilities
        
        # Check if abilities were modified
        if set(character_abilities) == set(original_abilities):
            print("FAILED: character_abilities should be modified")
            print(f"   Original: {original_abilities}")
            print(f"   Current: {character_abilities}")
            return False
            
        # Check ability_count
        try:
            if not isinstance(ability_count, int):
                print("FAILED: ability_count should be an integer")
                print(f"   Actual: {type(ability_count)}")
                return False
                
            if ability_count != len(character_abilities):
                print("FAILED: ability_count should equal the length of character_abilities")
                print(f"   Actual: {ability_count}")
                print(f"   Expected: {len(character_abilities)}")
                return False
                
            print("PASSED: Set modifications and ability_count are correct")
            print(f"   Modified abilities: {character_abilities}")
            print(f"   ability_count: {ability_count}")
            return True
        except NameError:
            print("FAILED: ability_count variable not found")
            return False
    except NameError:
        print("FAILED: Required variables not found")
        return False

# This has been moved to before Task 2

print("\nRunning Task 2 test...")
test_task2()

### Task 3 ###

## Syntax examples ##
# Set operations
# mage_skills = {"Fireball", "Teleport", "Frost Nova"}
# common_rpg_skills = {"Dodge", "Jump", "Teleport"}

# Union (all items from both sets, no duplicates)
# all_skills = mage_skills | common_rpg_skills  # or mage_skills.union(common_rpg_skills)

# # Intersection (only items in both sets)
# shared_skills = mage_skills & common_rpg_skills  # or mage_skills.intersection(common_rpg_skills)

# # Difference (items in first set but not in second)
# unique_mage_skills = mage_skills - common_rpg_skills  # or mage_skills.difference(common_rpg_skills)

# # Symmetric difference (items in either set but not in both)
# non_shared_skills = mage_skills ^ common_rpg_skills  # or mage_skills.symmetric_difference(common_rpg_skills)

## To Do ##
# 1. Create a set called 'enemy_abilities' with at least 3 abilities (strings), with at least 1 that's also in character_abilities
enemy_abilities = {"Heal", "Attack", "Dodge"}

# 2. Create a set 'all_abilities' that contains all abilities from both character_abilities and enemy_abilities
all_abilities = character_abilities | enemy_abilities

# 3. Create a set 'shared_abilities' that contains only abilities present in both sets
shared_abilities = character_abilities & enemy_abilities

# 4. Create a set 'unique_character_abilities' with abilities that only the character has (not the enemy)
unique_character_abilities = character_abilities - enemy_abilities


# Task 3 test #
def test_task3():
    # Check enemy_abilities
    try:
        if not isinstance(enemy_abilities, set):
            print("FAILED: enemy_abilities should be a set")
            print(f"   Actual: {type(enemy_abilities)}")
            return False
            
        if len(enemy_abilities) < 3:
            print("FAILED: enemy_abilities should have at least 3 items")
            print(f"   Actual length: {len(enemy_abilities)}")
            return False
            
        # Check all_abilities
        try:
            if not isinstance(all_abilities, set):
                print("FAILED: all_abilities should be a set")
                print(f"   Actual: {type(all_abilities)}")
                return False
                
            expected_all = character_abilities | enemy_abilities
            if all_abilities != expected_all:
                print("FAILED: all_abilities should be the union of character_abilities and enemy_abilities")
                print(f"   Actual: {all_abilities}")
                print(f"   Expected: {expected_all}")
                return False
                
            print(f"PASSED: all_abilities is correct: {all_abilities}")
        except NameError:
            print("FAILED: all_abilities variable not found")
            return False
            
        # Check shared_abilities
        try:
            if not isinstance(shared_abilities, set):
                print("FAILED: shared_abilities should be a set")
                print(f"   Actual: {type(shared_abilities)}")
                return False
                
            expected_shared = character_abilities & enemy_abilities
            if shared_abilities != expected_shared:
                print("FAILED: shared_abilities should be the intersection of character_abilities and enemy_abilities")
                print(f"   Actual: {shared_abilities}")
                print(f"   Expected: {expected_shared}")
                return False
                
            if len(shared_abilities) == 0:
                print("FAILED: shared_abilities should not be empty (enemy_abilities should have at least one ability from character_abilities)")
                return False
                
            print(f"PASSED: shared_abilities is correct: {shared_abilities}")
        except NameError:
            print("FAILED: shared_abilities variable not found")
            return False
            
        # Check unique_character_abilities
        try:
            if not isinstance(unique_character_abilities, set):
                print("FAILED: unique_character_abilities should be a set")
                print(f"   Actual: {type(unique_character_abilities)}")
                return False
                
            expected_unique = character_abilities - enemy_abilities
            if unique_character_abilities != expected_unique:
                print("FAILED: unique_character_abilities should be the difference between character_abilities and enemy_abilities")
                print(f"   Actual: {unique_character_abilities}")
                print(f"   Expected: {expected_unique}")
                return False
                
            print(f"PASSED: unique_character_abilities is correct: {unique_character_abilities}")
            return True
        except NameError:
            print("FAILED: unique_character_abilities variable not found")
            return False
    except NameError:
        print("FAILED: enemy_abilities variable not found")
        return False

print("\nRunning Task 3 test...")
test_task3()

### Task 4 ###

## Syntax examples ##
# Checking membership
# has_teleport = "Teleport" in mage_skills  # Returns True if "Teleport" is in the set
# 
# # Converting between sets and other data types
# skill_list = ["Fireball", "Teleport", "Frost Nova"]
# skill_set = set(skill_list)  # Converts list to set
# 
# skill_tuple = tuple(skill_set)  # Converts set to tuple
# skill_list_again = list(skill_set)  # Converts set to list
# 
# # Frozen sets (immutable sets that can't be changed after creation)
# default_skills = frozenset({"Walk", "Jump", "Interact"})  # Creates an immutable set

## To Do ##
# 1. Create a variable 'has_fireball' that checks if "Fireball" is in character_abilities
has_fireball = "Fireball" in character_abilities

# 2. Create a list called 'ability_list' containing all items from character_abilities
ability_list = list(character_abilities)

# 3. Create a new set 'base_abilities' from this list: ["Walk", "Jump", "Talk"]
base_abilities = set(["Walk", "Jump", "Talk"])

# 4. Create a frozenset called 'permanent_abilities' with at least 2 string abilities
permanent_abilities = frozenset({"ability1", "ability2"})

# Task 4 test #
def test_task4():
    # Check has_fireball
    try:
        if not isinstance(has_fireball, bool):
            print("FAILED: has_fireball should be a boolean")
            print(f"   Actual: {type(has_fireball)}")
            return False
            
        expected_has_fireball = "Fireball" in character_abilities
        if has_fireball != expected_has_fireball:
            print(f"FAILED: has_fireball should be {expected_has_fireball}")
            print(f"   Actual: {has_fireball}")
            return False
            
        print(f"PASSED: has_fireball is correct: {has_fireball}")
    except NameError:
        print("FAILED: has_fireball variable not found")
        return False
        
    # Check ability_list
    try:
        if not isinstance(ability_list, list):
            print("FAILED: ability_list should be a list")
            print(f"   Actual: {type(ability_list)}")
            return False
            
        if set(ability_list) != character_abilities:
            print("FAILED: ability_list should contain all items from character_abilities")
            print(f"   Actual list: {ability_list}")
            print(f"   Expected set: {character_abilities}")
            return False
            
        print(f"PASSED: ability_list is correct: {ability_list}")
    except NameError:
        print("FAILED: ability_list variable not found")
        return False
        
    # Check base_abilities
    try:
        if not isinstance(base_abilities, set):
            print("FAILED: base_abilities should be a set")
            print(f"   Actual: {type(base_abilities)}")
            return False
            
        expected_base = {"Walk", "Jump", "Talk"}
        if base_abilities != expected_base:
            print("FAILED: base_abilities should contain 'Walk', 'Jump', and 'Talk'")
            print(f"   Actual: {base_abilities}")
            print(f"   Expected: {expected_base}")
            return False
            
        print(f"PASSED: base_abilities is correct: {base_abilities}")
    except NameError:
        print("FAILED: base_abilities variable not found")
        return False
        
    # Check permanent_abilities
    try:
        if not isinstance(permanent_abilities, frozenset):
            print("FAILED: permanent_abilities should be a frozenset")
            print(f"   Actual: {type(permanent_abilities)}")
            return False
            
        if len(permanent_abilities) < 2:
            print("FAILED: permanent_abilities should have at least 2 items")
            print(f"   Actual length: {len(permanent_abilities)}")
            return False
            
        print(f"PASSED: permanent_abilities is a frozenset with at least 2 items")
        print(f"   Value: {permanent_abilities}")
        return True
    except NameError:
        print("FAILED: permanent_abilities variable not found")
        return False

print("\nRunning Task 4 test...")
test_task4()

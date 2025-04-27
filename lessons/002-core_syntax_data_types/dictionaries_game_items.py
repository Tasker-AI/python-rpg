### Lesson Description: ###
# Purpose of the concept: Dictionaries are mutable key-value pair collections for fast lookups
# When to use it: Use dictionaries when you need to store and retrieve data using unique keys (similar to objects in JavaScript)

### Task 1 ###

## Syntax examples ##
# Creating dictionaries
# player = {"name": "Wizard", "health": 100, "level": 5}  # Dictionary with string keys
# empty_dict = {}  # Empty dictionary
# 
# # Accessing dictionary values
# player_name = player["name"]  # Returns "Wizard"
# 
# # Alternative access with .get() (safer, returns None if key doesn't exist)
# player_health = player.get("health")  # Returns 100
# missing_value = player.get("mana")  # Returns None instead of error

## To Do ##
# Create a dictionary called 'character' with these key-value pairs:
# - "name" (string)
# - "level" (integer)
# - "health" (integer or float)
# - "is_magic_user" (boolean)
character = {
    "name" : "Harry",
    "level" : 3,
    "health" : 10.0,
    "is_magic_user" : True,
}

# Task 1 test #
def test_task1():
    try:
        if not isinstance(character, dict):
            print("FAILED: character should be a dictionary")
            print(f"   Actual: {type(character)}")
            print(f"   Expected: {type({})}")
            return False
        
        # Check for required keys
        required_keys = ["name", "level", "health", "is_magic_user"]
        for key in required_keys:
            if key not in character:
                print(f"FAILED: character dictionary missing required key '{key}'")
                print(f"   Current keys: {list(character.keys())}")
                return False
        
        # Check value types
        if not isinstance(character["name"], str):
            print("FAILED: character['name'] should be a string")
            print(f"   Actual: {type(character['name'])}")
            return False
            
        if not isinstance(character["level"], int):
            print("FAILED: character['level'] should be an integer")
            print(f"   Actual: {type(character['level'])}")
            return False
            
        if not isinstance(character["health"], (int, float)):
            print("FAILED: character['health'] should be a number (int or float)")
            print(f"   Actual: {type(character['health'])}")
            return False
            
        if not isinstance(character["is_magic_user"], bool):
            print("FAILED: character['is_magic_user'] should be a boolean")
            print(f"   Actual: {type(character['is_magic_user'])}")
            return False
            
        print("PASSED: character dictionary is correctly structured")
        print(f"   Value: {character}")
        return True
    except NameError:
        print("FAILED: character variable not found")
        return False

print("\nRunning Task 1 test...")
test_task1()

### Task 2 ###

## Syntax examples ##
# Modifying dictionaries
# player["health"] = 95  # Update existing value
# player["mana"] = 50    # Add new key-value pair
# 
# # Dictionary methods
# keys_list = player.keys()      # Returns dict_keys(['name', 'health', 'level', 'mana'])
# values_list = player.values()  # Returns dict_values(['Wizard', 95, 5, 50])
# items_list = player.items()    # Returns dict_items([('name', 'Wizard'), ('health', 95), ...])

## To Do ##
# 1. Update the 'health' value in your character dictionary to 95
character["health"] = 95

# 2. Add a new key-value pair: "weapon" with a string value
character["weapon"] = "Scimitar"

# 3. Create a variable 'character_keys' containing all the keys in the character dictionary
character_keys = character.keys()


# Task 2 test #
def test_task2():
    try:
        # Check health update
        if character["health"] != 95:
            print("FAILED: character['health'] should be updated to 95")
            print(f"   Actual: {character['health']}")
            print(f"   Expected: 95")
            return False
            
        # Check weapon added
        if "weapon" not in character:
            print("FAILED: character dictionary missing 'weapon' key")
            print(f"   Current keys: {list(character.keys())}")
            return False
            
        if not isinstance(character["weapon"], str):
            print("FAILED: character['weapon'] should be a string")
            print(f"   Actual: {type(character['weapon'])}")
            return False
            
        # Check character_keys
        try:
            if not isinstance(character_keys, type(character.keys())):
                print("FAILED: character_keys should be a dict_keys object")
                print(f"   Actual: {type(character_keys)}")
                return False
                
            expected_keys = set(character.keys())
            actual_keys = set(character_keys)
            if expected_keys != actual_keys:
                print("FAILED: character_keys should contain all keys from character dictionary")
                print(f"   Actual: {actual_keys}")
                print(f"   Expected: {expected_keys}")
                return False
                
            print("PASSED: All dictionary modifications are correct")
            print(f"   Updated character: {character}")
            print(f"   character_keys: {character_keys}")
            return True
        except NameError:
            print("FAILED: character_keys variable not found")
            return False
    except KeyError:
        print("FAILED: character dictionary missing required keys")
        return False

print("\nRunning Task 2 test...")
test_task2()

### Task 3 ###

## Syntax examples ##
# Checking if a key exists
# has_mana = "mana" in player  # Returns True if 'mana' is a key in player

# # Removing items
# removed_health = player.pop("health")  # Removes 'health' key and returns its value
# del player["mana"]  # Removes 'mana' key (no return value)

# # Looping through dictionaries
# for key in player:
#     print(key, player[key])  # Prints each key and value

# for key, value in player.items():
#     print(key, value)  # Cleaner way to loop through key-value pairs

## To Do ##
# 1. Create a variable 'has_armor' that checks if "armor" is a key in the character dictionary
has_armor = "armor" in character

# 2. Remove the "is_magic_user" key from the character dictionary using the pop() method and store the value in a variable called 'is_magic_user'
is_magic_user = character.pop("is_magic_user")

# 3. Create a string variable 'character_info' that contains a formatted string with all character details
#    (Hint: Loop through the dictionary and add each key-value pair to the string)
character_info = "\n--- Character Info ---"
for key, value in character.items():
    character_info += f"\n{key}: {value}"


# Task 3 test #
def test_task3():
    # Check has_armor
    try:
        if not isinstance(has_armor, bool):
            print("FAILED: has_armor should be a boolean")
            print(f"   Actual: {type(has_armor)}")
            return False
            
        expected_has_armor = "armor" in character
        if has_armor != expected_has_armor:
            print(f"FAILED: has_armor should be {expected_has_armor}")
            print(f"   Actual: {has_armor}")
            return False
            
        print(f"PASSED: has_armor is correct: {has_armor}")
    except NameError:
        print("FAILED: has_armor variable not found")
        return False
        
    # Check is_magic_user removal and variable
    try:
        if "is_magic_user" in character:
            print("FAILED: 'is_magic_user' key should be removed from character dictionary")
            return False
            
        if not isinstance(is_magic_user, bool):
            print("FAILED: is_magic_user should be a boolean")
            print(f"   Actual: {type(is_magic_user)}")
            return False
            
        print(f"PASSED: is_magic_user key removed and value stored: {is_magic_user}")
    except NameError:
        print("FAILED: is_magic_user variable not found")
        return False
        
    # Check character_info string
    try:
        if not isinstance(character_info, str):
            print("FAILED: character_info should be a string")
            print(f"   Actual: {type(character_info)}")
            return False
            
        # Check if all keys are mentioned in the string
        for key in character.keys():
            if str(key) not in character_info:
                print(f"FAILED: character_info should include the key '{key}'")
                return False
                
            # Check if all values are mentioned in the string
            if str(character[key]) not in character_info:
                print(f"FAILED: character_info should include the value '{character[key]}'")
                return False
                
        print("PASSED: character_info contains all character details")
        print(f"   character_info: {character_info}")
        return True
    except NameError:
        print("FAILED: character_info variable not found")
        return False

print("\nRunning Task 3 test...")
test_task3()

### Task 4 ###

## Syntax examples ##
# Nested dictionaries
# game_character = {
#     "info": {"name": "Wizard", "level": 5},
#     "stats": {"health": 100, "mana": 50},
#     "inventory": {"gold": 150, "potions": 3}
# }

# # Accessing nested values
# character_name = game_character["info"]["name"]  # Returns "Wizard"
# gold_amount = game_character["inventory"]["gold"]  # Returns 150

# Dictionary comprehensions (creating dictionaries from other data)
# squared_numbers = {x: x**2 for x in range(5)}  # Creates {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

## To Do ##
# 1. Create a nested dictionary called 'game_character' with these sections:
#    - "info": containing name and level from your character dictionary
#    - "stats": containing health from your character dictionary
#    - "inventory": containing weapon from your character dictionary and a new "gold" key with a numeric value
game_character = {
    "info": {
        "name" : character["name"],
        "level": character["level"],
    },
    "stats": {
        "health" : character["health"],
    },
    "inventory": {
        "weapon" : character["weapon"],
        "gold" : 10,
    },
}


# 2. Create a variable 'gold_amount' that accesses the gold value from the nested dictionary
gold_amount = game_character["inventory"]["gold"]

# 3. Create a dictionary called 'level_bonuses' using a dictionary comprehension that maps levels 1-5 to
#    bonus values (level × 10) - Example: {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
level_bonuses = {
    1 : 10,
    2 : 20,
    3 : 30,
    4 : 40,
    5 : 50,
}

# Task 4 test #
def test_task4():
    # Check game_character structure
    try:
        if not isinstance(game_character, dict):
            print("FAILED: game_character should be a dictionary")
            print(f"   Actual: {type(game_character)}")
            return False
            
        # Check required sections
        required_sections = ["info", "stats", "inventory"]
        for section in required_sections:
            if section not in game_character:
                print(f"FAILED: game_character missing required section '{section}'")
                print(f"   Current sections: {list(game_character.keys())}")
                return False
                
            if not isinstance(game_character[section], dict):
                print(f"FAILED: game_character['{section}'] should be a dictionary")
                print(f"   Actual: {type(game_character[section])}")
                return False
                
        # Check specific nested values
        if "name" not in game_character["info"] or game_character["info"]["name"] != character["name"]:
            print("FAILED: game_character['info'] should contain the name from character")
            print(f"   Actual info: {game_character['info']}")
            return False
            
        if "level" not in game_character["info"] or game_character["info"]["level"] != character["level"]:
            print("FAILED: game_character['info'] should contain the level from character")
            print(f"   Actual info: {game_character['info']}")
            return False
            
        if "health" not in game_character["stats"] or game_character["stats"]["health"] != character["health"]:
            print("FAILED: game_character['stats'] should contain the health from character")
            print(f"   Actual stats: {game_character['stats']}")
            return False
            
        if "weapon" not in game_character["inventory"] or game_character["inventory"]["weapon"] != character["weapon"]:
            print("FAILED: game_character['inventory'] should contain the weapon from character")
            print(f"   Actual inventory: {game_character['inventory']}")
            return False
            
        if "gold" not in game_character["inventory"] or not isinstance(game_character["inventory"]["gold"], (int, float)):
            print("FAILED: game_character['inventory'] should contain a numeric 'gold' value")
            print(f"   Actual inventory: {game_character['inventory']}")
            return False
            
        print("PASSED: game_character nested dictionary is correctly structured")
        print(f"   Value: {game_character}")
    except NameError:
        print("FAILED: game_character variable not found")
        return False
        
    # Check gold_amount
    try:
        if gold_amount != game_character["inventory"]["gold"]:
            print("FAILED: gold_amount should equal game_character['inventory']['gold']")
            print(f"   Actual: {gold_amount}")
            print(f"   Expected: {game_character['inventory']['gold']}")
            return False
            
        print(f"PASSED: gold_amount is correct: {gold_amount}")
    except NameError:
        print("FAILED: gold_amount variable not found")
        return False
        
    # Check level_bonuses
    try:
        if not isinstance(level_bonuses, dict):
            print("FAILED: level_bonuses should be a dictionary")
            print(f"   Actual: {type(level_bonuses)}")
            return False
            
        expected_bonuses = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
        if level_bonuses != expected_bonuses:
            print("FAILED: level_bonuses should map levels 1-5 to bonus values (level × 10)")
            print(f"   Actual: {level_bonuses}")
            print(f"   Expected: {expected_bonuses}")
            return False
            
        print("PASSED: level_bonuses dictionary comprehension is correct")
        print(f"   Value: {level_bonuses}")
        return True
    except NameError:
        print("FAILED: level_bonuses variable not found")
        return False

print("\nRunning Task 4 test...")
test_task4()

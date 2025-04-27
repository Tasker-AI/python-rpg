### Lesson Description: ###
# Purpose of the concept: Type conversions allow you to change data from one type to another
# When to use it: Use type conversions when you need to work with data in a different format than it was provided

### Task 1 ###

## Syntax examples ##
# String to number conversions
# score_str = "100"
# score_int = int(score_str)  # Converts to integer: 100
# 
# health_str = "95.5"
# health_float = float(health_str)  # Converts to float: 95.5
# 
# # Number to string conversion
# level = 5
# level_str = str(level)  # Converts to string: "5"

## To Do ##
# Complete the function that processes player data from a text input:
# 1. Convert the player_name_input to a string (it might already be a string, but this ensures it is)
# 2. Convert the player_level_input to an integer
# 3. Convert the player_health_input to a float
# 4. Return all three converted values as a tuple (name, level, health)


def convert_player_data(player_name_input, player_level_input, player_health_input):
    # Your code here
    name = str(player_name_input)
    level = int(player_level_input)
    health = float(player_health_input)

    return (name, level, health)


# Task 1 test #
def test_task1():
    test_cases = [
        # name_input, level_input, health_input, expected_result
        ("Wizard", "10", "95.5", ("Wizard", 10, 95.5)),
        (123, "5", "100.0", ("123", 5, 100.0)),
        ("Knight", 7, "85.5", ("Knight", 7, 85.5)),
        ("Archer", "9", 75, ("Archer", 9, 75.0)),
    ]
    
    for i, (name, level, health, expected) in enumerate(test_cases):
        result = convert_player_data(name, level, health)
        if result != expected:
            print(f"FAILED: Test case {i+1}")
            print(f"   Inputs: name='{name}', level='{level}', health='{health}'")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")
            return False
    
    print("PASSED: All player data conversions are correct!")
    return True

print("\nRunning Task 1 test...")
test_task1()

### Task 2 ###

## Syntax examples ##
# List/Tuple conversions
# coords_list = [10, 20, 30]
# coords_tuple = tuple(coords_list)  # Converts to tuple: (10, 20, 30)
# 
# items_tuple = ("sword", "shield", "potion")
# items_list = list(items_tuple)  # Converts to list: ["sword", "shield", "potion"]
# 
# # String to list conversion
# inventory_str = "sword,shield,potion"
# inventory_list = inventory_str.split(",")  # Creates list: ["sword", "shield", "potion"]
# 
# # List to string conversion
# weapons = ["bow", "arrow", "dagger"]
# weapons_str = ", ".join(weapons)  # Creates string: "bow, arrow, dagger"

## To Do ##
# Complete the function that processes inventory data:
# 1. Convert the inventory_tuple to a list
# 2. Convert the weapon_list to a tuple
# 3. Convert the equipment_str to a list by splitting on commas
# 4. Convert the potion_list to a string joined with " and "
# 5. Return all four converted values as a tuple (inventory_list, weapon_tuple, equipment_list, potion_str)


def convert_inventory_data(inventory_tuple, weapon_list, equipment_str, potion_list):
    # Your code here
    inventory_list = list(inventory_tuple)
    weapons_tuple = tuple(weapon_list)
    equipment_list = list(equipment_str.split(","))
    potion_str = " and ".join(potion_list)
    
    return (inventory_list, weapons_tuple, equipment_list, potion_str)


# Task 2 test #
def test_task2():
    test_cases = [
        # inventory_tuple, weapon_list, equipment_str, potion_list, expected_result
        (
            ("sword", "shield"), 
            ["bow", "arrow"], 
            "helmet,armor,boots", 
            ["health", "mana"], 
            (["sword", "shield"], ("bow", "arrow"), ["helmet", "armor", "boots"], "health and mana")
        ),
        (
            ("axe",), 
            ["staff"], 
            "robe,hat", 
            ["strength"], 
            (["axe"], ("staff",), ["robe", "hat"], "strength")
        ),
        (
            tuple(), 
            [], 
            "", 
            ["invisibility", "speed", "healing"], 
            ([], tuple(), [""], "invisibility and speed and healing")
        ),
    ]
    
    for i, (inv_tuple, weapon_list, equip_str, potion_list, expected) in enumerate(test_cases):
        result = convert_inventory_data(inv_tuple, weapon_list, equip_str, potion_list)
        if result != expected:
            print(f"FAILED: Test case {i+1}")
            print(f"   Inputs: inventory_tuple={inv_tuple}, weapon_list={weapon_list}, equipment_str='{equip_str}', potion_list={potion_list}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")
            return False
    
    print("PASSED: All inventory data conversions are correct!")
    return True

print("\nRunning Task 2 test...")
test_task2()

### Task 3 ###

## Syntax examples ##
# Boolean conversions
# is_active_str = "True"
# is_active_bool = bool(is_active_str)  # Converts to True (any non-empty string is True)
# 
# # Number to boolean
# health = 0
# is_alive = bool(health)  # Converts to False (0 is False, any other number is True)
# 
# # Type checking
# player_name = "Wizard"
# is_string = isinstance(player_name, str)  # Returns True
# is_number = isinstance(player_name, (int, float))  # Returns False

## To Do ##
# Complete the function that processes game status data:
# 1. Convert the health_value to a boolean (is_alive: True if health > 0, False otherwise)
# 2. Convert the mana_str to an integer and then to a boolean (has_mana: True if mana > 0, False otherwise)
# 3. Check if game_mode is a string using isinstance()
# 4. Return all three values as a tuple (is_alive, has_mana, is_string_mode)


def process_game_status(health_value, mana_str, game_mode):
    # Your code here
    health_int = int(health_value)
    if health_int > 0:
        is_alive = True
    else:
        is_alive = False
    mana_int = int(mana_str)
    if mana_int > 0:
        has_mana = bool(True)
    else:
        has_mana = bool(False)
    is_string_mode = isinstance(game_mode, str)
    return (is_alive, has_mana, is_string_mode)


# Task 3 test #
def test_task3():
    test_cases = [
        # health_value, mana_str, game_mode, expected_result
        (100, "50", "adventure", (True, True, True)),
        (0, "0", "battle", (False, False, True)),
        (50, "10", 123, (True, True, False)),
        (-10, "-5", ["survival"], (False, False, False)),
    ]
    
    for i, (health, mana, mode, expected) in enumerate(test_cases):
        result = process_game_status(health, mana, mode)
        if result != expected:
            print(f"FAILED: Test case {i+1}")
            print(f"   Inputs: health_value={health}, mana_str='{mana}', game_mode={mode}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")
            return False
    
    print("PASSED: All game status conversions are correct!")
    return True

print("\nRunning Task 3 test...")
test_task3()

### Task 4 ###

## Syntax examples ##
# Dictionary conversions
# # List of tuples to dictionary
# item_tuples = [("sword", 100), ("shield", 150), ("potion", 50)]
# item_dict = dict(item_tuples)  # Creates: {"sword": 100, "shield": 150, "potion": 50}
# 
# # Dictionary to list of tuples
# inventory = {"bow": 200, "arrow": 5, "armor": 300}
# inventory_items = list(inventory.items())  # Creates: [("bow", 200), ("arrow", 5), ("armor", 300)]
# 
# # Dictionary keys/values to lists
# keys_list = list(inventory.keys())  # Creates: ["bow", "arrow", "armor"]
# values_list = list(inventory.values())  # Creates: [200, 5, 300]

## To Do ##
# Complete the function that processes shop data:
# 1. Convert the price_tuples list to a dictionary
# 2. Convert the discount_dict dictionary to a list of tuples
# 3. Extract the keys from the price_dict into a list
# 4. Extract the values from the price_dict into a list
# 5. Return all four as a tuple (price_dict, discount_tuples, item_names, prices)


def process_shop_data(price_tuples, discount_dict):
    # Your code here
    price_dict = dict(price_tuples)
    discount_tuples = list(tuple(discount_dict.items()))
    item_names = price_dict.keys()
    prices = price_dict.values()
    return (price_dict, discount_tuples, item_names, prices)


# Task 4 test #
def test_task4():
    test_cases = [
        # price_tuples, discount_dict, expected_result
        (
            [("sword", 100), ("shield", 150), ("potion", 50)],
            {"sword": 10, "potion": 5},
            (
                {"sword": 100, "shield": 150, "potion": 50},
                [("sword", 10), ("potion", 5)],
                ["sword", "shield", "potion"],
                [100, 150, 50]
            )
        ),
        (
            [("bow", 200), ("arrow", 5)],
            {"bow": 20},
            (
                {"bow": 200, "arrow": 5},
                [("bow", 20)],
                ["bow", "arrow"],
                [200, 5]
            )
        ),
    ]
    
    for i, (prices, discounts, expected) in enumerate(test_cases):
        result = process_shop_data(prices, discounts)
        
        # Check each part of the result
        if result[0] != expected[0]:
            print(f"FAILED: Test case {i+1} - price_dict incorrect")
            print(f"   Expected: {expected[0]}")
            print(f"   Actual: {result[0]}")
            return False
            
        # For discount_tuples, we need to check if they contain the same items regardless of order
        if sorted(result[1]) != sorted(expected[1]):
            print(f"FAILED: Test case {i+1} - discount_tuples incorrect")
            print(f"   Expected: {sorted(expected[1])}")
            print(f"   Actual: {sorted(result[1])}")
            return False
            
        # For item_names and prices, we need to check if they contain the same items
        if sorted(result[2]) != sorted(expected[2]):
            print(f"FAILED: Test case {i+1} - item_names incorrect")
            print(f"   Expected: {sorted(expected[2])}")
            print(f"   Actual: {sorted(result[2])}")
            return False
            
        if sorted(result[3]) != sorted(expected[3]):
            print(f"FAILED: Test case {i+1} - prices incorrect")
            print(f"   Expected: {sorted(expected[3])}")
            print(f"   Actual: {sorted(result[3])}")
            return False
    
    print("PASSED: All shop data conversions are correct!")
    return True

print("\nRunning Task 4 test...")
test_task4()

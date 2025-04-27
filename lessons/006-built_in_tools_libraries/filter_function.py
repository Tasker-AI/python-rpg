### Lesson Filter Function ###

# Purpose of the concept:
# The filter() function creates an iterator from elements of an iterable for which a function returns True.
# It filters out elements that don't meet a certain condition.

# When to use it:
# - When you need to select only certain elements from a collection
# - When you want to remove elements that don't meet specific criteria
# - As an alternative to list comprehensions with conditions or for loops with if statements


### Exercise ### 
# Create a function called is_legendary_item that takes an item level and returns True if the level is 50 or higher
# (Legendary items are level 50+)

# def function_name(parameter):
#     return boolean_expression
def is_legendary_item(item_level):
    return item_level >= 50


### Exercise ### 
# Use filter() to get only the legendary items from this list of item levels
# Store the result in a variable called legendary_items
# The original list is: [12, 34, 67, 23, 75, 48, 99, 44]

# result = filter(function_name, iterable)
# result_list = list(result)  # Convert filter object to list

item_levels = [12, 34, 67, 23, 75, 48, 99, 44]
legendary_items = list(filter(is_legendary_item, item_levels))


### Exercise ### 
# Create a function called can_equip_item that takes a dictionary representing an item
# and returns True if the player can equip it (player level >= item's required level)
# The player is level 30
# Then use filter() to get only the items the player can equip from the items list
# Store the result in a variable called equippable_items

# def function_name(parameter):
#     return parameter['key'] condition value

def can_equip_item(item):
    return player_level >= item["required_level"]

    
items = [
    {"name": "Iron Sword", "type": "weapon", "required_level": 10},
    {"name": "Dragon Shield", "type": "shield", "required_level": 40},
    {"name": "Leather Boots", "type": "armor", "required_level": 5},
    {"name": "Magic Staff", "type": "weapon", "required_level": 25},
    {"name": "Plate Armor", "type": "armor", "required_level": 35}
]

player_level = 30
equippable_items = list(filter(can_equip_item, items))


# Syntax required:
# def function_name(parameter):
#     return parameter['key'] condition value

# Tests #
def runtests():
    print("Testing your filter() function implementations...")
    
    # Test is_legendary_item function
    test_value = 55
    expected = True
    result = is_legendary_item(test_value)
    print(f"Is level {test_value} legendary? {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    test_value = 45
    expected = False
    result = is_legendary_item(test_value)
    print(f"Is level {test_value} legendary? {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    # Test legendary_items
    expected = [67, 75, 99]
    print(f"Legendary items: {list(legendary_items)}")
    print(f"Expected: {expected}")
    print(f"Test passed: {list(legendary_items) == expected}\n")
    
    # Test can_equip_item function
    test_item = {"name": "Test Sword", "type": "weapon", "required_level": 25}
    expected = True
    result = can_equip_item(test_item)
    print(f"Can equip item with level {test_item['required_level']}? {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    test_item = {"name": "Test Shield", "type": "shield", "required_level": 35}
    expected = False
    result = can_equip_item(test_item)
    print(f"Can equip item with level {test_item['required_level']}? {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    # Test equippable_items
    expected = [
        {"name": "Iron Sword", "type": "weapon", "required_level": 10},
        {"name": "Leather Boots", "type": "armor", "required_level": 5},
        {"name": "Magic Staff", "type": "weapon", "required_level": 25}
    ]
    print(f"Equippable items: {list(equippable_items)}")
    print(f"Expected: {[item['name'] for item in expected]}")
    
    # Check if each expected item is in the result
    result_names = [item["name"] for item in equippable_items]
    expected_names = [item["name"] for item in expected]
    print(f"Test passed: {sorted(result_names) == sorted(expected_names)}")

runtests()

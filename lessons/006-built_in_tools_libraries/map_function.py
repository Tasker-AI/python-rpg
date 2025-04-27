### Lesson Map Function ###

# Purpose of the concept:
# The map() function applies a given function to each item in an iterable (like a list)
# and returns a map object (which can be converted to a list or other iterable).

# When to use it:
# - When you need to transform each element in a list or other iterable
# - When you want to apply the same operation to multiple elements
# - As an alternative to list comprehensions or for loops for simple transformations


# To Do: Create a function called double_damage that takes a damage value and returns double that value
def double_damage(x):
    return int(x) * 2

# Syntax required: 
# def function_name(parameter):
#     return transformed_value


# To Do: Use map() to apply your double_damage function to a list of damage values
# Store the result in a variable called doubled_damages
# The original list is: [12, 45, 32, 64, 7]

damage_values = [12, 45, 32, 64, 7]

doubled_damages = list(map(double_damage, damage_values))



# Syntax required:
# result = map(function_name, iterable)
# result_list = list(result)  # Convert map object to list


# To Do: Create a function called calculate_critical_hit that takes a damage value 
# and returns a string saying "Critical hit! {damage*3} damage dealt!"
# Then use map() to apply this function to the damage_values list
# Store the result in a variable called critical_hit_messages
def calculate_critical_hit(damage):
    return f"Critical hit! {damage * 3} damage dealt!"

critical_hit_messages = list(map(calculate_critical_hit, damage_values))

# Syntax required:
# def function_name(parameter):
#     return f"String with {parameter} interpolated"


# Tests #
def runtests():
    print("Testing your map() function implementations...")
    
    # Test double_damage function
    test_value = 10
    expected = 20
    result = double_damage(test_value)
    print(f"Double damage test: {test_value} -> {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    # Test doubled_damages
    expected = [24, 90, 64, 128, 14]
    print(f"Doubled damages: {list(doubled_damages)}")
    print(f"Expected: {expected}")
    print(f"Test passed: {list(doubled_damages) == expected}\n")
    
    # Test calculate_critical_hit function
    test_value = 10
    expected = "Critical hit! 30 damage dealt!"
    result = calculate_critical_hit(test_value)
    print(f"Critical hit test: {test_value} -> {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    # Test critical_hit_messages
    expected = [
        "Critical hit! 36 damage dealt!",
        "Critical hit! 135 damage dealt!",
        "Critical hit! 96 damage dealt!",
        "Critical hit! 192 damage dealt!",
        "Critical hit! 21 damage dealt!"
    ]
    print(f"Critical hit messages: {list(critical_hit_messages)}")
    print(f"Expected: {expected}")
    print(f"Test passed: {list(critical_hit_messages) == expected}")

runtests()

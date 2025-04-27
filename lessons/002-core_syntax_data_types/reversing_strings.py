### Lesson Reversing Strings ###

# Purpose: Learning how to reverse strings in Python
# When to use: When you need to flip the order of characters in a string,
# such as for text processing, checking palindromes, or creating game puzzles

### Task ###

# To Do: Create a function that reverses a game character's name using string slicing
# Hint: In Python, you can use slicing with a negative step to reverse a string

# Syntax required: string[::-1]

def reverse_name(character_name):
    return character_name[::-1]
    


# To Do: Create a function that reverses a string using a for loop
# This shows how to manually reverse a string by building a new one character by character

# Syntax required: 
# reversed_string = ""
# for char in string:
#     reversed_string = char + reversed_string

def reverse_spell_name(spell_name):
    reversed_string = ""
    for char in spell_name:
        reversed_string = char + reversed_string
    return reversed_string


# To Do: Create a function that reverses a string using the reversed() function and join()
# This is another common way to reverse strings in Python

# Syntax required: 
# "".join(reversed(string))

def reverse_weapon_name(weapon_name):
    return "".join(reversed(weapon_name))


# Tests #
def runtests():
    print("Testing reverse_name...")
    test_name = "Warrior"
    expected = "roirraW"
    result = reverse_name(test_name)
    print(f"Input: {test_name}")
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    print(f"Test passed: {result == expected}")
    
    print("\nTesting reverse_spell_name...")
    test_spell = "Fireball"
    expected = "llaberiF"
    result = reverse_spell_name(test_spell)
    print(f"Input: {test_spell}")
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    print(f"Test passed: {result == expected}")
    
    print("\nTesting reverse_weapon_name...")
    test_weapon = "Excalibur"
    expected = "rubilacxE"
    result = reverse_weapon_name(test_weapon)
    print(f"Input: {test_weapon}")
    print(f"Expected: {expected}")
    print(f"Result: {result}")
    print(f"Test passed: {result == expected}")

runtests() # Tests should be uncommented by default

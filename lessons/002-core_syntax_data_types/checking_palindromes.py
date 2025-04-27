### Lesson Checking Palindromes ###

# Purpose: Learning how to check if a string is a palindrome (reads the same forward and backward)
# When to use: When creating word puzzles, validating special inputs, or implementing
# game mechanics that involve palindromic words or phrases

### Task ###

# To Do: Create a function that checks if a game character name is a palindrome
# A palindrome reads the same forward and backward (ignoring case)
# Example palindromes: "level", "radar", "madam"

# Syntax required: 
# string.lower() - converts string to lowercase
# string == reversed_string - comparing strings

def is_palindrome(character_name):
    lowercase = character_name.lower()
    reversed_string = lowercase[::-1]
    if reversed_string == lowercase:
        return True
    else:
        return False


# To Do: Create a function that checks if a phrase is a palindrome
# This should ignore spaces and be case-insensitive
# Example: "A man a plan a canal Panama" is a palindrome

# Syntax required:
# string.lower() - converts string to lowercase
# string.replace(" ", "") - removes spaces
# for char in string: - iterate through characters

def is_phrase_palindrome(phrase):
    lowercase = phrase.lower()
    cleaned_string = lowercase.replace(" ", "")
    reversed_string = ""
    for char in cleaned_string:
        reversed_string = char + reversed_string
    if reversed_string == cleaned_string:
        return True
    else:
        return False


# To Do: Create a function that finds the longest palindrome substring in a string
# This is a more advanced palindrome challenge

# Syntax required:
# for i in range(len(string)): - iterate through string indices
# string[start:end+1] - get substring
# left, right = i, i - start from center and expand

def find_longest_palindrome(text):
    longest_palindrome = ""
    
    for i in range(len(text)):
        # odd length palindromes
        left, right = i, i
        while left >= 0 and right <len(text) and text[left] == text[right]:
            current_palindrome = text[left:right+1]
            
            if len(current_palindrome) > len(longest_palindrome):
                longest_palindrome = current_palindrome
            
            left -= 1
            right += 1
            
        # Add this for even-length palindromes
        left, right = i, i + 1
        while left >= 0 and right < len(text) and text[left] == text[right]:
            current_palindrome = text[left:right+1]
            if len(current_palindrome) > len(longest_palindrome):
                longest_palindrome = current_palindrome
            left -= 1
            right += 1
    
    return longest_palindrome


# Tests #
def runtests():
    print("Testing is_palindrome...")
    test_cases = [
        ("level", True),
        ("Radar", True),
        ("warrior", False),
        ("Kayak", True),
        ("sword", False)
    ]
    
    for input_str, expected in test_cases:
        result = is_palindrome(input_str)
        print(f"Input: {input_str}")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    print("\nTesting is_phrase_palindrome...")
    test_cases = [
        ("race car", True),
        ("A man a plan a canal Panama", True),
        ("Magic spell cast", False),
        ("No lemon no melon", True)
    ]
    
    for input_str, expected in test_cases:
        result = is_phrase_palindrome(input_str)
        print(f"Input: {input_str}")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    print("\nTesting find_longest_palindrome...")
    test_cases = [
        ("babad", "bab"),  # or "aba" is also valid
        ("cbbd", "bb"),
        ("dragonracecar", "racecar"),
        ("bananas", "anana")
    ]
    
    for input_str, expected in test_cases:
        result = find_longest_palindrome(input_str)
        print(f"Input: {input_str}")
        print(f"Expected: {expected} (or another palindrome of same length)")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected or (len(result) == len(expected) and is_palindrome(result))}")
        print()

runtests() # Tests should be uncommented by default

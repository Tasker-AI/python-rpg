### Lesson Handling Anagrams ###

# Purpose: Learning how to work with anagrams in Python
# When to use: When creating word puzzles, implementing word games,
# or solving problems that involve rearranging letters

### Task ###

# To Do: Create a function that checks if two strings are anagrams of each other
# Anagrams are words that contain the same letters but in a different order
# Example: "listen" and "silent" are anagrams

# Syntax required: 
# sorted(string) - returns a sorted list of characters
# string.lower() - converts string to lowercase

def are_anagrams(word1, word2):
    string1 = sorted(word1.lower())
    string2 = sorted(word2.lower())
    return string1 == string2
    


# To Do: Create a function that finds all anagrams of a word from a list of words
# This function should return a list of all words from the input list that are anagrams of the target word

# Syntax required:
# for word in word_list: - iterate through a list of words
# if condition: result.append(word) - add matching words to result list

def find_anagrams(target_word, word_list):
    result = []
    cleaned_target = sorted(target_word.lower())
    for word in word_list:
        cleaned_word = sorted(word.lower())
        if cleaned_target == cleaned_word:
            result.append(word)
    return result



# To Do: Create a function that generates all possible anagrams of a word
# This is a more advanced anagram challenge using recursion
# For simplicity, we'll limit this to short words (3-4 letters)

# Syntax required:
# if len(word) <= 1: return [word] - base case for recursion
# for i in range(len(word)): - iterate through each position
# first_char = word[i]
# remaining_chars = word[:i] + word[i+1:]
# for perm in generate_anagrams(remaining_chars): - recursive call

def generate_anagrams(word):
    
    # If the word has 0 or 1 characters, there's only one possible arrangement (the word itself)
    if len(word) <= 1:
        return [word]
    
    results = []
    # If the word has 2 or more chars
    for i in range(len(word)):
        first_char = word[i]
        remaining_chars = word[:i] + word[i+1:]
        # For each permutation of the remaining characters
        for perm in generate_anagrams(remaining_chars):  # Recursive call
            # Create a new permutation with the chosen first character
            new_perm = first_char + perm
            # and add it to the results
            results.append(new_perm)
    return results
            


# Tests #
def runtests():
    print("Testing are_anagrams...")
    test_cases = [
        ("listen", "silent", True),
        ("triangle", "integral", True),
        ("sword", "words", True),
        ("hello", "world", False),
        ("Debit Card", "Bad Credit", True)  # Case and space insensitive
    ]
    
    for word1, word2, expected in test_cases:
        result = are_anagrams(word1, word2)
        print(f"Word 1: '{word1}'")
        print(f"Word 2: '{word2}'")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    print("\nTesting find_anagrams...")
    word_list = ["listen", "enlists", "google", "banana", "silent", "inlets", "enlist"]
    target = "listen"
    expected = ["listen", "silent", "inlets"]
    
    result = find_anagrams(target, word_list)
    print(f"Target word: '{target}'")
    print(f"Word list: {word_list}")
    print(f"Expected anagrams: {expected}")
    print(f"Result anagrams: {result}")
    print(f"Test passed: sorted(result) == sorted(expected)")
    print(f"Test passed: {sorted(result) == sorted(expected)}")
    
    print("\nTesting generate_anagrams...")
    test_cases = [
        ("abc", ["abc", "acb", "bac", "bca", "cab", "cba"]),
        ("cat", ["cat", "cta", "act", "atc", "tca", "tac"])
    ]
    
    for word, expected in test_cases:
        result = generate_anagrams(word)
        print(f"Word: '{word}'")
        print(f"Expected anagrams: {sorted(expected)}")
        print(f"Result anagrams: {sorted(result)}")
        print(f"Test passed: {sorted(result) == sorted(expected)}")
        print()

runtests() # Tests should be uncommented by default

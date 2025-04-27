### String Manipulation Exam ###

# This exam covers all the string manipulation techniques you've learned:
# - Reversing strings
# - Checking palindromes
# - Finding substrings
# - Handling anagrams

### Challenge 1: Secret Message Decoder ###

# To Do: Create a function that decodes a secret message by:
# 1. Reversing the string
# 2. Removing all spaces
# 3. Converting to lowercase

# Syntax required: string[::-1], string.replace(), string.lower()

def decode_message(encrypted_message):
    reversed_string = encrypted_message[::-1]
    cleaned_string = reversed_string.replace(" ", "")
    lowercase_string = cleaned_string.lower()
    return lowercase_string
    


### Challenge 2: Spell Checker ###

# To Do: Create a function that checks if a spell name is valid by:
# 1. Checking if it contains the substring "magic" or "spell" (case insensitive)
# 2. Checking that it's not a palindrome (palindrome spells are unstable!)
# 3. Making sure it's between 5 and 15 characters long

# Syntax required: string.lower(), in, len(), palindrome check

def is_valid_spell(spell_name):
    
    lowercase_string = spell_name.lower()
    sorted_string = sorted(lowercase_string)
    
    has_keyword = "magic" in lowercase_string or "spell" in lowercase_string
    
    is_palindrome = lowercase_string == lowercase_string[::-1]    
    
    valid_length = 5 <= len(spell_name) <=15
    
    return has_keyword and not is_palindrome and valid_length
    

### Challenge 3: Weapon Matcher ###

# To Do: Create a function that finds all weapons from an inventory that are anagrams of each other
# Return a list of lists, where each inner list contains a group of anagram weapons
# Example: ["sword", "words", "bow", "shield", "shield"] -> [["sword", "words"], ["shield", "shield"]]

# Syntax required: sorted(), string.lower(), nested loops

def group_weapon_anagrams(weapons):
    # This function groups weapons that are anagrams of each other
    # Example input: ["sword", "words", "bow", "shield", "shield"]
    # Example output: [["sword", "words"], ["bow"], ["shield", "shield"]]
    
    # Dictionary to store anagram groups
    # We'll use sorted characters as keys and lists of weapons as values
    # Example: {"dorsw": ["sword", "words"], "bow": ["bow"], "dehils": ["shield", "shield"]}
    anagram_groups = {}
    
    for weapon in weapons:
        # Sort the characters to identify anagrams
        # Example: "sword" -> "dorsw", "words" -> "dorsw", "bow" -> "bow"
        sorted_chars = ''.join(sorted(weapon.lower()))
        
        # If we've seen this pattern before, add to that group
        # Example: When we see "words", we add it to the "dorsw" group that already has "sword"
        if sorted_chars in anagram_groups:
            anagram_groups[sorted_chars].append(weapon)
            # Example: {"dorsw": ["sword", "words"], ...}
        else:
            # If this is a new pattern, create a new group
            # Example: When we first see "sword", we create {"dorsw": ["sword"]}
            anagram_groups[sorted_chars] = [weapon]        

    # Convert dictionary values to a list of lists
    # Example: {"dorsw": ["sword", "words"], "bow": ["bow"]} -> [["sword", "words"], ["bow"]]
    list_result = list(anagram_groups.values())
    
    # return the list of lists
    return list_result


### Challenge 4: Longest Balanced Name ###

# To Do: Create a function that finds the longest "balanced" character name
# A balanced name has the same number of vowels and consonants
# If there are multiple balanced names of the same length, return the first one

# Syntax required: string operations, counting, loops

def find_longest_balanced_name(character_names):
    longest_balanced = ""
    for word in character_names:
        # Initialize counters for each name
        vowel_count = 0
        const_count = 0
        
        lowercase_word = word.lower()
        for char in lowercase_word:
            if char.isalpha():
                if char in "aeiou":
                    vowel_count += 1
                else:
                    const_count += 1
        if vowel_count == const_count:
            if len(word) > len(longest_balanced):
                longest_balanced = word
    return longest_balanced 


### Challenge 5: Quest Formatter ###

# To Do: Create a function that formats a quest description by:
# 1. Capitalizing the first letter of each sentence
# 2. Replacing all occurrences of "player" with the character's name
# 3. Adding "!" to the end if the quest doesn't already end with punctuation

# Syntax required: string methods, string concatenation, conditionals

def format_quest(quest_description, character_name):
    
    formatted_quest = ""
    
    # Split the quest into sentences
    sentences = quest_description.split(".")
    
    # Process each sentence
    formatted_sentences = []
    
    for sentence in sentences:
        # Skip empty sentences
        if sentence.strip():
            # Capitalize
            capitalized = sentence.strip().capitalize()
            formatted_sentences.append(capitalized)
    
    # Join sentences with periods
    formatted_quest = ". ".join(formatted_sentences)
        
    char_quest = formatted_quest.replace("player", character_name).replace("Player", character_name.capitalize())
    
    if char_quest and char_quest[-1] not in "!.?":
        char_quest += "!"
    
    return char_quest


# Tests #
def runtests():
    # Challenge 1: Secret Message Decoder
    print("Challenge 1: Secret Message Decoder")
    test_cases = [
        ("TSEUQ EHT ETELPMOC", "completethequest"),
        ("Eht Nogard si ni eht Evac", "cavetheinisdragonthe"),
        ("EMIT FO RELUR EHT MA I", "iamtheruleroftime")
    ]
    
    for encrypted, expected in test_cases:
        result = decode_message(encrypted)
        print(f"Encrypted: '{encrypted}'")
        print(f"Expected: '{expected}'")
        print(f"Result: '{result}'")
        print(f"Test passed: {result == expected}")
        print()
    
    # Challenge 2: Spell Checker
    print("\nChallenge 2: Spell Checker")
    test_cases = [
        ("Magic Missile", True),
        ("Abracadabra", False),  # No "magic" or "spell"
        ("Level", False),  # Palindrome
        ("Sp", False),  # Too short
        ("SuperCalifragilisticSpellAlakazam", False)  # Too long
    ]
    
    for spell, expected in test_cases:
        result = is_valid_spell(spell)
        print(f"Spell: '{spell}'")
        print(f"Expected: {expected}")
        print(f"Result: {result}")
        print(f"Test passed: {result == expected}")
        print()
    
    # Challenge 3: Weapon Matcher
    print("\nChallenge 3: Weapon Matcher")
    weapons = ["sword", "words", "bow", "arrow", "worra", "shield", "drows"]
    expected = [["sword", "words", "drows"], ["arrow", "worra"], ["bow"], ["shield"]]
    result = group_weapon_anagrams(weapons)
    
    # Sort for consistent comparison
    expected = [sorted(group) for group in expected]
    expected.sort(key=lambda x: x[0])
    result = [sorted(group) for group in result]
    result.sort(key=lambda x: x[0])
    
    print(f"Weapons: {weapons}")
    print(f"Expected groups: {expected}")
    print(f"Result groups: {result}")
    print(f"Test passed: {result == expected}")
    print()
    
    # Challenge 4: Longest Balanced Name
    print("\nChallenge 4: Longest Balanced Name")
    names = ["Arthur", "Merlin", "Lancelot", "Gawain", "Percival", "Galahad"]
    expected = "Gawain"  # 3 vowels, 3 consonants
    result = find_longest_balanced_name(names)
    print(f"Names: {names}")
    print(f"Expected: '{expected}'")
    print(f"Result: '{result}'")
    print(f"Test passed: {result == expected}")
    print()
    
    # Challenge 5: Quest Formatter
    print("\nChallenge 5: Quest Formatter")
    quest = "find the lost artifact. player must search the ancient ruins"
    character = "Elric"
    expected = "Find the lost artifact. Elric must search the ancient ruins!"
    result = format_quest(quest, character)
    print(f"Original quest: '{quest}'")
    print(f"Character: '{character}'")
    print(f"Expected: '{expected}'")
    print(f"Result: '{result}'")
    print(f"Test passed: {result == expected}")
    print()

runtests() # Tests should be uncommented by default

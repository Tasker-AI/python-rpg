### Lesson: String Manipulations ###

# Purpose: Learn how to manipulate strings in Python
# When to use: When you need to work with text in your game (character names, dialogue, descriptions)

### Task ###

# step 1: String slicing - extract parts of a string
# Syntax: string[start:end:step]
# - start: first index to include (default: 0)
# - end: first index to exclude (default: length of string)
# - step: how many characters to skip (default: 1)
# Examples:
# text = "Python Gaming"
# text[0:6]     # "Python"
# text[7:]      # "Gaming"
# text[:6]      # "Python"
# text[-6:]     # "Gaming"
# text[::2]     # "Pto aig" (every second character)

game_title = "Dragon Quest Adventures"
# Extract just the words "Dragon Quest" from game_title
dragon_quest = game_title[0:12]

# step 2: String methods - join strings together
# Syntax: string.join(iterable)
# - string: the separator to join with
# - iterable: a list or other iterable containing strings
# Examples:
# " ".join(["Hello", "World"])  # "Hello World"
# "-".join(["game", "over"])    # "game-over"
# "".join(["a", "b", "c"])      # "abc"

character_classes = ["Warrior", "Mage", "Archer", "Healer"]
# Join the character classes with commas and the word "and" before the last item
# Result should be: "Warrior, Mage, Archer and Healer"
classes_text = ", ".join(character_classes[0:-1]) + " and " + character_classes[-1]

# step 3: String formatting - create dynamic text
# Syntax: f-strings (Python 3.6+)
# f"Text {variable} more text {expression}"
# Examples:
# name = "Player"
# score = 100
# f"Hello, {name}! Your score is {score}."
# f"Double score: {score * 2}"

player_name = "Alex"
player_level = 7
player_health = 120
player_weapon = "Sword of Truth"
# Create a character status message using all variables
# Should look like: "Alex (Level 7) - Health: 120 - Weapon: Sword of Truth"
status_message = f"{player_name} (Level {player_level}) - Health: {player_health} - Weapon: {player_weapon}"

# Tests #
def run_tests():
    # Test 1: String slicing
    try:
        # Check if dragon_quest exists and has the right value
        if 'dragon_quest' in globals():
            if dragon_quest == "Dragon Quest":
                print("Test 1 passed: Correctly extracted 'Dragon Quest'")
            else:
                print(f"Test 1 failed: Expected 'Dragon Quest', got '{dragon_quest}'")
        else:
            print("Test 1 failed: dragon_quest variable not found")
    except Exception as e:
        print(f"Test 1 error: {e}")

    # Test 2: String joining
    try:
        # Check if classes_text exists and has the right format
        if 'classes_text' in globals():
            expected = "Warrior, Mage, Archer and Healer"
            if classes_text == expected:
                print("Test 2 passed: Correctly joined character classes")
            else:
                print(f"Test 2 failed: Expected '{expected}', got '{classes_text}'")
        else:
            print("Test 2 failed: classes_text variable not found")
    except Exception as e:
        print(f"Test 2 error: {e}")

    # Test 3: String formatting
    try:
        # Check if status_message exists and has the right format
        if 'status_message' in globals():
            expected = "Alex (Level 7) - Health: 120 - Weapon: Sword of Truth"
            if status_message == expected:
                print("Test 3 passed: Correctly formatted status message")
            else:
                print(f"Test 3 failed: Expected '{expected}', got '{status_message}'")
        else:
            print("Test 3 failed: status_message variable not found")
    except Exception as e:
        print(f"Test 3 error: {e}")

run_tests() # Tests should be uncommented by default

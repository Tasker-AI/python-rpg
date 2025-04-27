### Input/Output Exam ###

# This exam tests your knowledge of:
# 1. Getting and validating user input
# 2. Reading from files
# 3. Writing to files
# 4. Formatted output

# You are creating a game save system for "Dragon Quest"
# Complete each function below to pass all tests

# Task 1: Create a function that gets a player name and validates it
# The name must be between 3-10 characters and contain only letters
# Return the valid name or None if invalid
def get_valid_player_name():
    player_name = input("What is your name: ")
    is_valid = len(player_name) >=3 and len(player_name) <= 10 and player_name.isalpha()
    if is_valid:
        return player_name
    else:
        return None


# Task 2: Create a function that reads player data from a file
# The file contains lines with "player_name:level:class"
# Return a list of dictionaries with keys "name", "level", and "class"
# If the file doesn't exist, return an empty list
def read_player_data(filename):
    players_list = []
    try:
        with open(filename, "r") as file:
            content = file.read()
            lines = str(content).split("\n")
            for line in lines:
                if line: 
                    part = line.split(":")
                    if len(part) >= 3:
                        player = {}
                        player["name"] = part[0]
                        player["level"] = part[1]
                        player["class"] = part[2]
                        players_list.append(player)
        
        return players_list
    except FileNotFoundError:
        return []
        
            


# Task 3: Create a function that writes player data to a file
# The function takes a list of player dictionaries and a filename
# Each player should be written as "player_name:level:class"
# Return True if successful, False if there was an error
def write_player_data(players, filename):
    players_string = ""
    for player in players:  
        players_string += f"{player['name']}:{player['level']}:{player['class']}\n"
    try: 
        with open(filename, "w") as file:
            file.write(players_string)      
            return True
    except:
        return False    


# Task 4: Create a function that formats and displays player stats
# The function takes a player dictionary with keys "name", "level", "class"
# Return a formatted string like:
# "PLAYER PROFILE
# Name: [name]
# Level: [level]
# Class: [class]"
def format_player_stats(player):
    formatted_string = f"PLAYER PROFILE\nName: {player['name']}\nLevel: {player['level']}\nClass: {player['class']}"
    
    
    return formatted_string




# Tests #
def run_tests():
    print("Running tests...")
    
    # Test 1: get_valid_player_name
    print("\nTest 1: get_valid_player_name")
    # This test will be skipped as it requires user input
    print("Skipping test 1 as it requires user input")
    print("To manually test: call get_valid_player_name() and enter valid/invalid names")
    
    # Test 2: read_player_data
    print("\nTest 2: read_player_data")
    # Create a test file
    test_file = "test_players.txt"
    with open(test_file, "w") as f:
        f.write("Hero:10:Warrior\n")
        f.write("Mage:8:Wizard\n")
        f.write("Archer:9:Ranger\n")
    
    expected = [
        {"name": "Hero", "level": "10", "class": "Warrior"},
        {"name": "Mage", "level": "8", "class": "Wizard"},
        {"name": "Archer", "level": "9", "class": "Ranger"}
    ]
    result = read_player_data(test_file)
    print(f"Expected: {expected}")
    print(f"Got: {result}")
    print(f"Test passed: {result == expected}")
    
    # Test with non-existent file
    result = read_player_data("non_existent_file.txt")
    print(f"Expected (non-existent file): []")
    print(f"Got: {result}")
    print(f"Test passed: {result == []}")
    
    # Test 3: write_player_data
    print("\nTest 3: write_player_data")
    players = [
        {"name": "Ninja", "level": "12", "class": "Assassin"},
        {"name": "Tank", "level": "15", "class": "Guardian"}
    ]
    test_output_file = "test_output.txt"
    result = write_player_data(players, test_output_file)
    print(f"Write successful: {result}")
    
    # Verify the written file
    with open(test_output_file, "r") as f:
        content = f.read()
    expected_content = "Ninja:12:Assassin\nTank:15:Guardian\n"
    print(f"Expected content: {expected_content}")
    print(f"Actual content: {content}")
    print(f"Content test passed: {content == expected_content}")
    
    # Test 4: format_player_stats
    print("\nTest 4: format_player_stats")
    player = {"name": "DragonSlayer", "level": "20", "class": "Knight"}
    expected_output = "PLAYER PROFILE\nName: DragonSlayer\nLevel: 20\nClass: Knight"
    result = format_player_stats(player)
    print(f"Expected: {expected_output}")
    print(f"Got: {result}")
    print(f"Test passed: {result == expected_output}")
    
    # Clean up test files
    import os
    try:
        os.remove(test_file)
        os.remove(test_output_file)
        print("\nTest files cleaned up successfully")
    except:
        print("\nFailed to clean up test files")
    
    print("\nExam complete!")

run_tests()

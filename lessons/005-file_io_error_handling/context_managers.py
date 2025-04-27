### Lesson: Context Managers (with statements) ###

# Purpose: Context managers provide a clean way to manage resources like files
# When to use: Whenever you need to ensure proper cleanup of resources (especially files)
# Example: Saving/loading game progress without worrying about closing files

### Exercise 1 ### 
# Let's create a function to save a player's score using a context manager
# The with statement automatically handles opening and closing the file
# This is much safer than manually closing files

# In Python, context managers use this pattern:
# with open(filename, mode) as file_variable:
#     file_variable.write(some_data)
# No need to close the file - it happens automatically!

def save_game_score(player_name, score):
    pass


### Exercise 2 ### 
# Now let's implement a function to load the highest score from our save file
# If the file doesn't exist, it should return 0
# Remember: with handles closing the file even if there's an error!

# In Python, you can handle file-not-found errors like this:
# try:
#     with open(filename, mode) as file_variable:
#         # do something with the file
# except FileNotFoundError:
#     # handle case where file doesn't exist

def get_high_score():
    pass


### Exercise 3 ### 
# Let's implement a function to update the high score only if the new score is higher
# This will require both reading and writing to the file
# The function should return True if it's a new high score, False otherwise

# In Python, you can combine file operations and conditionals:
# with open(filename, mode) as file:
#     current_value = int(file.read())
#     if new_value > current_value:
#         # new high score logic

def update_high_score(player_name, new_score):
    pass


# Tests #
def runtests():
    import os
    
    # Test file paths
    SCORE_FILE = "game_scores.txt"
    HIGH_SCORE_FILE = "high_score.txt"
    
    # Clean up any existing test files
    for file in [SCORE_FILE, HIGH_SCORE_FILE]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n=== Testing save_game_score function ===")
    save_game_score("Harry", 1000)
    # Check if file exists and has correct content
    with open(SCORE_FILE, "r") as file:
        content = file.read()
    print(f"File content: {content}")
    expected = "Harry: 1000"
    print(f"Expected: {expected}")
    assert expected in content, f"Save game failed: '{content}' != '{expected}'"
    print("Save game test passed!")
    
    print("\n=== Testing get_high_score function ===")
    # First test when file doesn't exist
    if os.path.exists(HIGH_SCORE_FILE):
        os.remove(HIGH_SCORE_FILE)
    score = get_high_score()
    print(f"Score when file doesn't exist: {score}")
    assert score == 0, f"Expected 0 when file doesn't exist, got {score}"
    
    # Create a file with a score and test again
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write("1500")
    score = get_high_score()
    print(f"Score from file: {score}")
    assert score == 1500, f"Expected 1500, got {score}"
    print("Get high score test passed!")
    
    print("\n=== Testing update_high_score function ===")
    # Test with a lower score (should not update)
    result = update_high_score("Newbie", 1000)
    print(f"Update with lower score (1000 < 1500): {result}")
    assert result == False, "Should return False for lower score"
    with open(HIGH_SCORE_FILE, "r") as file:
        content = file.read()
    print(f"High score after lower score attempt: {content}")
    assert "1500" in content, "High score should not change with lower score"
    
    # Test with a higher score (should update)
    result = update_high_score("Champion", 2000)
    print(f"Update with higher score (2000 > 1500): {result}")
    assert result == True, "Should return True for higher score"
    with open(HIGH_SCORE_FILE, "r") as file:
        content = file.read()
    print(f"High score after higher score attempt: {content}")
    assert "2000" in content, "High score should update with higher score"
    print("Update high score test passed!")
    
    # Clean up test files
    for file in [SCORE_FILE, HIGH_SCORE_FILE]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\nAll tests passed! You've successfully used context managers.")

runtests()

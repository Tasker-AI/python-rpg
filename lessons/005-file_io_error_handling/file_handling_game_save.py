### Lesson: File Handling in Python ###

# Purpose: Learn how to read from and write to files in Python
# When to use: When you need to save game data, load configurations, or process text files

### Task 1: Writing to Files ###

## Syntax examples ##

# To write to a file, you first need to open it with the 'w' mode
# file = open('filename.txt', 'w')
# file.write('Hello, world!')
# file.close()

# A better way is to use the 'with' statement, which automatically closes the file
# with open('filename.txt', 'w') as file:
#     file.write('Hello, world!')

# Common file modes:
# 'w' - Write (creates new file or overwrites existing file)
# 'a' - Append (adds to end of file)
# 'r' - Read (default mode)
# 'r+' - Read and write

## To Do ##

# 1. Create a function called 'save_game' that takes a player name and score

player_name = input("What is your name? ")
score = input("What is the score? ")
# 2. The function should write this data to a file called 'game_scores.txt'
# 3. Each line in the file should be in the format: "player_name:score"
# 4. Use the 'with' statement and 'a' mode to append to the file
def save_game(player_name, score):
    # Hint: The test is looking for format "player_name:score" (no space after colon)
    # Hint: No need for a leading newline on the first entry
    with open('game_scores.txt', 'a') as file:
        file.write(f"\n{player_name}:{score}")

save_game(player_name, score)

# Task 1 test #
def test_task1():
    try:
        # Test if save_game function exists
        if 'save_game' not in globals():
            print("Test failed: save_game function not found")
            return False
            
        # Call the function with test data
        save_game("TestPlayer", 100)
        
        # Check if the file was created and contains the correct data
        with open('game_scores.txt', 'r') as file:
            content = file.read()
            if "TestPlayer:100" in content:
                print("Test passed: Data was correctly written to file")
            else:
                print("Test failed: Data not found in file")
                return False
                
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 2: Reading from Files ###

## Syntax examples ##

# To read an entire file as a string:
# with open('filename.txt', 'r') as file:
#     content = file.read()

# To read a file line by line:
# with open('filename.txt', 'r') as file:
#     for line in file:
#         print(line.strip())  # strip() removes the newline character

# To read all lines into a list:
# with open('filename.txt', 'r') as file:
#     lines = file.readlines()

## To Do ##

# 1. Create a function called 'get_high_score' that takes no parameters
def get_high_score():
   
    # 2. The function should read the 'game_scores.txt' file
    try: 
        with open('game_scores.txt', 'r') as file:
            highscore_name = ""
            highscore = 0
            # 3. Parse each line to extract player names and scores
            for line in file:
                try:
                    name, score = line.split(':')
                    score = int(score)
                    if score >= highscore:
                        highscore = score
                        highscore_name = name
                except ValueError:
                    # Skip this line and continue with the next one
                    continue
            
            # 4. Return the name and score of the player with the highest score    
            return (highscore_name, highscore)
            
    # 5. If the file doesn't exist or is empty, return None
    except FileNotFoundError:
        print("File not found")
        return None


print(get_high_score())

## Task 2 test ##
def test_task2():
    try:
        # Test if get_high_score function exists
        if 'get_high_score' not in globals():
            print("Test failed: get_high_score function not found")
            return False
            
        # Add some test scores
        with open('game_scores.txt', 'w') as file:
            file.write("Player1:150\n")
            file.write("Player2:300\n")
            file.write("Player3:200\n")
        
        # Call the function and check the result
        high_score = get_high_score()
        if high_score is None:
            print("Test failed: Function returned None")
            return False
            
        name, score = high_score
        if name == "Player2" and score == 300:
            print("Test passed: Correctly identified the highest score")
        else:
            print(f"Test failed: Expected ('Player2', 300) but got ({name}, {score})")
            return False
            
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


### Task 3: File Error Handling ###

## Syntax examples ##

# When working with files, it's important to handle errors properly
# try:
#     with open('nonexistent_file.txt', 'r') as file:
#         content = file.read()
# except FileNotFoundError:
#     print("The file doesn't exist")
# except PermissionError:
#     print("You don't have permission to access this file")
# except Exception as e:
#     print(f"An error occurred: {e}")

## To Do ##

# 1. Create a function called 'safe_delete_score' that takes a player name
def safe_delete_score(player_name):
    # 2. The function should:
    #    - Try to read the game_scores.txt file
    try:
        
        
        with open('game_scores.txt', 'r') as file:
            
            # Read all lines into a list first
            content = file.read().split('\n')
            
            # Create a new list with only lines that don't contain player_name
            new_list = []
            
            # Remove any lines containing the given player name
            for line in content:
                if player_name not in line:
                    new_list.append(line)
                    
            # join the new_list into a string
            output = "\n".join(new_list)
            
        with open('game_scores.txt', 'w') as file:
            # Write the remaining lines back to the file
            file.write(output) 
            
        # 4. Return True if successful, False if an error occurred
        return True
        
    # 3. Handle at least two types of errors: FileNotFoundError and another of your choice
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("You don't have permission to access this file")
    except Exception as e:
        print(f"An error occurred: {e}")
    # 4. Return True if successful, False if an error occurred
    return False
            
    

safe_delete_score("jim")

## Task 3 test ##
def test_task3():
    try:
        # Test if safe_delete_score function exists
        if 'safe_delete_score' not in globals():
            print("Test failed: safe_delete_score function not found")
            return False
            
        # Set up test data
        with open('game_scores.txt', 'w') as file:
            file.write("PlayerA:100\n")
            file.write("PlayerB:200\n")
            file.write("PlayerC:300\n")
        
        # Test deleting an existing player
        result = safe_delete_score("PlayerB")
        if not result:
            print("Test failed: Function returned False when it should have succeeded")
            return False
            
        # Check if the player was deleted
        with open('game_scores.txt', 'r') as file:
            content = file.read()
            if "PlayerB" in content:
                print("Test failed: PlayerB was not deleted from the file")
                return False
            else:
                print("Test passed: PlayerB was successfully deleted")
        
        # Test the function's error handling by deleting the file
        import os
        os.remove('game_scores.txt')
        
        # Try to delete a player from a non-existent file
        result = safe_delete_score("PlayerC")
        if result:
            print("Test failed: Function returned True when file doesn't exist")
            return False
        else:
            print("Test passed: Function correctly handled missing file")
            
        return True
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False


# Run all tests
def run_tests():
    print("\n=== Running Tests ===")
    task1_passed = test_task1()
    task2_passed = test_task2()
    task3_passed = test_task3()
    
    if task1_passed and task2_passed and task3_passed:
        print("\nAll tests passed! Your game save system is working!")
    else:
        print("\nSome tests failed. Check your code and try again!")

run_tests()
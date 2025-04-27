### Lesson - Binary Search and Recursion ###

# Purpose: Binary search quickly finds elements in sorted collections with O(log n) time complexity
# When to use: For efficient searching in large sorted collections like high scores or item databases
# Example: Finding a player's rank in a sorted leaderboard or searching for items by level

# Binary search works by repeatedly dividing the search interval in half:
# 1. Compare the target value with the middle element of the array
# 2. If they match, return the middle index
# 3. If the target is less than the middle, search the left half
# 4. If the target is greater than the middle, search the right half
# 5. Repeat until the element is found or the interval is empty

import bisect

### Exercise 1 ###
# Implement an iterative binary search function that:
# 1. Takes a sorted list of high scores and a target score
# 2. Returns the index if the target score is found
# 3. Returns -1 if the target is not in the list

# Example of binary search (iterative approach):
# def binary_search(arr, target):
#     left, right = 0, len(arr) - 1
#     
#     while left <= right:
#         mid = (left + right) // 2  # Find middle index
#         
#         if arr[mid] == target:
#             return mid
#         elif arr[mid] < target:
#             left = mid + 1  # Search right half
#         else:
#             right = mid - 1  # Search left half
#             
#     return -1  # Target not found

def find_high_score(high_scores, target_score):
    left = 0
    right = len(high_scores) -1
    
    while left <= right:
        mid = (left + right) // 2
        
        if high_scores[mid] == target_score:
            return mid
        elif high_scores[mid] < target_score:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1


### Exercise 2 ###
# Implement a recursive binary search function that:
# 1. Takes a sorted list of player levels, a target level, and optionally start/end indices
# 2. Returns the index if the target level is found
# 3. Returns -1 if the target is not in the list
# 4. Uses recursion instead of a loop

# Example recursive function structure:
# def recursive_function(data, target, start=0, end=None):
#     # Base case - when to stop recursion
#     if start > end:
#         return -1
#         
#     # Recursive case - call function again with modified parameters
#     mid = (start + end) // 2
#     
#     if data[mid] == target:
#         return mid
#     elif data[mid] < target:
#         return recursive_function(data, target, mid + 1, end)
#     else:
#         return recursive_function(data, target, start, mid - 1)

def find_player_level(player_levels, target_level, start=0, end=None):
    if end is None:
        end = len(player_levels) - 1
    
    if start > end:
        return -1
    
    mid = (start + end) // 2
    
    if player_levels[mid] == target_level:
        return mid
    elif player_levels[mid] < target_level:
        return find_player_level(player_levels, target_level, mid + 1, end)
    else:
        return find_player_level(player_levels, target_level, start, mid - 1)



### Exercise 3 ###
# Create a function to find all players within a level range that:
# 1. Takes a sorted list of player levels and min/max level values
# 2. Returns a new list with players whose levels are between min and max (inclusive)
# 3. Uses binary search to efficiently find the start and end positions

def find_players_in_level_range(player_levels, min_level, max_level):
    # Find leftmost position to insert min_level
    left_pos = bisect.bisect_left(player_levels, min_level)
    
    # Find rightmost position to insert max_level
    right_pos = bisect.bisect_right(player_levels, max_level)
    
    # Return the slice between these positions
    return player_levels[left_pos:right_pos]


# Tests #
def runtests():
    # Test Exercise 1: Iterative binary search
    high_scores = [1000, 1500, 2250, 2800, 3300, 4100, 5000, 6200]
    print("Test 1: Iterative binary search")
    print(f"Expected index of 3300: 4, Got: {find_high_score(high_scores, 3300)}")
    print(f"Expected index of 2250: 2, Got: {find_high_score(high_scores, 2250)}")
    print(f"Expected index of 9999 (not in list): -1, Got: {find_high_score(high_scores, 9999)}")
    scores_test_passed = (find_high_score(high_scores, 3300) == 4 and 
                          find_high_score(high_scores, 2250) == 2 and 
                          find_high_score(high_scores, 9999) == -1)
    print(f"Test passed: {scores_test_passed}")
    
    # Test Exercise 2: Recursive binary search
    player_levels = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    end_index = len(player_levels) - 1
    print("\nTest 2: Recursive binary search")
    print(f"Expected index of level 25: 4, Got: {find_player_level(player_levels, 25, 0, end_index)}")
    print(f"Expected index of level 5: 0, Got: {find_player_level(player_levels, 5, 0, end_index)}")
    print(f"Expected index of level 99 (not in list): -1, Got: {find_player_level(player_levels, 99, 0, end_index)}")
    level_test_passed = (find_player_level(player_levels, 25, 0, end_index) == 4 and 
                         find_player_level(player_levels, 5, 0, end_index) == 0 and 
                         find_player_level(player_levels, 99, 0, end_index) == -1)
    print(f"Test passed: {level_test_passed}")
    
    # Test Exercise 3: Finding players in range
    all_player_levels = [5, 12, 15, 18, 22, 27, 33, 38, 42, 50, 62, 70]
    print("\nTest 3: Finding players in level range")
    players_20_40 = find_players_in_level_range(all_player_levels, 20, 40)
    expected_levels = [22, 27, 33, 38]
    print(f"Expected levels between 20-40: {expected_levels}")
    print(f"Got: {players_20_40}")
    range_test_passed = (len(players_20_40) == len(expected_levels) and 
                         all(level in players_20_40 for level in expected_levels))
    print(f"Test passed: {range_test_passed}")
    
    # Bonus: Performance comparison between linear and binary search
    import time
    import random
    
    # Create a large sorted list for testing
    large_list = list(range(0, 1000000, 2))  # Sorted list of even numbers
    target = 999998  # Last element
    
    # Linear search time
    start = time.time()
    linear_result = -1
    for i, num in enumerate(large_list):
        if num == target:
            linear_result = i
            break
    linear_time = (time.time() - start) * 1000
    
    # Binary search time
    start = time.time()
    binary_result = find_high_score(large_list, target)
    binary_time = (time.time() - start) * 1000
    
    print("\nPerformance Comparison (1,000,000 elements):")
    print(f"Linear search time: {linear_time:.2f} ms")
    print(f"Binary search time: {binary_time:.2f} ms")
    print(f"Binary search is {linear_time/binary_time:.1f}x faster!")
    
    # Verify both methods found the correct result
    print(f"Both searches found the target at index {linear_result}: {linear_result == binary_result}")

runtests()

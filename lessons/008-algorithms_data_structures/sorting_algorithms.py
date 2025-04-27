### Lesson - Sorting Algorithms and Dynamic Programming ###

# Purpose: Understand efficient sorting algorithms and basic dynamic programming concepts
# When to use: When you need to organize game data (leaderboards, inventory, enemies by difficulty)
# Example: Sorting player scores, optimizing game resources, or calculating optimal paths

# There are many sorting algorithms with different time complexities:
# - Quicksort: O(n log n) average case, O(n²) worst case
# - Mergesort: O(n log n) guaranteed
# - Bubblesort: O(n²) - simple but inefficient for large datasets

# Python has a built-in sorted() function that uses Timsort (combination of mergesort and insertion sort)

### Exercise 1 ###
# Implement quicksort to sort a list of player scores:
# 1. Select a pivot element from the list
# 2. Partition the list into elements less than pivot and greater than pivot
# 3. Recursively sort both partitions
# 4. Return the combined sorted list

# Example quicksort implementation:
# def quicksort(arr):
#     if len(arr) <= 1:
#         return arr
#     
#     pivot = arr[len(arr) // 2]
#     left = [x for x in arr if x < pivot]
#     middle = [x for x in arr if x == pivot]
#     right = [x for x in arr if x > pivot]
#     
#     return quicksort(left) + middle + quicksort(right)

def sort_player_scores(scores):
    if len(scores) <= 1:
        return scores
    
    pivot = scores[len(scores) // 2]
    left = [x for x in scores if x < pivot]
    middle = [x for x in scores if x == pivot]
    right = [x for x in scores if x > pivot]
    
    return sort_player_scores(left) + middle + sort_player_scores(right)


### Exercise 2 ###
# Implement a function to find the nth highest score in a list:
# 1. Use your quicksort function to sort the scores
# 2. Return the nth highest score (1st highest is the maximum)
# 3. Handle edge cases (n larger than list size, empty list, etc.)

def find_nth_highest_score(scores, n):
    if len(scores) == 0:
        raise ValueError("Cannot find nth highest score in an empty list")
        
    if n > len(scores):
        raise ValueError(f"Cannot find position {n} in a list of size {len(scores)}")
    
    sorted_scores = sort_player_scores(scores)
    return sorted_scores[len(sorted_scores) - n]


### Exercise 3 ###
# Dynamic Programming Example: Implement a memoized function to calculate 
# the optimal damage for a sequence of attacks with cooldowns
# 1. Takes a list of (damage, cooldown) tuples representing attacks
# 2. Calculates maximum damage possible in a given time
# 3. Uses memoization to avoid recalculating the same subproblems

# Example memoization:
# def memoized_function(n, memo={}):
#     if n in memo:
#         return memo[n]  # Return cached result
#     
#     # Calculate result for n
#     result = ...
#     
#     memo[n] = result    # Cache the result
#     return result

def calculate_optimal_damage(attacks, time_limit, memo = None):
    
    if memo is None:
        memo = {}
        
    # Base case: if we have no time left    
    if time_limit <= 0:
        return 0
    
    # Check if we've already calculated this
    if time_limit in memo:
        return memo[time_limit]
    
    # Try each attack and find the best one
    max_damage = 0
    for damage, cooldown in attacks:
        if cooldown <= time_limit:
            # Damage from this attack + best damage we can do with remaining time
            current_damage = damage + calculate_optimal_damage(
                attacks, 
                time_limit - cooldown, 
                memo
            )
            max_damage = max(max_damage, current_damage)
    
    # Save the result in our memo dictionary
    memo[time_limit] = max_damage
    return max_damage


# Tests #
def runtests():
    # Test Exercise 1: Quicksort
    scores = [5000, 1000, 8000, 3000, 2000, 4000, 7000, 6000]
    sorted_scores = sort_player_scores(scores)
    expected_scores = sorted(scores)  # Using Python's built-in sorting
    
    print("Test 1: Quicksort")
    print(f"Original scores: {scores}")
    print(f"Your sorted scores: {sorted_scores}")
    print(f"Expected sorted scores: {expected_scores}")
    sort_test_passed = (sorted_scores == expected_scores)
    print(f"Test passed: {sort_test_passed}")
    
    # Test Exercise 2: Finding nth highest score
    print("\nTest 2: Finding nth highest score")
    print(f"3rd highest score: {find_nth_highest_score(scores, 3)}")
    print(f"1st highest score: {find_nth_highest_score(scores, 1)}")
    print(f"8th highest score: {find_nth_highest_score(scores, 8)}")
    # Error case
    try:
        invalid_result = find_nth_highest_score(scores, 10)
        nth_test_passed = False
        print(f"Expected error for invalid n, Got: {invalid_result}")
    except ValueError:
        nth_test_passed = True
        print("Correctly raised ValueError for invalid n")
    print(f"Test passed: {nth_test_passed and find_nth_highest_score(scores, 3) == 6000 and find_nth_highest_score(scores, 1) == 8000}")
    
    # Test Exercise 3: Dynamic Programming
    attacks = [(50, 1), (100, 2), (150, 3)]  # (damage, cooldown) tuples
    time_limit = 5
    
    print("\nTest 3: Dynamic Programming - Optimal Damage")
    optimal_damage = calculate_optimal_damage(attacks, time_limit)
    
    # Expected result:
    # With 5 time units, we can use attack[1] (100 dmg, 2 cooldown) twice
    # and attack[0] (50 dmg, 1 cooldown) once for a total of 250 damage
    expected_damage = 250
    
    print(f"Attacks: {attacks}")
    print(f"Time limit: {time_limit}")
    print(f"Your calculated optimal damage: {optimal_damage}")
    print(f"Expected optimal damage: {expected_damage}")
    dp_test_passed = (optimal_damage == expected_damage)
    print(f"Test passed: {dp_test_passed}")
    
    # Performance test for memoization
    import time
    
    print("\nPerformance test: Memoized vs Non-memoized")
    
    # Generate a larger problem
    large_attacks = [(i*10, i) for i in range(1, 11)]  # 10 different attacks
    large_time = 20
    
    # Time the memoized version
    start = time.time()
    result_memo = calculate_optimal_damage(large_attacks, large_time)
    memo_time = (time.time() - start) * 1000
    
    print(f"Memoized calculation time: {memo_time:.2f} ms")
    print(f"Optimal damage for large problem: {result_memo}")

runtests()

### Lesson - Big O Notation Basics ###

# Purpose: Big O notation describes the performance or complexity of an algorithm
# When to use: When analyzing or optimizing algorithms for game systems
# Example: Deciding which algorithm to use for pathfinding or inventory searching

# Common Big O notations:
# O(1)      - Constant time (fastest, doesn't change with input size)
# O(log n)  - Logarithmic time (very efficient, often in binary search operations)
# O(n)      - Linear time (scales linearly with input size)
# O(n log n)- Linearithmic time (efficient sorts like merge sort)
# O(n²)     - Quadratic time (slower, often in nested loops)
# O(2^n)    - Exponential time (very slow, often in recursive algorithms)

### Exercise 1 ###
# Implement a constant time (O(1)) function that:
# 1. Takes a list of player scores and an index
# 2. Returns the player score at that index
# 3. Returns -1 if the index is invalid

def get_player_score(scores, index):
    if 0 <= index < len(scores):
        return scores[index]
    else:
        return -1


### Exercise 2 ###
# Implement a linear time (O(n)) function that:
# 1. Takes a list of item names and a target item
# 2. Returns the index of the target in the list
# 3. Returns -1 if the target is not found

# Example O(n) search - iterate through each element once:
# def linear_search(items, target):
#     for i in range(len(items)):
#         if items[i] == target:
#             return i
#     return -1

def find_item(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


### Exercise 3 ###
# Implement a quadratic time (O(n²)) function that:
# 1. Takes a list of enemy coordinates (tuples of x, y positions)
# 2. Returns a list of distances between each pair of enemies
# 3. Distance formula: sqrt((x2-x1)²+(y2-y1)²) simplified as (x2-x1)²+(y2-y1)²
#    (We'll skip the square root for simplicity)

def calculate_enemy_distances(enemy_coords):
    distances = []
    
    for i in range(len(enemy_coords)):

        for j in range(i+1, len(enemy_coords)):
            x1, y1 = enemy_coords[i]
            x2, y2 = enemy_coords[j]
            distance = (x2-x1)**2 + (y2-y1)**2
            distances.append(distance)
    
    return distances


# Tests #
def runtests():
    # Test Exercise 1: O(1) constant time access
    scores = [5000, 7500, 10000, 12500, 15000]
    print("Test 1: Constant time access O(1)")
    print(f"Expected score at index 2: 10000, Got: {get_player_score(scores, 2)}")
    print(f"Expected score for invalid index: -1, Got: {get_player_score(scores, 10)}")
    print(f"Test passed: {get_player_score(scores, 2) == 10000 and get_player_score(scores, 10) == -1}")
    
    # Test Exercise 2: O(n) linear time search
    items = ["Sword", "Shield", "Potion", "Map", "Compass"]
    print("\nTest 2: Linear time search O(n)")
    print(f"Expected index of 'Potion': 2, Got: {find_item(items, 'Potion')}")
    print(f"Expected index of 'Gold': -1, Got: {find_item(items, 'Gold')}")
    print(f"Test passed: {find_item(items, 'Potion') == 2 and find_item(items, 'Gold') == -1}")
    
    # Test Exercise 3: O(n²) quadratic time calculation
    enemies = [(1, 1), (4, 5), (7, 2)]
    expected = [25, 37, 18]  # Distances: (1,1)->(4,5), (1,1)->(7,2), (4,5)->(7,2)
    distances = calculate_enemy_distances(enemies)
    
    print("\nTest 3: Quadratic time calculation O(n²)")
    print(f"Expected distances: {expected}")
    print(f"Got distances: {distances}")
    all_match = True
    for i in range(len(expected)):
        if expected[i] not in distances:
            all_match = False
            break
    print(f"Test passed: {all_match and len(distances) == len(expected)}")
    
    # Bonus: Performance demonstration
    import time
    
    # O(n) performance
    print("\nPerformance Demonstration:")
    sizes = [1000, 10000, 100000]
    for size in sizes:
        big_list = list(range(size))
        target = size-1  # Worst case scenario
        
        start = time.time()
        result = find_item(big_list, target)
        end = time.time()
        
        print(f"Linear search O(n) with {size} elements: {(end-start)*1000:.2f} ms")

runtests()

import heapq

### Lesson: Heaps (using heapq) ###

# Purpose: To understand and use heaps, specifically min-heaps, via Python's `heapq` module.
# A min-heap is a specialized tree-based data structure where the smallest element is always at the root.
# When to use: Excellent for implementing priority queues, finding the smallest/largest elements efficiently, 
# and certain graph algorithms (like Dijkstra's).
# Example use case: In a game, managing events based on time (e.g., monster spawns, buff expirations) 
# where you always want to process the soonest event first.


### Exercise 1: Create a Min-Heap (heapify) ###
# Task: You have a list of enemy spawn times (in seconds). Convert this list into a min-heap 
#       so the earliest spawn time is easily accessible.
# Syntax: heapq.heapify(list_instance) # Modifies the list in-place

spawn_times = [120, 45, 90, 30, 60] 
# Convert spawn_times into a min-heap below
heapq.heapify(spawn_times)


### Exercise 2: Add an Event (heappush) ###
# Task: A special event triggers a new enemy spawn at 15 seconds. Add this time to the heap.
# Syntax: heapq.heappush(heap, item)

new_spawn_time = 15
# Add new_spawn_time to the spawn_times heap below
heapq.heappush(spawn_times, new_spawn_time)

### Exercise 3: Process the Next Event (heappop) ###
# Task: Get the earliest spawn time from the heap (process the event) and assign it to `next_spawn`.
#       `heappop` removes and returns the smallest item.
# Syntax: smallest_item = heapq.heappop(heap)

next_spawn = heapq.heappop(spawn_times)
# Pop the smallest item from spawn_times and assign it to next_spawn below


### Exercise 4: Peek at the Next Event ###
# Task: Check the time of the *next* earliest spawn event without removing it from the heap.
#       Assign this time to `peek_next_spawn`.
# Syntax: smallest_item = heap[0] # Accessing the first element (root)

peek_next_spawn = spawn_times[0]
# Get the smallest item (without removing) and assign it to peek_next_spawn below


### Exercise 5: Find N Largest Times (nlargest) ###
# Task: Find the 3 latest spawn times remaining in the heap.
#       Assign the result (a list) to `latest_3_spawns`.
# Syntax: largest_items = heapq.nlargest(n, iterable) # Note: works on any iterable, not just heaps

latest_3_spawns = heapq.nlargest(3, spawn_times)
# Find the 3 largest times in spawn_times and assign to latest_3_spawns below


# --- Tests --- #
def run_tests():
    print("Running Heap (heapq) Tests...")
    passed_tests = 0
    total_tests = 5
    
    # Need a fresh copy for some tests
    original_spawn_times = [120, 45, 90, 30, 60]
    current_heap = list(original_spawn_times) # Create a copy
    
    # Test Exercise 1
    try:
        heapq.heapify(current_heap) # Apply heapify to the copy
        # Check heap property (smallest is root) - a basic check
        if current_heap[0] == 30:
            print("Exercise 1: Passed - List successfully heapified (smallest is root).")
            passed_tests += 1
        else:
            print(f"Exercise 1: Failed - heapify did not place smallest element at root.")
            print(f"  Heap after heapify starts with: {current_heap[0] if current_heap else 'empty'}")
            print(f"  Expected root: 30")
    except Exception as e:
        print(f"Exercise 1: Failed with error - {e}")
        
    # Test Exercise 2 (continues on current_heap)
    try:
        new_time = 15
        heapq.heappush(current_heap, new_time)
        if current_heap[0] == new_time:
            print("Exercise 2: Passed - New smallest item pushed correctly.")
            passed_tests += 1
        else:
             print(f"Exercise 2: Failed - heappush did not result in the new smallest item at root.")
             print(f"  Heap root after push: {current_heap[0] if current_heap else 'empty'}")
             print(f"  Expected root: {new_time}")
    except Exception as e:
        print(f"Exercise 2: Failed with error - {e}")

    # Test Exercise 3 (continues on current_heap)
    try:
        popped_item = heapq.heappop(current_heap)
        expected_pop = 15
        # Check popped item AND the new root
        if popped_item == expected_pop and current_heap[0] == 30:
            print("Exercise 3: Passed - Smallest item popped correctly, heap property maintained.")
            passed_tests += 1
        else:
            print(f"Exercise 3: Failed - heappop did not return correct item or maintain heap.")
            print(f"  Expected popped: {expected_pop}, Got popped: {popped_item}")
            print(f"  Expected new root: 30, Got new root: {current_heap[0] if current_heap else 'empty'}")
    except Exception as e:
         print(f"Exercise 3: Failed with error - {e}")
        
    # Test Exercise 4 (uses the state of current_heap from Exercise 3)
    try:
        peeked_item = current_heap[0]
        expected_peek = 30
        if peeked_item == expected_peek:
             print("Exercise 4: Passed - Peeked at the correct smallest item.")
             passed_tests += 1
        else:
            print(f"Exercise 4: Failed - Peek returned incorrect item.")
            print(f"  Expected peek: {expected_peek}")
            print(f"  Got peek:      {peeked_item}")
    except IndexError:
         print(f"Exercise 4: Failed - Heap is empty, cannot peek.")
    except Exception as e:
        print(f"Exercise 4: Failed with error - {e}")
        
    # Test Exercise 5 (uses the state of current_heap from Exercise 3)
    try:
        # Use the 'latest_3_spawns' variable the user is supposed to create
        # Ensure the variable exists and is assigned
        if 'latest_3_spawns' in globals():
            user_latest_3 = latest_3_spawns
            expected_latest_3 = sorted([120, 90, 60], reverse=True) # nlargest returns sorted list
            # heapq.nlargest returns sorted list, so direct comparison works
            if user_latest_3 == expected_latest_3:
                 print("Exercise 5: Passed - Found the 3 largest items correctly.")
                 passed_tests += 1
            else:
                print(f"Exercise 5: Failed - nlargest result incorrect.")
                print(f"  Expected: {expected_latest_3}")
                print(f"  Got:      {user_latest_3}")
        else:
            print("Exercise 5: Failed - Variable 'latest_3_spawns' not found or assigned.")
            
    except Exception as e:
         print(f"Exercise 5: Failed with error - {e}")

    print(f"\nHeap (heapq) Tests Finished. Passed {passed_tests}/{total_tests}.")

# Run tests
run_tests()

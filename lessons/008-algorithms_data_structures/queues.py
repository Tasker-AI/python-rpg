### Lesson: Queues (using collections.deque) ###

# Purpose: To understand and implement the Queue data structure (FIFO - First-In, First-Out)
# using the efficient `collections.deque` object. Queues are essential for managing
# tasks or items in the order they arrive.

# When to use it:
# - Print job queues.
# - Task scheduling (processing tasks in order received).
# - Web server request handling.
# - Breadth-First Search (BFS) graph traversal algorithms.

# Why `collections.deque`?
# - Lists are inefficient for `pop(0)` (removing from the start).
# - `deque` provides fast O(1) appends and pops from both ends.

# `deque` operations for a Queue:
# - Import: `from collections import deque`
# - Initialize: `my_queue = deque()`
# - Enqueue (add to back): `my_queue.append(item)`
# - Dequeue (remove from front): `item = my_queue.popleft()`
# - Peek (view front): `front_item = my_queue[0]` (Check if not empty first!)

from collections import deque # Import deque

### Exercise 1: Enqueue Players ###
# Task: Players are joining a game lobby queue.
# Start with an empty deque `lobby_queue`. Enqueue 'Alice', then 'Bob', then 'Charlie'.
# Syntax: queue_deque.append(item)

lobby_queue = deque()
# Enqueue 'Alice'
lobby_queue.append("Alice")
# Enqueue 'Bob'
lobby_queue.append("Bob")
# Enqueue 'Charlie'
lobby_queue.append("Charlie")

### Exercise 2: Dequeue Players ###
# Task: The game is starting, let the first player in the queue join.
# Dequeue one player from the front of `lobby_queue` created in Exercise 1.
# Store the dequeued player in `first_player_to_join`.
# Syntax: dequeued_item = queue_deque.popleft()

first_player_to_join = lobby_queue.popleft() # Dequeue from lobby_queue


### Exercise 3: Peek at the Next Player ###
# Task: See who is next in line without removing them from the queue.
# Access the front element (index 0) of `lobby_queue` (after the dequeue in Ex 2)
# and store it in `next_player_in_line`. Check if the queue is empty first!
# Syntax: if queue_deque: front_item = queue_deque[0]

if lobby_queue:
    next_player_in_line = lobby_queue[0] # Peek at lobby_queue[0] if not empty


# Tests #
def run_tests():
    print("Running Queue Tests...\n")
    # Note: These tests assume exercises are run sequentially and modify the same queue
    global lobby_queue, first_player_to_join, next_player_in_line

    # Test Exercise 1 Results (before dequeue)
    print("--- Testing Exercise 1: Enqueue ---")
    # Reconstruct expected queue state after pushes
    expected_queue_after_enqueue = deque(['Alice', 'Bob', 'Charlie'])
    # Infer state before dequeue
    current_queue_before_dequeue = deque()
    if first_player_to_join is not None:
         # If dequeue happened, add the dequeued item back to the left
         current_queue_before_dequeue.appendleft(first_player_to_join)
    # Add the rest of the current queue items
    current_queue_before_dequeue.extend(lobby_queue)

    if current_queue_before_dequeue == expected_queue_after_enqueue:
        print("Exercise 1: Passed (Queue after enqueues seems correct)")
    else:
        print(f"Exercise 1: Failed - Queue state after enqueues is unexpected.")
        print(f"  Expected after enqueues: {list(expected_queue_after_enqueue)}")
        print(f"  Inferred state: {list(current_queue_before_dequeue)}")
        print(f"  (Current queue is: {list(lobby_queue)}, First dequeued was: {first_player_to_join})")
    print("-" * 20)


    # Test Exercise 2 Results
    print("--- Testing Exercise 2: Dequeue ---")
    expected_dequeued_item = 'Alice'
    if first_player_to_join == expected_dequeued_item:
        print("Exercise 2: Passed")
    else:
        print(f"Exercise 2: Failed - Dequeued item mismatch.")
        print(f"  Expected dequeued: {expected_dequeued_item}")
        print(f"  Got:               {first_player_to_join}")
    print("-" * 20)

    # Test Exercise 3 Results
    print("--- Testing Exercise 3: Peek ---")
    expected_queue_after_dequeue = deque(['Bob', 'Charlie'])
    expected_peek_item = 'Bob' # Front item after 'Alice' was dequeued

    if lobby_queue != expected_queue_after_dequeue:
         print(f"Exercise 3: Failed - Queue state after dequeue is incorrect.")
         print(f"  Expected queue: {list(expected_queue_after_dequeue)}")
         print(f"  Current queue:  {list(lobby_queue)}")
    elif not lobby_queue: # Check if queue became unexpectedly empty
        print(f"Exercise 3: Failed - Queue is empty, cannot peek.")
    elif next_player_in_line == expected_peek_item:
        print("Exercise 3: Passed")
    else:
        print(f"Exercise 3: Failed - Peek item mismatch.")
        print(f"  Expected peek: {expected_peek_item}")
        print(f"  Got:           {next_player_in_line}")
    print("-" * 20)

    print("\nTests Finished.")

# Run tests
run_tests()

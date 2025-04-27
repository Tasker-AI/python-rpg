### Lesson: Linked Lists - Nodes and Linking ###

# Purpose: To understand the fundamental structure of a Linked List: the Node.
# Learn how to create individual nodes and manually link them together
# to form a chain representing a sequence.

# What is a Node?
# - A container holding a piece of data (`value`).
# - A pointer (`next`) that refers to the next Node in the sequence, or `None` if it's the last node.

# Why Linked Lists?
# - Dynamic size, efficient insertions/deletions *if* you know where.
# - Foundation for other data structures (like stacks, queues, hash maps).

# Python Implementation:
# We define a class to represent a Node.

class Node:
    """Represents a single node in a linked list."""
    def __init__(self, value):
        self.value = value  # The data stored in the node
        self.next = None    # Reference to the next node, initially None

### Exercise 1: Create Nodes ###
# Task: Create three separate Node objects representing items in an inventory chain.
# Node 1: value 'Sword'
# Node 2: value 'Shield'
# Node 3: value 'Potion'
# Store them in variables node1, node2, node3.
# Syntax: variable = Node(actual_value)

node1 = Node("Sword") # Create Node with value 'Sword'
node2 = Node("Shield") # Create Node with value 'Shield'
node3 = Node("Potion") # Create Node with value 'Potion'


### Exercise 2: Link the Nodes ###
# Task: Connect the nodes created above to form the sequence: Sword -> Shield -> Potion.
# The 'next' attribute of node1 should point to node2.
# The 'next' attribute of node2 should point to node3.
# The 'next' attribute of node3 should remain None (it's the end).
# Syntax: node_a.next = node_b

# Link node1 to node2
node1.next = node2
# Link node2 to node3
node2.next = node3



### Exercise 3: Basic Traversal (Manual) ###
# Task: Access the values by following the 'next' pointers, starting from node1.
# Store the value of the first node (node1) in `first_item_value`.
# Store the value of the node *after* node1 in `second_item_value`.
# Store the value of the node *after* node2 in `third_item_value`.
# Syntax: value = node.value
# Syntax: next_node = node.next

first_item_value = node1.value  # Get value from node1
second_item_value = node1.next.value # Get value from node1.next
third_item_value = node1.next.next.value  # Get value from node1.next.next


# Tests #
def run_tests():
    print("Running Linked List Node Tests...\n")
    global node1, node2, node3, first_item_value, second_item_value, third_item_value

    # Test Exercise 1 Results
    print("--- Testing Exercise 1: Create Nodes ---")
    ex1_passed = True
    if not isinstance(node1, Node) or getattr(node1, 'value', None) != 'Sword':
        print("Exercise 1: Failed - node1 check failed.")
        ex1_passed = False
    if not isinstance(node2, Node) or getattr(node2, 'value', None) != 'Shield':
        print("Exercise 1: Failed - node2 check failed.")
        ex1_passed = False
    if not isinstance(node3, Node) or getattr(node3, 'value', None) != 'Potion':
        print("Exercise 1: Failed - node3 check failed.")
        ex1_passed = False

    if ex1_passed:
        print("Exercise 1: Passed")
    print("-" * 20)


    # Test Exercise 2 Results (requires Ex1 nodes to exist)
    print("--- Testing Exercise 2: Link Nodes ---")
    ex2_passed = True
    if not ex1_passed:
        print("Exercise 2: Skipped (depends on Exercise 1 passing)")
        ex2_passed = False
    else:
        if getattr(node1, 'next', None) is not node2:
            print("Exercise 2: Failed - node1.next should point to node2.")
            ex2_passed = False
        if getattr(node2, 'next', None) is not node3:
            print("Exercise 2: Failed - node2.next should point to node3.")
            ex2_passed = False
        if getattr(node3, 'next', None) is not None:
            print("Exercise 2: Failed - node3.next should be None.")
            ex2_passed = False

    if ex1_passed and ex2_passed:
        print("Exercise 2: Passed")
    print("-" * 20)

    # Test Exercise 3 Results (requires Ex1 & Ex2)
    print("--- Testing Exercise 3: Traversal ---")
    ex3_passed = True
    if not ex1_passed or not ex2_passed:
         print("Exercise 3: Skipped (depends on Exercises 1 & 2 passing)")
         ex3_passed = False
    else:
        if first_item_value != 'Sword':
            print(f"Exercise 3: Failed - first_item_value mismatch (Expected: 'Sword', Got: {first_item_value})")
            ex3_passed = False
        if second_item_value != 'Shield':
            print(f"Exercise 3: Failed - second_item_value mismatch (Expected: 'Shield', Got: {second_item_value})")
            ex3_passed = False
        if third_item_value != 'Potion':
            print(f"Exercise 3: Failed - third_item_value mismatch (Expected: 'Potion', Got: {third_item_value})")
            ex3_passed = False

    if ex1_passed and ex2_passed and ex3_passed:
        print("Exercise 3: Passed")
    print("-" * 20)

    print("\nTests Finished.")

# Run tests (only if Node class is defined)
if 'Node' in globals():
    run_tests()
else:
    print("Error: Node class definition not found.")

### Lesson: Graph Representation (Adjacency List) ###

# Purpose: To learn how to represent a graph structure using an adjacency list in Python.
# An adjacency list uses a dictionary where keys are nodes and values are lists of their neighbors.
# When to use: Representing networks, maps, relationships, dependencies, etc., especially when connections are sparse.
# Example use case: Representing locations in a game world and the paths connecting them.

# Our simple game world map:
# Town Square <---> Market <---> Forest Entrance
# Town Square <---> Castle Gate
# Forest Entrance ---> Goblin Camp (One-way path!)


### Exercise 1: Initialize the Graph ###
# Task: Create an empty dictionary called `game_map` to represent our graph.
# Syntax: my_dict = {}

game_map = {} # Replace None with an empty dictionary


### Exercise 2: Add Nodes (Locations) ###
# Task: Add the locations (nodes) to the `game_map`. For now, each location will have an empty list of connections.
# Locations: 'Town Square', 'Market', 'Forest Entrance', 'Castle Gate', 'Goblin Camp'
# Syntax: my_graph[node] = []

# Add each location as a key with an empty list as its value in game_map below
game_map["Town Square"] = []
game_map["Market"] = []
game_map["Forest Entrance"] = []
game_map["Castle Gate"] = []
game_map["Goblin Camp"] = []


### Exercise 3: Add Edges (Paths) ###
# Task: Add the connections (edges) between locations based on the map description above.
# Remember: If A <---> B, you need to add B to A's list AND add A to B's list.
# For one-way paths (A ---> B), only add B to A's list.
# Syntax: my_graph[node1].append(node2)

# Add the connections to the game_map below
# Example: game_map['Town Square'].append('Market')
#          game_map['Market'].append('Town Square') # Because it's a two-way path
game_map["Town Square"].append("Market")
game_map["Town Square"].append("Castle Gate")
game_map["Forest Entrance"].append("Goblin Camp")
game_map["Forest Entrance"].append("Market")
game_map["Market"].append("Town Square")
game_map["Market"].append("Forest Entrance")
game_map["Castle Gate"].append("Town Square")


### Exercise 4: Get Neighbors ###
# Task: Get the list of locations directly connected to the 'Forest Entrance' and assign it to `forest_neighbors`.
# Syntax: neighbors = my_graph[node]

forest_neighbors = []
# Get the neighbors of 'Forest Entrance' from game_map and assign to forest_neighbors below
forest_neighbors = game_map["Forest Entrance"]

# --- Tests --- #
def run_tests():
    print("Running Graph Representation Tests...")
    passed_tests = 0
    total_tests = 4
    
    # Test Exercise 1
    try:
        if isinstance(game_map, dict) and not game_map:
             print("Exercise 1: Passed - Graph initialized as an empty dictionary.")
             passed_tests += 1
        else:
            print(f"Exercise 1: Failed - game_map should be an empty dictionary.")
            print(f"  Got: {type(game_map)}, Value: {game_map}")
    except Exception as e:
        print(f"Exercise 1: Failed with error - {e}")
        
    # Test Exercise 2 (Requires Ex 1 to pass)
    try:
        expected_nodes = {'Town Square', 'Market', 'Forest Entrance', 'Castle Gate', 'Goblin Camp'}
        current_nodes = set(game_map.keys())
        if current_nodes == expected_nodes:
            # Check if values are lists (initially empty)
            all_lists = all(isinstance(v, list) for v in game_map.values())
            if all_lists and all(not v for v in game_map.values()): # Check they are empty
                print("Exercise 2: Passed - All nodes added correctly with empty neighbor lists.")
                passed_tests += 1
            elif not all_lists:
                 print(f"Exercise 2: Failed - Not all values are lists.")
            else: # Lists are not empty
                 print(f"Exercise 2: Failed - Neighbor lists should be empty at this stage.")
        else:
            print(f"Exercise 2: Failed - Nodes mismatch.")
            print(f"  Expected Nodes: {expected_nodes}")
            print(f"  Found Nodes:    {current_nodes}")
            if expected_nodes - current_nodes:
                print(f"  Missing Nodes:  {expected_nodes - current_nodes}")
            if current_nodes - expected_nodes:
                 print(f"  Extra Nodes:    {current_nodes - expected_nodes}")
    except Exception as e:
        print(f"Exercise 2: Failed with error - {e}")

    # Test Exercise 3 (Requires Ex 2 to pass)
    try:
        # Check a few key connections based on the description
        ts_neighbors = set(game_map.get('Town Square', []))
        mkt_neighbors = set(game_map.get('Market', []))
        fe_neighbors = set(game_map.get('Forest Entrance', []))
        gc_in_fe = 'Goblin Camp' in fe_neighbors # One way
        fe_in_gc = 'Forest Entrance' in game_map.get('Goblin Camp', []) # Should NOT be true
        ts_in_mkt = 'Town Square' in mkt_neighbors
        mkt_in_ts = 'Market' in ts_neighbors
        
        correct = True
        if not ({'Market', 'Castle Gate'} == ts_neighbors):
            print("Exercise 3: Failed - Incorrect neighbors for Town Square.")
            print(f"  Expected: {{'Market', 'Castle Gate'}}, Got: {ts_neighbors}")
            correct = False
        if not ({'Town Square', 'Forest Entrance'} == mkt_neighbors):
            print("Exercise 3: Failed - Incorrect neighbors for Market.")
            print(f"  Expected: {{'Town Square', 'Forest Entrance'}}, Got: {mkt_neighbors}")
            correct = False
        if not ({'Market', 'Goblin Camp'} == fe_neighbors):
             print("Exercise 3: Failed - Incorrect neighbors for Forest Entrance.")
             print(f"  Expected: {{'Market', 'Goblin Camp'}}, Got: {fe_neighbors}")
             correct = False
        if fe_in_gc:
            print("Exercise 3: Failed - Goblin Camp should not link back to Forest Entrance (one-way path).")
            correct = False
            
        if correct:
            print("Exercise 3: Passed - Edges seem to be added correctly (based on checks).")
            passed_tests += 1
        
    except Exception as e:
        print(f"Exercise 3: Failed with error - {e}")
        
    # Test Exercise 4 (Requires Ex 3 to pass)
    try:
        expected_forest_neighbors = ['Market', 'Goblin Camp'] # Order might matter if user appends
        # Allow set comparison if list order is different but content is same
        if forest_neighbors == expected_forest_neighbors or set(forest_neighbors) == set(expected_forest_neighbors):
            print("Exercise 4: Passed - Correct neighbors for Forest Entrance retrieved.")
            passed_tests += 1
        else:
            print(f"Exercise 4: Failed - Incorrect neighbors retrieved for Forest Entrance.")
            print(f"  Expected (order might vary): {expected_forest_neighbors}")
            print(f"  Got: {forest_neighbors}")
    except Exception as e:
        print(f"Exercise 4: Failed with error - {e}")

    print(f"\nGraph Representation Tests Finished. Passed {passed_tests}/{total_tests}.")

# Run tests
run_tests()

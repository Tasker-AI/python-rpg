### Lesson Description: ###
# Purpose of the concept: Control flow determines the order in which code executes
# When to use it: Use control flow to make decisions, repeat actions, and handle different scenarios in your game

### Task 1 ###

## Syntax examples ##
# if/elif/else statements
# if condition1:
#     # code to run if condition1 is True
# elif condition2:
#     # code to run if condition1 is False and condition2 is True
# else:
#     # code to run if all conditions are False
#
# Comparison operators: ==, !=, <, >, <=, >=
# Logical operators: and, or, not

## To Do ##
# Complete the function that determines a character's attack power based on:
# - If the character is a mage (is_mage=True), use magic_skill as the base
# - If the character is not a mage, use strength as the base
# - If the character has a weapon (has_weapon=True), add a 10 point bonus
# - If the character's level is 10 or higher, double the final attack power

def calculate_attack_power(is_mage, level, strength, magic_skill, has_weapon):
    # Your code here
    attack_power = 0
    
    if is_mage == True:
        attack_power = magic_skill
    else:
        attack_power = strength
        
    if has_weapon == True:
        attack_power += 10
        
    if level >= 10:
        attack_power *= 2
        
    return attack_power


# Task 1 test #
def test_task1():
    test_cases = [
        # is_mage, level, strength, magic_skill, has_weapon, expected_result
        (True, 5, 10, 20, True, 30),      # Mage with weapon: 20 + 10 = 30
        (True, 5, 10, 20, False, 20),     # Mage without weapon: 20
        (False, 5, 15, 20, True, 25),     # Warrior with weapon: 15 + 10 = 25
        (False, 5, 15, 20, False, 15),    # Warrior without weapon: 15
        (True, 10, 10, 20, True, 60),     # Level 10 mage with weapon: (20 + 10) * 2 = 60
        (False, 12, 15, 20, False, 30),   # Level 12 warrior without weapon: 15 * 2 = 30
    ]
    
    for i, (is_mage, level, strength, magic_skill, has_weapon, expected) in enumerate(test_cases):
        result = calculate_attack_power(is_mage, level, strength, magic_skill, has_weapon)
        if result != expected:
            print(f"FAILED: Test case {i+1}")
            print(f"   Inputs: is_mage={is_mage}, level={level}, strength={strength}, magic_skill={magic_skill}, has_weapon={has_weapon}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")
            return False
    
    print("PASSED: All attack power calculations are correct!")
    return True

print("\nRunning Task 1 test...")
test_task1()

### Task 2 ###

## Syntax examples ##
# for loops
# for item in iterable:
#     # code to run for each item
#
# while loops
# while condition:
#     # code to run while condition is True
#     # make sure condition eventually becomes False to avoid infinite loops
#
# Loop control
# break - exits the loop completely
# continue - skips to the next iteration
# pass - does nothing (placeholder)

## To Do ##
# Complete the function that simulates a battle between a player and enemies:
# - The battle continues while both the player is alive (health > 0) and there are enemies left
# - For each round, the player defeats one enemy (reduce enemy_count by 1)
# - Each round, the player takes damage equal to the number of remaining enemies
# - If the player's health drops to 0 or below, they are defeated
# - Return a tuple with (victory, remaining_health, rounds)
#   - victory: True if all enemies are defeated, False if the player is defeated
#   - remaining_health: The player's health at the end of the battle
#   - rounds: The number of rounds the battle lasted

def simulate_battle(player_health, enemy_count):
    # Your code here
    rounds = 0
    while enemy_count > 0 and player_health > 0:
        rounds += 1
        player_health -= enemy_count
        enemy_count -= 1
        if player_health <= 0:
            result = (False, player_health, rounds)
            return result
    result = (True, player_health, rounds)
    return result


# Task 2 test #
def test_task2():
    test_cases = [
        # player_health, enemy_count, expected_result (victory, remaining_health, rounds)
        (10, 3, (True, 4, 3)),      # Player defeats 3 enemies, taking 3+2+1=6 damage
        (5, 3, (False, 0, 2)),      # Player defeats 2 enemies, taking 3+2=5 damage and is defeated
        (20, 5, (True, 5, 5)),      # Player defeats all 5 enemies, taking 5+4+3+2+1=15 damage
        (10, 0, (True, 10, 0)),     # No enemies, no battle
        (3, 3, (False, 0, 1)),      # Player is defeated after 1 round
    ]
    
    for i, (health, enemies, expected) in enumerate(test_cases):
        result = simulate_battle(health, enemies)
        if result != expected:
            print(f"FAILED: Test case {i+1}")
            print(f"   Inputs: player_health={health}, enemy_count={enemies}")
            print(f"   Expected: {expected}")
            print(f"   Actual: {result}")
            return False
    
    print("PASSED: All battle simulations are correct!")
    return True

print("\nRunning Task 2 test...")
test_task2()

### Task 3 ###

## Syntax examples ##
# List comprehensions
# new_list = [expression for item in iterable if condition]
#
# Dictionary comprehensions
# new_dict = {key_expr: value_expr for item in iterable if condition}
#
# Nested loops
# for outer_item in outer_iterable:
#     for inner_item in inner_iterable:
#         # code using both outer_item and inner_item

## To Do ##
# Complete the function that generates a game map with the following requirements:
# - The map is a list of lists (a grid) with the specified width and height
# - Each cell contains a dictionary with 'type' and 'items' keys
# - Cells on the edge of the map have type 'wall'
# - Cells not on the edge have type 'room'
# - Each 'room' cell has a 10% chance to contain a 'treasure' in its 'items' list
# - Each 'room' cell has a 20% chance to contain a 'monster' in its 'items' list
# - A cell can contain both a treasure and a monster
# - 'wall' cells always have empty 'items' lists

def generate_game_map(width, height):
    # Import random to generate random numbers
    import random
    
    # Create an empty map (list of lists)
    game_map = []
    
    # For each row (y-coordinate)
    for y in range(height):
        # Create a new row
        row = []
        
        # For each column (x-coordinate)
        for x in range(width):
            # Determine if this cell is on the edge
            is_edge = x == 0 or y == 0 or x == width-1 or y == height-1
            
            # Create cell dictionary
            if is_edge:
                # Wall cells have type 'wall' and empty items list
                cell = {'type': 'wall', 'items': []}
            else:
                # Room cells have type 'room' and might contain items
                cell = {'type': 'room', 'items': []}
                
                # 10% chance for treasure
                if random.random() < 0.1:  # random.random() returns a number between 0 and 1
                    cell['items'].append('treasure')
                    
                # 20% chance for monster
                if random.random() < 0.2:
                    cell['items'].append('monster')
            
            # Add the cell to the row
            row.append(cell)
        
        # Add the row to the map
        game_map.append(row)
            
    return game_map


# Task 3 test #
def test_task3():
    # Test with fixed dimensions for deterministic testing
    width, height = 5, 4
    game_map = generate_game_map(width, height)
    
    # Check dimensions
    if len(game_map) != height:
        print(f"FAILED: Map height should be {height}")
        print(f"   Actual: {len(game_map)}")
        return False
        
    for row in game_map:
        if len(row) != width:
            print(f"FAILED: Map width should be {width}")
            print(f"   Actual: {len(row)}")
            return False
    
    # Check cell structure and wall placement
    for y in range(height):
        for x in range(width):
            cell = game_map[y][x]
            
            # Check cell structure
            if not isinstance(cell, dict) or 'type' not in cell or 'items' not in cell:
                print(f"FAILED: Cell at ({x},{y}) has incorrect structure")
                print(f"   Cell: {cell}")
                return False
                
            # Check wall placement
            is_edge = x == 0 or y == 0 or x == width-1 or y == height-1
            expected_type = 'wall' if is_edge else 'room'
            if cell['type'] != expected_type:
                print(f"FAILED: Cell at ({x},{y}) should be type '{expected_type}'")
                print(f"   Actual: {cell['type']}")
                return False
                
            # Check items
            if cell['type'] == 'wall' and cell['items']:
                print(f"FAILED: Wall cell at ({x},{y}) should have empty items list")
                print(f"   Items: {cell['items']}")
                return False
                
            if not isinstance(cell['items'], list):
                print(f"FAILED: Cell items at ({x},{y}) should be a list")
                print(f"   Actual: {cell['items']}")
                return False
    
    # Count room cells with treasures and monsters to verify probabilities
    # (We can't test exact probabilities in a deterministic test, but we can check if items exist)
    room_count = 0
    treasure_count = 0
    monster_count = 0
    
    for row in game_map:
        for cell in row:
            if cell['type'] == 'room':
                room_count += 1
                if 'treasure' in cell['items']:
                    treasure_count += 1
                if 'monster' in cell['items']:
                    monster_count += 1
    
    print(f"PASSED: Game map generated correctly!")
    print(f"   Map dimensions: {width}x{height}")
    print(f"   Room cells: {room_count}")
    print(f"   Rooms with treasure: {treasure_count}")
    print(f"   Rooms with monsters: {monster_count}")
    return True

print("\nRunning Task 3 test...")
test_task3()

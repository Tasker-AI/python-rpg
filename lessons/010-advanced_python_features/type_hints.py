### Lesson - Type Hints in Python ###

# Purpose: Type hints allow you to specify expected data types for variables, parameters, and return values
# When to use: In larger projects, APIs, or when you want to catch type errors before runtime
# Example: Ensuring game functions receive the correct data types to prevent bugs

from typing import List, Dict, Tuple, Optional, Union, Callable
import random
import mypy


### Exercise 1 ###
# Add type hints to this function that:
# 1. Takes a player name (string) and level (integer)
# 2. Returns a formatted string
# 3. Use the -> notation for the return type

# Basic type hint syntax:
# def function_name(parameter: type) -> return_type:
#     function_body


def create_player_status(name: str, level: int) -> str:
    """Create a formatted status for a player"""
    return f"Player {name} is at level {level}"


### Exercise 2 ###
# Add type hints to this function that:
# 1. Takes a list of integers (player scores)
# 2. Returns a tuple containing (highest_score, average_score)
# 3. Use the typing module's List for the parameter type

# List/Dict/Tuple type hint syntax:
# from typing import List, Dict, Tuple
# def process_data(data: List[int]) -> Tuple[int, float]:
#     return max_value, average


def calculate_score_stats(scores: List[int]) -> Tuple[int, float]:
    """Calculate stats from a list of scores"""
    if not scores:
        return (0, 0.0)
    
    highest = max(scores)
    average = sum(scores) / len(scores)
    return (highest, average)


### Exercise 3 ###

# Create a function with type hints:
# 1. Takes a dictionary mapping item names (str) to their quantities (int)
# 2. Also takes an optional item name to check. Use Optional for parameters that might be None
# 3. Returns an int
def count_inventory(items: Dict[str, int], item_name: Optional[str]=None) -> int:
    """Count items in inventory"""
    # If no specific item requested, return total of all items
    if item_name is None:
        return sum(items.values())
    
    # Otherwise return the quantity of the specific item (or 0 if not found)
    else:
        return items.get(item_name, 0)


# Tests #
def runtests():
    # Test Exercise 1: Basic type hints
    print("Test 1: Basic type hints")
    status = create_player_status("Alex", 10)
    print(f"Player status: {status}")
    expected = "Player Alex is at level 10"
    print(f"Expected: {expected}")
    print(f"Test passed: {status == expected}")
    
    # Check annotations
    print(f"\nFunction annotations: {create_player_status.__annotations__}")
    has_param_hints = 'name' in create_player_status.__annotations__ and 'level' in create_player_status.__annotations__
    has_return_hint = 'return' in create_player_status.__annotations__
    if not has_param_hints or not has_return_hint:
        print("Missing type hints! Make sure to annotate parameters and return type")
    
    # Test Exercise 2: Container type hints
    print("\nTest 2: Container type hints")
    scores = [85, 92, 78, 95, 88]
    highest, average = calculate_score_stats(scores)
    print(f"Scores: {scores}")
    print(f"Highest: {highest}, Average: {average:.2f}")
    expected_highest = 95
    expected_average = 87.6
    print(f"Test passed: {highest == expected_highest and abs(average - expected_average) < 0.01}")
    
    # Check annotations
    print(f"\nFunction annotations: {calculate_score_stats.__annotations__}")
    has_param_hints = 'scores' in calculate_score_stats.__annotations__
    has_return_hint = 'return' in calculate_score_stats.__annotations__
    if not has_param_hints or not has_return_hint:
        print("Missing type hints! Make sure to annotate parameters and return type")
    
    # Test Exercise 3: Optional/Union type hints
    print("\nTest 3: Optional type hints")
    inventory = {"Health Potion": 5, "Mana Potion": 3, "Sword": 1, "Shield": 1}
    print(f"Inventory: {inventory}")
    
    # Test without specific item
    total = count_inventory(inventory)
    print(f"Total item count: {total}")
    expected_total = 10
    total_test = total == expected_total
    
    # Test with specific item
    potion_count = count_inventory(inventory, "Health Potion")
    print(f"Health Potion count: {potion_count}")
    expected_potion = 5
    potion_test = potion_count == expected_potion
    
    print(f"Test passed: {total_test and potion_test}")
    
    # Check annotations
    print(f"\nFunction annotations: {count_inventory.__annotations__}")
    has_param_hints = 'items' in count_inventory.__annotations__ and 'item_name' in count_inventory.__annotations__
    has_return_hint = 'return' in count_inventory.__annotations__
    if not has_param_hints or not has_return_hint:
        print("Missing type hints! Make sure to annotate parameters and return type")
    
    # Bonus: Creating a mypy error to see how it works
    # This would be caught by mypy but not by regular Python
    try:
        # This would pass runtime but fail mypy type checking
        print("\nBonus: What would mypy catch?")
        create_player_status(123, "ten")  # Types are reversed!
        print("Note: This would fail mypy static type checking")
    except:
        print("This code actually failed at runtime (unusual case)")

runtests()

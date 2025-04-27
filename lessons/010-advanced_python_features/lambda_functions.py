### Lesson - Lambda Functions in Python ###

# Purpose: Lambda functions allow you to create small, anonymous functions for simple operations
# When to use: When you need a small function for a short period (particularly with map, filter, sorted)
# Example: Sorting game items, filtering enemies, or mapping player stats

### Exercise 1 ###
# Create a lambda function that:
# 1. Takes a player name
# 2. Returns a greeting like "Welcome, PlayerName!"
# 3. Assign it to a variable called greet_player

# Standard function approach:
# def greet_player(name):
#     return f"Welcome, {name}!"

# Lambda function syntax:
# lambda parameter1, parameter2, ...: expression

greet_player = lambda name: f"Welcome, {name}!"


### Exercise 2 ###
# Use map() with a lambda function to:
# 1. Take a list of item values
# 2. Apply a 20% discount to each item
# 3. Return the list of discounted prices rounded to 2 decimal places

# Example with map and lambda:
# discounted_prices = list(map(lambda x: expression, prices))

def apply_discount(prices):
    return list(map(lambda price: round(price * 0.8, 2), prices))


### Exercise 3 ###
# Use filter() with a lambda function to:
# 1. Take a list of enemy tuples (name, health, level)
# 2. Filter out enemies with health less than 20 or level less than 5
# 3. Return a list of the names of remaining enemies

# Example with filter and lambda:
# filtered_items = list(filter(lambda item: condition, items))

def get_tough_enemies(enemies):
    # First filter for tough enemies (both conditions must be met)
    tough = filter(lambda enemy: enemy[1] >= 20 and enemy[2] >= 5, enemies)
    # Then extract just the names
    return [enemy[0] for enemy in tough]

    # Same as:
    # return [enemy[0] for enemy in filter(lambda enemy: enemy[1] >= 20 and enemy[2] >= 5, enemies)]



# Tests #
def runtests():
    # Test Exercise 1: Basic lambda
    player_name = "Alex"
    greeting = greet_player(player_name)
    
    print("Test 1: Basic lambda function")
    print(f"Expected greeting: Welcome, Alex!")
    print(f"Your greeting: {greeting}")
    lambda_test_passed = greeting == f"Welcome, {player_name}!"
    print(f"Test passed: {lambda_test_passed}")
    
    # Test Exercise 2: Map with lambda
    item_prices = [49.99, 99.50, 15.25, 75.00, 32.99]
    discounted = apply_discount(item_prices)
    expected_discounted = [40.0, 79.6, 12.2, 60.0, 26.39]
    
    print("\nTest 2: Map with lambda")
    print(f"Original prices: {item_prices}")
    print(f"Discounted prices: {discounted}")
    print(f"Expected discounted: {expected_discounted}")
    
    # Check if the values are close enough (handle floating point precision)
    map_test_passed = len(discounted) == len(expected_discounted)
    if map_test_passed:
        for i in range(len(discounted)):
            if abs(discounted[i] - expected_discounted[i]) > 0.01:
                map_test_passed = False
                break
    print(f"Test passed: {map_test_passed}")
    
    # Test Exercise 3: Filter with lambda
    enemies = [
        ("Goblin", 15, 3),
        ("Troll", 45, 8),
        ("Dragon", 150, 20),
        ("Skeleton", 22, 5),
        ("Zombie", 30, 4)
    ]
    tough_enemies = get_tough_enemies(enemies)
    expected_tough = ["Troll", "Dragon", "Skeleton"]
    
    print("\nTest 3: Filter with lambda")
    print(f"All enemies: {[e[0] for e in enemies]}")
    print(f"Tough enemies: {tough_enemies}")
    print(f"Expected tough enemies: {expected_tough}")
    filter_test_passed = sorted(tough_enemies) == sorted(expected_tough)
    print(f"Test passed: {filter_test_passed}")
    
    # Performance comparison
    import time
    
    # Create large dataset
    large_items = [i for i in range(100000)]
    
    # Standard function approach
    def double_item(x):
        return x * 2
    
    start = time.time()
    standard_result = list(map(double_item, large_items))
    standard_time = (time.time() - start) * 1000
    
    # Lambda approach
    start = time.time()
    lambda_result = list(map(lambda x: x * 2, large_items))
    lambda_time = (time.time() - start) * 1000
    
    print("\nPerformance comparison:")
    print(f"Standard function time: {standard_time:.2f} ms")
    print(f"Lambda function time: {lambda_time:.2f} ms")
    print(f"Results match: {standard_result == lambda_result}")

runtests()

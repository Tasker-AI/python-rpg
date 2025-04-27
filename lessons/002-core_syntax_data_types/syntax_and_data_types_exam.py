### Lesson syntax_and_data_types_exam ###

# Purpose of the concept
# Test your understanding of Python syntax and core data types with a gaming twist.

### Task 1: Create a Player Name ###
# To Do: Assign the string "KnightRider" to a variable called player_name.
# Syntax required:
# player_name = "your_name"
# Expected output format:
# player_name should be a string.

player_name = "KnightRider"

### Task 2: Set Player Level ###
# To Do: Assign the integer 5 to a variable called player_level.
# Syntax required:
# player_level = 0
# Expected output format:
# player_level should be an integer.

player_level = 5

### Task 3: Health as a Float ###
# To Do: Assign the value 99.5 to a variable called player_health.
# Syntax required:
# player_health = 0.0
# Expected output format:
# player_health should be a float.

player_health = 99.5

### Task 4: Inventory List ###
# To Do: Create a list called inventory with the items "sword", "shield", and "potion".
# Syntax required:
# inventory = ["item1", "item2"]
# Expected output format:
# inventory should be a list of strings.

inventory = ["sword", "shield", "potion"]

### Task 5: Player Stats Dictionary ###
# To Do: Create a dictionary called player_stats with keys "level", "health", and "mana" and values 5, 99.5, and 30.
# Syntax required:
# player_stats = {"key": value}
# Expected output format:
# player_stats should be a dictionary with correct keys and values.

player_stats = {"level" : 5, "health": 99.5, "mana" : 30}

# Tests #
def runtests():
    print("--- Task 1 ---")
    try:
        assert isinstance(player_name, str), f"Expected string, got {type(player_name)}"
        assert player_name == "KnightRider", f"Expected 'KnightRider', got {player_name}"
        print("Task 1 Passed")
    except Exception as e:
        print("Task 1 Failed:", e)
    print("\n--- Task 2 ---")
    try:
        assert isinstance(player_level, int), f"Expected int, got {type(player_level)}"
        assert player_level == 5, f"Expected 5, got {player_level}"
        print("Task 2 Passed")
    except Exception as e:
        print("Task 2 Failed:", e)
    print("\n--- Task 3 ---")
    try:
        assert isinstance(player_health, float), f"Expected float, got {type(player_health)}"
        assert player_health == 99.5, f"Expected 99.5, got {player_health}"
        print("Task 3 Passed")
    except Exception as e:
        print("Task 3 Failed:", e)
    print("\n--- Task 4 ---")
    try:
        assert isinstance(inventory, list), f"Expected list, got {type(inventory)}"
        assert inventory == ["sword", "shield", "potion"], f"Expected ['sword', 'shield', 'potion'], got {inventory}"
        print("Task 4 Passed")
    except Exception as e:
        print("Task 4 Failed:", e)
    print("\n--- Task 5 ---")
    try:
        assert isinstance(player_stats, dict), f"Expected dict, got {type(player_stats)}"
        assert player_stats == {"level": 5, "health": 99.5, "mana": 30}, f"Expected {{'level': 5, 'health': 99.5, 'mana': 30}}, got {player_stats}"
        print("Task 5 Passed")
    except Exception as e:
        print("Task 5 Failed:", e)

runtests() # Tests should be uncommented by default

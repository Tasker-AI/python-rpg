### Lesson control_structures_exam ###

# Purpose of the concept
# Test your understanding of Python control structures (for loops, while loops, if-elif-else) in a gaming context.

### Task 1: For Loop - Counting Coins ###
# To Do: Use a for loop to sum all the coins in the list and assign the total to total_coins.
# Syntax required:
# for item in list:
#     ...
# Expected output format:
# total_coins should be the sum of the numbers in coins_list.

coins_list = [1, 5, 10, 25, 100]
total_coins = 0
for number in coins_list:
    total_coins += number


### Task 2: While Loop - Level Up ###
# To Do: Use a while loop to increase player_level by 1 until it reaches 10. Start with player_level = 5.
# Syntax required:
# while condition:
#     ...
# Expected output format:
# player_level should be 10 after the loop.

player_level = 5
while player_level <10:
    player_level +=1

### Task 3: If-Elif-Else - Health Status ###
# To Do: Set health_status to 'Critical' if health < 20, 'Injured' if health < 70, else 'Healthy'.
# Syntax required:
# if ...:
# elif ...:
# else:
# Expected output format:
# health_status should be a string based on health value.

health = 45
if health <20:
    health_status = "Critical"
elif health <70:
    health_status = "Injured"
else:
    health_status = "Healthy"

# Tests #
def runtests():
    print("--- Task 1 ---")
    try:
        assert total_coins == sum(coins_list), f"Expected {sum(coins_list)}, got {total_coins}"
        print("Task 1 Passed")
    except Exception as e:
        print("Task 1 Failed:", e)
    print("\n--- Task 2 ---")
    try:
        assert player_level == 10, f"Expected 10, got {player_level}"
        print("Task 2 Passed")
    except Exception as e:
        print("Task 2 Failed:", e)
    print("\n--- Task 3 ---")
    try:
        expected = 'Critical' if health < 20 else 'Injured' if health < 70 else 'Healthy'
        assert health_status == expected, f"Expected {expected}, got {health_status}"
        print("Task 3 Passed")
    except Exception as e:
        print("Task 3 Failed:", e)

runtests() # Tests should be uncommented by default

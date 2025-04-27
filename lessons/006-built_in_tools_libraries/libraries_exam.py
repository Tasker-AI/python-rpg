### Libraries Exam ###

# Instructions: Complete the following functions using concepts learned
# from the math, random, collections, and itertools libraries.
# No syntax hints are provided for the exam. Good luck!

import math
import random
from collections import Counter, defaultdict
from itertools import product, chain # Allow imports

### Exercise 1: Critical Hit Damage ###
# Task: Implement a function `calculate_damage(base_damage, crit_chance_percent, crit_multiplier)`
# - Generate a random integer roll between 1 and 100 (inclusive).
# - If the roll is strictly greater than (100 - crit_chance_percent), calculate critical damage:
#   Use math.pow() to raise the base_damage to the power of crit_multiplier, then take the floor using math.floor().
# - Otherwise, calculate normal damage: Generate a random float factor between 0.8 and 1.2 (inclusive)
#   using random.uniform(), multiply it by base_damage, and take the floor using math.floor().
# - Return the calculated damage (which should be an integer).

def calculate_damage(base_damage, crit_chance_percent, crit_multiplier):
    random_number = random.randint(1, 100)
    if random_number > 100 - crit_chance_percent:
        return math.floor(math.pow(base_damage, crit_multiplier))
    else:
        return math.floor(random.uniform(0.8, 1.2) * base_damage)
    

### Exercise 2: Loot Organization ###
# Task: Implement a function `organize_loot(loot_list)`
# - The input `loot_list` is a list of dictionaries, e.g.,
#   [{'name': 'Gold Coin', 'type': 'currency', 'rarity': 'common'}, {'name': 'Health Potion', 'type': 'potion', 'rarity': 'common'}, ...]
# - First, use collections.Counter to count how many items of each 'type' there are. Store this in 'type_counts'.
# - Second, use collections.defaultdict(list) to group the item 'name's by their 'rarity'. Store this in 'items_by_rarity'.
# - Return a tuple containing two elements: (type_counts, items_by_rarity)

def organize_loot(loot_list):
    # get a list of all item types so that count can count the orrucances
    types_only = [item["type"] for item in loot_list]
    print(types_only)
    type_counts = Counter(types_only)
    
    items_by_rarity = defaultdict(list)
    # loop through the original list of dictionaries. Each item is a dict
    for item in loot_list:
        # access the list for the item's rarity (items_by_rarity[item['rarity']]) 
        # and append the item's name (item['name']) to it.
        items_by_rarity[item["rarity"]].append(item["name"])
        
    # return the counts and the defaultdict object
    return (type_counts, items_by_rarity)

### Exercise 3: Team Matchups ###
# Task: Implement a function `generate_matchups(all_players, team_size)`

def generate_matchups(all_players, team_size):
    # `all_players` is a list of player names.
    # `team_size` is the number of players per team.
    # Randomly divide `all_players` into two teams of `team_size`. Make sure the same player isn't on both teams.
    # Use random.sample() to select players for the first team. The remaining players form the second team.
    # (Assume len(all_players) is exactly 2 * team_size).
    first_team = random.sample(all_players, team_size)
    second_team = []
    for player in all_players:
        if player not in first_team:
            second_team.append(player)
    
    # Use itertools.product() to generate all possible (player_team1, player_team2) matchup pairs between the two teams.
    team_combos = product(first_team, second_team)
    
    # Return the list of matchup pairs (a list of tuples).
    return list(team_combos)

# Tests #
def run_tests():
    print("Running Exam Tests...\n")
    passed_count = 0
    total_tests = 3

    # Test Exercise 1
    print("--- Testing Exercise 1: calculate_damage ---")
    # We run multiple trials because of randomness
    results_ex1 = {'crit': 0, 'normal': 0}
    expected_crit_dmg = math.floor(math.pow(10, 1.5)) # ~31
    base_damage = 10
    crit_chance = 50 # 50%
    crit_multiplier = 1.5
    trials = 200
    random.seed(50) # Set seed for reproducibility during test run

    try:
        for _ in range(trials):
            dmg = calculate_damage(base_damage, crit_chance, crit_multiplier)
            if dmg == expected_crit_dmg:
                results_ex1['crit'] += 1
            elif 8 <= dmg <= 12: # Normal damage range floor(10*0.8) to floor(10*1.2)
                 results_ex1['normal'] += 1
            else:
                 # Fail immediately if damage is outside expected ranges
                 print(f"Exercise 1: Failed - Unexpected damage value: {dmg}")
                 print(f"  Expected crit: {expected_crit_dmg}, Expected normal range: 8-12")
                 results_ex1['fail'] = 1 # Mark failure
                 break

        if 'fail' not in results_ex1:
            # Check if distribution is roughly correct (allow some margin for randomness)
            crit_ratio = results_ex1['crit'] / trials
            # Expect roughly 50% crits
            if 0.4 < crit_ratio < 0.6:
                 print("Exercise 1: Passed (Checks on damage values and approximate crit ratio look good)")
                 passed_count +=1
            else:
                 print(f"Exercise 1: Failed - Crit ratio ({crit_ratio:.2f}) is too far from expected {crit_chance/100:.2f}")
                 print(f"  Counts: {results_ex1}")

    except Exception as e:
        print(f"Exercise 1: Failed - An error occurred: {e}")
    print("-" * 20)


    # Test Exercise 2
    print("--- Testing Exercise 2: organize_loot ---")
    sample_loot = [
        {'name': 'Gold Coin', 'type': 'currency', 'rarity': 'common'},
        {'name': 'Health Potion', 'type': 'potion', 'rarity': 'common'},
        {'name': 'Iron Sword', 'type': 'weapon', 'rarity': 'common'},
        {'name': 'Mana Potion', 'type': 'potion', 'rarity': 'common'},
        {'name': 'Gem', 'type': 'currency', 'rarity': 'rare'},
        {'name': 'Dragon Scale', 'type': 'material', 'rarity': 'epic'},
        {'name': 'Elixir', 'type': 'potion', 'rarity': 'rare'},
        {'name': 'Vorpal Sword', 'type': 'weapon', 'rarity': 'epic'},
    ]
    expected_type_counts = Counter({'currency': 2, 'potion': 3, 'weapon': 2, 'material': 1})
    # Convert expected defaultdict to dict and sort lists for comparison
    expected_items_by_rarity_dict = {
        'common': sorted(['Gold Coin', 'Health Potion', 'Iron Sword', 'Mana Potion']),
        'rare': sorted(['Gem', 'Elixir']),
        'epic': sorted(['Dragon Scale', 'Vorpal Sword'])
    }

    try:
        type_counts, items_by_rarity = organize_loot(sample_loot)
        passed_ex2 = True

        if not isinstance(type_counts, Counter) or type_counts != expected_type_counts:
            print("Exercise 2: Failed - Type counts mismatch.")
            print(f"  Expected: {expected_type_counts}")
            print(f"  Got:      {type_counts}")
            passed_ex2 = False

        # Convert actual defaultdict to dict and sort lists for comparison
        actual_items_by_rarity_dict = {k: sorted(v) for k, v in items_by_rarity.items()}

        if not isinstance(items_by_rarity, defaultdict) or actual_items_by_rarity_dict != expected_items_by_rarity_dict:
            print("Exercise 2: Failed - Items by rarity mismatch.")
            print(f"  Expected: {expected_items_by_rarity_dict}")
            print(f"  Got:      {actual_items_by_rarity_dict}")
            passed_ex2 = False

        if passed_ex2:
            print("Exercise 2: Passed")
            passed_count += 1

    except Exception as e:
         print(f"Exercise 2: Failed - An error occurred: {e}")
    print("-" * 20)

    # Test Exercise 3
    print("--- Testing Exercise 3: generate_matchups ---")
    players = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    team_size = 3
    random.seed(123) # Control randomness for sampling

    try:
        matchups = generate_matchups(players, team_size)

        # Determine expected teams based on seed
        random.seed(123) # Reset seed to replicate sample
        team1_expected = sorted(random.sample(players, team_size))
        team2_expected = sorted(list(set(players) - set(team1_expected)))
        expected_matchups = sorted(list(product(team1_expected, team2_expected)))

        # Sort the generated matchups for comparison
        passed_ex3 = True
        if not isinstance(matchups, list) or len(matchups) != team_size * team_size:
             print(f"Exercise 3: Failed - Output is not a list or has incorrect length ({len(matchups)} instead of {team_size*team_size}).")
             passed_ex3 = False
        elif sorted(matchups) != expected_matchups:
            print("Exercise 3: Failed - Matchup list mismatch.")
            # Find which team was likely generated to help debug
            generated_players_flat = set(p for pair in matchups for p in pair)
            if generated_players_flat != set(players):
                 print("  Hint: The players involved in the generated matchups don't match the original player list.")
            else:
                 # Try to guess the teams formed
                 possible_team1 = sorted(list(set(p[0] for p in matchups)))
                 possible_team2 = sorted(list(set(p[1] for p in matchups)))
                 print(f"  Hint: Expected Teams (sorted): {team1_expected} vs {team2_expected}")
                 print(f"  Hint: Teams inferred from your output (sorted): {possible_team1} vs {possible_team2}")

            print(f"  Expected matchups based on seed (teams sorted): {expected_matchups}")
            print(f"  Got (sorted): {sorted(matchups)}")
            passed_ex3 = False

        if passed_ex3:
            print("Exercise 3: Passed")
            passed_count += 1
    except Exception as e:
         print(f"Exercise 3: Failed - An error occurred: {e}")

    print("-" * 20)

    print(f"\nExam Finished. Passed {passed_count}/{total_tests} tests.")

run_tests()

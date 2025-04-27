### Lesson Zip Function ###

# Purpose of the concept:
# The zip() function takes iterables (like lists), aggregates them element-wise,
# and returns an iterator of tuples where the i-th tuple contains the i-th element from each iterable.

# When to use it:
# - When you need to combine multiple lists or iterables element by element
# - When you want to iterate through multiple sequences in parallel
# - When creating dictionaries from separate lists of keys and values


### Exercise ### 
# Create a function called combine_player_stats that takes two lists:
# 1. A list of stat names (like "Health", "Attack", "Defense")
# 2. A list of stat values (like 100, 45, 30)
# The function should return a dictionary where the stat names are keys and the stat values are values

# dict(zip(keys, values))
# OR
# {key: value for key, value in zip(keys, values)}

def combine_player_stats(stat_names, stat_values):
    return dict(zip(stat_names, stat_values))


### Exercise ### 
# Use zip() to combine these two lists into a list of tuples
# Each tuple should contain a monster name and its corresponding level
# Store the result in a variable called monster_data

monster_names = ["Goblin", "Dragon", "Troll", "Skeleton", "Witch"]
monster_levels = [5, 50, 30, 15, 25]
monster_data = list(zip(monster_names, monster_levels))


### Exercise ### 
# Use zip() to iterate through three lists at once:
# 1. A list of weapon names
# 2. A list of weapon damages
# 3. A list of weapon rarities
# Create a function called display_weapons that takes these three lists and returns
# a list of formatted strings like: "Weapon: Sword, Damage: 15, Rarity: Common"

# for item1, item2, item3 in zip(list1, list2, list3):
#     formatted_string = f"Format with {item1}, {item2}, and {item3}"

def display_weapons(weapon_names, weapon_damages, weapon_rarities):
    formatted_list = []
    
    for item1, item2, item3 in zip(weapon_names, weapon_damages, weapon_rarities):
        formatted_string = f"Weapon: {item1}, Damage: {item2}, Rarity: {item3}"
        formatted_list.append(formatted_string)
    


    return formatted_list


# Tests #
def runtests():
    print("Testing your zip() function implementations...")
    
    # Test combine_player_stats function
    stat_names = ["Health", "Attack", "Defense", "Speed"]
    stat_values = [150, 65, 40, 90]
    expected = {"Health": 150, "Attack": 65, "Defense": 40, "Speed": 90}
    result = combine_player_stats(stat_names, stat_values)
    print(f"Player stats: {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}\n")
    
    # Test monster_data
    expected = [
        ("Goblin", 5),
        ("Dragon", 50),
        ("Troll", 30),
        ("Skeleton", 15),
        ("Witch", 25)
    ]
    print(f"Monster data: {list(monster_data)}")
    print(f"Expected: {expected}")
    print(f"Test passed: {list(monster_data) == expected}\n")
    
    # Test display_weapons function
    weapon_names = ["Sword", "Bow", "Axe", "Staff"]
    weapon_damages = [15, 12, 20, 8]
    weapon_rarities = ["Common", "Uncommon", "Rare", "Epic"]
    expected = [
        "Weapon: Sword, Damage: 15, Rarity: Common",
        "Weapon: Bow, Damage: 12, Rarity: Uncommon",
        "Weapon: Axe, Damage: 20, Rarity: Rare",
        "Weapon: Staff, Damage: 8, Rarity: Epic"
    ]
    result = display_weapons(weapon_names, weapon_damages, weapon_rarities)
    print(f"Weapon display: {result}")
    print(f"Expected: {expected}")
    print(f"Test passed: {result == expected}")

runtests()

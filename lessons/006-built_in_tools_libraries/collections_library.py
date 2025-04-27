### Lesson: collections Library (Counter, defaultdict) ###

# Purpose: The `collections` library provides specialized container datatypes.
# - `Counter`: A dict subclass for counting hashable objects.
# - `defaultdict`: A dict subclass that calls a factory function to supply missing values.

# When to use it:
# - `Counter`: Tallying items (inventory counts), frequency analysis (most common monster?).
# - `defaultdict`: Grouping items into categories (items by type), accumulating values
#   without pre-initializing keys (tracking scores per player/team).

# Example Use Case:
# - `Counter`: Player picks up loot ['sword', 'potion', 'potion', 'gold', 'sword'].
#   A Counter would easily show {'sword': 2, 'potion': 2, 'gold': 1}.
# - `defaultdict`: Grouping inventory items by type: {'weapon': ['sword'], 'consumable': ['potion'], 'misc': ['gold']}.
#   If you add a new type, `defaultdict` automatically creates the list for it.

# Note: You need to import the specific classes from the collections library.
# from collections import Counter, defaultdict

from collections import Counter, defaultdict # Import for exercises

### Exercise 1: Counting Loot Items ###
# Task: You have a list representing loot collected by a player.
# Use `collections.Counter` to count the occurrences of each item type.
# Syntax: item_counts = Counter(list_of_items)
# Access counts like a dictionary: item_counts['item_name']

loot_collected = ['shield', 'potion', 'sword', 'potion', 'gold', 'potion', 'shield', 'gem']
inventory_counts = Counter(loot_collected)


### Exercise 2: Accessing Counts ###
# Task: Using the `inventory_counts` Counter from Exercise 1, get the count
# of 'potion' items. Also, try accessing the count of an item that wasn't
# in the original list, like 'helmet'. Observe how Counter handles missing keys.
# Syntax: count = counter_object['key']

potion_count = inventory_counts["potion"]
helmet_count = inventory_counts['helmet']


### Exercise 3: Grouping Items by Type ###
# Task: You have a list of item dictionaries, each with a 'name' and 'type'.
# Use `collections.defaultdict` with a `list` factory to group item *names* by their *type*.
# The resulting dictionary should look like: {'weapon': ['sword', ...], 'armor': [...], ...}
# Syntax: grouped_items = defaultdict(list)
# Then iterate through items and append: grouped_items[item['type']].append(item['name'])

item_list = [
    {'name': 'Iron Sword', 'type': 'weapon'},
    {'name': 'Health Potion', 'type': 'consumable'},
    {'name': 'Leather Vest', 'type': 'armor'},
    {'name': 'Steel Sword', 'type': 'weapon'},
    {'name': 'Mana Potion', 'type': 'consumable'},
    {'name': 'Chainmail', 'type': 'armor'},
]

items_by_type = defaultdict(list) 
# Then, loop through item_list and append names to the correct type list in items_by_type
print(items_by_type)
for item in item_list:
    items_by_type[item["type"]].append(item["name"])
    
print(items_by_type)


# Tests #
def run_tests():
    print("Running Tests...\n")
    global inventory_counts, potion_count, helmet_count, items_by_type # Allow tests to access

    # Test Exercise 1 & 2
    print("--- Testing Exercises 1 & 2: Counter ---")
    expected_counts = {'shield': 2, 'potion': 3, 'sword': 1, 'gold': 1, 'gem': 1}
    passed_counter = True
    if not isinstance(inventory_counts, Counter):
         print(f"Exercise 1: Failed - inventory_counts is not a Counter object (type: {type(inventory_counts)}) ")
         passed_counter = False
    elif inventory_counts != expected_counts:
        print(f"Exercise 1: Failed - Counts mismatch. Expected {expected_counts}, got {inventory_counts}")
        passed_counter = False

    expected_potion_count = 3
    expected_helmet_count = 0 # Counter returns 0 for missing keys
    if potion_count != expected_potion_count:
        print(f"Exercise 2: Failed - Potion count mismatch. Expected {expected_potion_count}, got {potion_count}")
        passed_counter = False
    if helmet_count != expected_helmet_count:
        print(f"Exercise 2: Failed - Helmet count mismatch (should be 0 for missing keys). Expected {expected_helmet_count}, got {helmet_count}")
        passed_counter = False

    if passed_counter:
        print("Exercises 1 & 2: Passed")
    print("-" * 20)

    # Test Exercise 3
    print("--- Testing Exercise 3: defaultdict ---")
    # Loop through items_list and populate items_by_type *if user hasn't*
    # This allows testing even if the user only created the defaultdict
    if items_by_type is None:
        items_by_type = defaultdict(list) # Create instance if user didn't

    # Check if user added the loop logic
    if not items_by_type: # If it's still empty after potential creation
        temp_dict = defaultdict(list)
        try:
             for item in item_list:
                 temp_dict[item['type']].append(item['name'])
             if not temp_dict: # If loop didn't add anything
                  print("Exercise 3: Hint - Remember to loop through item_list and append to items_by_type.")
        except Exception:
             print("Exercise 3: Hint - Remember to loop through item_list and append to items_by_type.")


    # Manually populate the user's dict if they didn't add the loop
    # This allows checking the defaultdict creation independently.
    if not items_by_type and isinstance(items_by_type, defaultdict):
         print("Exercise 3: Info - Populating defaultdict for testing (user loop missing).")
         for item in item_list:
             items_by_type[item['type']].append(item['name'])

    expected_grouping = {
        'weapon': ['Iron Sword', 'Steel Sword'],
        'consumable': ['Health Potion', 'Mana Potion'],
        'armor': ['Leather Vest', 'Chainmail']
    }
    passed_defaultdict = True
    if not isinstance(items_by_type, defaultdict):
        print(f"Exercise 3: Failed - items_by_type is not a defaultdict object (type: {type(items_by_type)}) ")
        passed_defaultdict = False
    # Convert to regular dict for comparison, as order within lists doesn't matter for this test
    elif {k: sorted(v) for k, v in items_by_type.items()} != {k: sorted(v) for k, v in expected_grouping.items()}:
        print(f"Exercise 3: Failed - Grouping mismatch.")
        print(f"  Expected: {expected_grouping}")
        # Show sorted lists in output for easier comparison
        print(f"  Got:      { {k: sorted(v) for k, v in items_by_type.items()} }")
        passed_defaultdict = False

    if passed_defaultdict:
        print("Exercise 3: Passed")
    print("-" * 20)

    print("\nTests Finished.")

# Run tests after user code block
run_tests()

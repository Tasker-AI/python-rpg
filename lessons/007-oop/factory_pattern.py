### Lesson - Factory Pattern in Python ###

# Purpose: Factory patterns create objects without specifying their exact class
# When to use: When you need to create different but related objects based on conditions
# Example: Creating different types of enemies, items, or weapons in a game

# Import the character classes we've created
from classes_basics import GameCharacter
from inheritance import Warrior, Mage

# A Factory class creates objects based on parameters
# Example factory:
# class Factory:
#     @staticmethod
#     def create_product(product_type):
#         if product_type == "type_a":
#             return ProductA()
#         elif product_type == "type_b":
#             return ProductB()


### Exercise 1 ###
# Create a CharacterFactory class with a static create_character method that:
# 1. Takes character_type, name, and other relevant parameters
# 2. Returns a Warrior if character_type is "warrior"
# 3. Returns a Mage if character_type is "mage"
# 4. Returns a basic GameCharacter if character_type is "npc"

class CharacterFactory:
    @staticmethod
    def create_character(character_type, name, health = 100, armor = 10, mana = 10):
        if character_type == "warrior":
            return Warrior(name, health, armor)
        elif character_type == "mage":
            return Mage(name, health, mana)
        elif character_type == "npc":
            return GameCharacter(name, health)


### Exercise 2 ###
# Create a game function called create_party that:
# 1. Creates a list with one warrior, one mage, and one npc
# 2. Uses the CharacterFactory to create each character
# 3. Returns the list of characters

# For example:
# def create_party(warrior_name, mage_name, npc_name):
#     # Your code here
#     return party_members

def create_party(warrior_name, mage_name, npc_name):
    party_list = []
    party_list.append(CharacterFactory.create_character("warrior", warrior_name))
    party_list.append(CharacterFactory.create_character("mage", mage_name))
    party_list.append(CharacterFactory.create_character("npc", npc_name))
    
    return party_list


### Exercise 3 ###
# Create a function called team_attack that:
# 1. Takes a list of characters and an opponent
# 2. Makes each character attack the opponent (mages use fireball, others use take_damage)
# 3. Returns the total damage dealt

# For example:
# def team_attack(team, opponent):
#     # Your code here
#     return total_damage_dealt

def team_attack(team, opponent):
    total_damage_dealt = 0
    
    for character in team:
        if isinstance(character, Mage):
            total_damage_dealt += opponent.take_damage(character.fireball(opponent))            
        else:
            total_damage_dealt += opponent.take_damage(10)            

    return total_damage_dealt


# Tests #
def runtests():
    print("Test 1: Creating different character types")
    warrior = CharacterFactory.create_character("warrior", "Aragorn", 150, 15)
    mage = CharacterFactory.create_character("mage", "Gandalf", 100, 120)
    npc = CharacterFactory.create_character("npc", "Villager", 50)
    
    print(f"Expected warrior class: Warrior, Got: {warrior.__class__.__name__}")
    print(f"Expected mage class: Mage, Got: {mage.__class__.__name__}")
    print(f"Expected npc class: GameCharacter, Got: {npc.__class__.__name__}")
    
    is_correct_class = (warrior.__class__.__name__ == "Warrior" and 
                        mage.__class__.__name__ == "Mage" and 
                        npc.__class__.__name__ == "GameCharacter")
    print(f"Test passed: {is_correct_class}")
    
    print("\nTest 2: Creating a party")
    party = create_party("Hero", "Wizard", "Guide")
    
    print(f"Expected party size: 3, Got: {len(party)}")
    print(f"Expected classes: Warrior, Mage, GameCharacter")
    print(f"Got: {[character.__class__.__name__ for character in party]}")
    
    is_correct_party = (len(party) == 3 and 
                       any(char.__class__.__name__ == "Warrior" for char in party) and
                       any(char.__class__.__name__ == "Mage" for char in party) and
                       any(char.__class__.__name__ == "GameCharacter" for char in party))
    print(f"Test passed: {is_correct_party}")
    
    print("\nTest 3: Team attack")
    opponent = GameCharacter("Boss", 200)
    damage = team_attack(party, opponent)
    
    print(f"Expected boss health < 200, Got: {opponent.health}")
    print(f"Expected total damage > 0, Got: {damage}")
    print(f"Test passed: {opponent.health < 200 and damage > 0}")

runtests()

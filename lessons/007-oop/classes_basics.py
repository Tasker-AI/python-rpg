### Lesson - Classes in Python ###

# Purpose: Classes allow you to create custom data types with methods and attributes
# When to use: When you need to represent real-world objects with properties and behaviors
# Example: Game characters, items, or systems that have state and behavior

# In Python, classes are defined using the 'class' keyword
# Example class definition:
# class ClassName:
#     def __init__(self, param1, param2):  # Constructor method
#         self.attribute1 = param1  # Instance attribute
#         self.attribute2 = param2
#
#     def method_name(self, param):  # Instance method
#         return self.attribute1 + param

### Exercise 1 ###
# Create a GameCharacter class that:
# 1. Takes name and health as initialization parameters
# 2. Sets these as attributes
# 3. Add a method called is_alive() that returns True if health > 0, False otherwise

class GameCharacter:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        
    def is_alive(self):
        
        return self.health > 0

    ### Exercise 2 ###
    # Add a take_damage method to GameCharacter that:
    # 1. Takes a damage_amount parameter
    # 2. Subtracts the damage from the character's health
    # 3. Ensures health never goes below 0
    # 4. Returns the remaining health

    # For example:
    # def take_damage(self, damage_amount):
    #     # Your code here
    #     return self.health

    def take_damage(self, damage_amount):
        if self.health - damage_amount < 0:
            self.health = 0
            return self.health
        else:
            self.health -= damage_amount
            return self.health
        

    ### Exercise 3 ###
    # Add a heal method to GameCharacter that:
    # 1. Takes a heal_amount parameter
    # 2. Adds the amount to the character's health
    # 3. Returns the new health value
    # 4. Doesn't do anything if the character is not alive (health is 0)

    # For example:
    # def heal(self, heal_amount):
    #     # Your code here
    #     return self.health

    def heal(self, heal_amount):
        if self.health > 0:
            self.health += heal_amount
            return self.health

# Tests #
def runtests():
    print("Test 1: Creating a character")
    hero = GameCharacter("Hero", 100)
    print(f"Expected name: Hero, Got: {hero.name}")
    print(f"Expected health: 100, Got: {hero.health}")
    print(f"Test passed: {hero.name == 'Hero' and hero.health == 100}")
    
    print("\nTest 2: Checking if character is alive")
    print(f"Expected alive status: True, Got: {hero.is_alive()}")
    print(f"Test passed: {hero.is_alive() == True}")
    
    print("\nTest 3: Taking damage")
    hero.take_damage(30)
    print(f"Expected health after damage: 70, Got: {hero.health}")
    print(f"Test passed: {hero.health == 70}")
    
    print("\nTest 4: Taking fatal damage")
    hero.take_damage(100)
    print(f"Expected health after fatal damage: 0, Got: {hero.health}")
    print(f"Expected alive status: False, Got: {hero.is_alive()}")
    print(f"Test passed: {hero.health == 0 and hero.is_alive() == False}")
    
    print("\nTest 5: Healing when dead")
    old_health = hero.health
    hero.heal(50)
    print(f"Expected health after healing when dead: {old_health}, Got: {hero.health}")
    print(f"Test passed: {hero.health == old_health}")
    
    print("\nTest 6: Healing when alive")
    hero2 = GameCharacter("Hero2", 50)
    hero2.heal(25)
    print(f"Expected health after healing: 75, Got: {hero2.health}")
    print(f"Test passed: {hero2.health == 75}")

runtests()

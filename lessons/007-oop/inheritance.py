### Lesson - Inheritance in Python ###

# Purpose: Inheritance allows a class to inherit attributes and methods from another class
# When to use: When you need specialized versions of a base class with shared functionality
# Example: Different types of game characters (Warrior, Mage) with common base attributes

# In Python, you can create a child class that inherits from a parent class:
# class ParentClass:
#     def parent_method(self):
#         return "This is from the parent"
#
# class ChildClass(ParentClass):  # Inheritance happens in the parentheses
#     def child_method(self):
#         return "This is from the child"
#
#     def parent_method(self):  # Overriding the parent method
#         return "This is the child's version"

# Copy your GameCharacter class from the previous lesson
class GameCharacter:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        
    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage_amount):
        if self.health - damage_amount < 0:
            self.health = 0
        else:
            self.health -= damage_amount
        return self.health

    def heal(self, heal_amount):
        if self.health > 0:
            self.health += heal_amount
        return self.health


### Exercise 1 ###
# Create a Warrior class that inherits from GameCharacter with:
# 1. An __init__ method that takes name, health, and armor
# 2. Call the parent's __init__ method to set name and health
# 3. Set the armor attribute

class Warrior(GameCharacter):
    def __init__(self, name, health, armor):
        super().__init__(name, health)
        self.armor = armor


    ### Exercise 2 ###
    # Override the take_damage method in the Warrior class to:
    # 1. Reduce the damage by the armor amount (damage - armor)
    # 2. Ensure the damage is at least 1 (if damage after reduction is less than 1)
    # 3. Call the parent's take_damage method with the adjusted damage

    # Hint:
    # def take_damage(self, damage_amount):
    #     # Your armor reduction logic here
    #     return super().take_damage(adjusted_damage)
    
    def take_damage(self, damage_amount):
        if (damage_amount - self.armor) >= 1:
            adjusted_damage = (damage_amount - self.armor)
            return super().take_damage(adjusted_damage)
        else:
            return super().take_damage(1)


### Exercise 3 ###
# Create a Mage class that inherits from GameCharacter with:
# 1. An __init__ method that takes name, health, and mana
# 2. Call the parent's __init__ method
# 3. Add a fireball method that:
#    - Takes an opponent parameter (another GameCharacter)
#    - Deals 50 damage if mana >= 20
#    - Reduces mana by 20
#    - Returns the spell success (True if cast, False if not enough mana)

class Mage(GameCharacter):
    def __init__(self, name, health, mana):    
        super().__init__(name, health)
        self.mana = mana
        
    def fireball(self, opponent):
        if self.mana >= 20:
            opponent.take_damage(50)
            self.mana -= 20
            return True
        else:
            return False
            


# Tests #
def runtests():
    print("Test 1: Warrior inheritance")
    warrior = Warrior("Conan", 150, 10)
    print(f"Expected name: Conan, Got: {warrior.name}")
    print(f"Expected health: 150, Got: {warrior.health}")
    print(f"Expected armor: 10, Got: {warrior.armor}")
    print(f"Test passed: {warrior.name == 'Conan' and warrior.health == 150 and warrior.armor == 10}")
    
    print("\nTest 2: Warrior damage reduction")
    warrior.take_damage(15)
    print(f"Expected health after 15 damage with 10 armor: 145, Got: {warrior.health}")
    print(f"Test passed: {warrior.health == 145}")
    
    print("\nTest 3: Warrior minimum damage")
    warrior.take_damage(5)  # With 10 armor, should only take 1 damage
    print(f"Expected health after 5 damage with 10 armor (min 1): 144, Got: {warrior.health}")
    print(f"Test passed: {warrior.health == 144}")
    
    print("\nTest 4: Mage inheritance and methods")
    mage = Mage("Merlin", 90, 100)
    print(f"Expected name: Merlin, Got: {mage.name}")
    print(f"Expected health: 90, Got: {mage.health}")
    print(f"Expected mana: 100, Got: {mage.mana}")
    print(f"Test passed: {mage.name == 'Merlin' and mage.health == 90 and mage.mana == 100}")
    
    print("\nTest 5: Mage casting fireball")
    opponent = GameCharacter("Enemy", 100)
    spell_success = mage.fireball(opponent)
    print(f"Expected spell success: True, Got: {spell_success}")
    print(f"Expected opponent health after fireball: 50, Got: {opponent.health}")
    print(f"Expected mage mana after fireball: 80, Got: {mage.mana}")
    print(f"Test passed: {spell_success and opponent.health == 50 and mage.mana == 80}")
    
    print("\nTest 6: Mage with insufficient mana")
    mage.mana = 10  # Set mana low
    spell_success = mage.fireball(opponent)
    print(f"Expected spell success: False, Got: {spell_success}")
    print(f"Expected opponent health unchanged: 50, Got: {opponent.health}")
    print(f"Expected mage mana unchanged: 10, Got: {mage.mana}")
    print(f"Test passed: {not spell_success and opponent.health == 50 and mage.mana == 10}")

runtests()

### Lesson - Unit Testing in Python ###

# Purpose: Unit tests validate that individual functions work correctly
# When to use: When developing new features or fixing bugs to ensure code reliability
# Example: Testing game mechanics like combat, inventory, or level progression

import unittest

### Exercise 1 ###
# Create a function with these requirements:
# 1. Takes a player level (int) and returns the max health for that level
# 2. The health calculation is: base_health(100) + (level * 10)
# 3. If level is negative, raise a ValueError with message "Level cannot be negative"

def calculate_max_health(level):
    """Calculate a player's maximum health based on their level"""
    if level < 0:
        raise ValueError("Level cannot be negative")
    else:
        return 100 + (level * 10)


### Exercise 2 ###
# Create a function with these requirements:
# 1. Calculate damage dealt based on weapon power and critical hit chance
# 2. If critical (critical=True), multiply damage by 2
# 3. If the target has armor, reduce damage by armor value
# 4. Return the final damage (minimum 1, even with high armor)

def calculate_damage(weapon_power, critical=False, armor=0):
    """Calculate damage dealt to a target"""
    # Start with base damage
    damage = weapon_power
    
    if critical:
        damage = damage * 2
        
    damage = damage - armor
        
    if damage < 1:
        damage = 1
        
    return damage


### Exercise 3 ###
# Create a function with these requirements:
# 1. Simulates gaining experience points and potentially leveling up
# 2. Takes current level, current XP, and XP gained
# 3. Returns tuple of (new_level, new_xp) after gaining experience
# 4. Level increases each time XP reaches level * 100

def gain_experience(current_level, current_xp, xp_gained):
    """Add experience and handle level up if necessary"""
    new_level = current_level
    new_xp = current_xp + xp_gained
        
    # Keep leveling up as long as we have enough XP
    while new_xp >= new_level * 100:
        new_xp = new_xp - (new_level * 100)  # Subtract XP needed for current level
        new_level += 1                      # Increase level
    
    return (new_level, new_xp)


# Tests #
class GameMechanicsTests(unittest.TestCase):
    
    def test_max_health_calculation(self):
        """Test that max health is calculated correctly for different levels"""
        # Testing normal cases
        self.assertEqual(calculate_max_health(1), 110, "Level 1 health should be 110")
        self.assertEqual(calculate_max_health(5), 150, "Level 5 health should be 150")
        self.assertEqual(calculate_max_health(10), 200, "Level 10 health should be 200")
        
        # Testing edge case (level 0)
        self.assertEqual(calculate_max_health(0), 100, "Level 0 health should be 100")
        
        # Testing that negative level raises ValueError
        with self.assertRaises(ValueError):
            calculate_max_health(-1)
    
    def test_damage_calculation(self):
        """Test that damage is calculated correctly with criticals and armor"""
        # Basic damage test
        self.assertEqual(calculate_damage(50), 50, "Base damage should be the weapon power")
        
        # Critical hit test
        self.assertEqual(calculate_damage(50, critical=True), 100, "Critical hit should double damage")
        
        # Armor reduction test
        self.assertEqual(calculate_damage(50, armor=20), 30, "Armor should reduce damage")
        
        # Armor with critical test
        self.assertEqual(calculate_damage(50, critical=True, armor=20), 80, "Critical, then armor reduction")
        
        # Minimum damage test
        self.assertEqual(calculate_damage(10, armor=20), 1, "Damage should be at least 1")
    
    def test_experience_gain(self):
        """Test experience gain and leveling mechanics"""
        # Basic XP gain, no level up
        self.assertEqual(gain_experience(1, 50, 20), (1, 70), "Should gain XP without level up")
        
        # XP gain causing level up
        self.assertEqual(gain_experience(1, 90, 20), (2, 10), "Should level up and carry over XP")
        
        # Multiple level ups
        self.assertEqual(gain_experience(5, 50, 500), (6, 50), "Should handle multiple level ups")
        
        # Edge case - exact XP for level up
        self.assertEqual(gain_experience(2, 150, 50), (3, 0), "Should level up with exact XP")

if __name__ == '__main__':
    unittest.main()

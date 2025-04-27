### Lesson - Logging in Python ###

# Purpose: Logging provides a way to track events in your game without using print statements
# When to use: For debugging, tracking game state, or recording player actions
# Example: Logging player movement, combat events, or errors in game code

import logging
import random
import time

### Exercise 1 ###
# Create a function that:
# 1. Sets up a basic logger with a specified log level
# 2. Configures it to log to both console and a file
# 3. Returns the configured logger

def setup_game_logger(log_level=logging.INFO):
    """Setup and configure a logger for the game"""
    # Create a logger
    logger = logging.getLogger("game")

    # Set the log level
    logger.setLevel(log_level)  # log_level is passed as parameter

    # Create logs directory if it doesn't exist
    import os
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Create a file handler that logs to a file in the logs directory
    log_file_path = os.path.join(logs_dir, "game.log")
    file_handler = logging.FileHandler(log_file_path)

    # Create a console handler that logs to console
    console_handler = logging.StreamHandler()

    # Create a formatter to control the format of log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Return the configured logger
    return logger


### Exercise 2 ###
# Create a function that simulates a player moving through a game world:
# 1. Takes a logger and direction string (north, south, east, west)


def move_player(logger, direction):
    """Simulate player movement with logging"""
    
    # 2. Logs the attempt to move with INFO level
    logger.info(direction)
    
    # 3. 20% chance to encounter an obstacle (log as WARNING)
    if random.randint(1, 100) <= 20:
        logger.warning("Obstacle encountered")
        return False
    
    # 4. 10% chance to encounter an error (log as ERROR)
    if random.randint(1, 100) <= 10:
        logger.error("Error encountered")
        return False
    
    # 5. Returns True if movement succeeded
    logger.info(f"Successfully moved {direction}")
    return True
        
    


### Exercise 3 ###
# Create a function that simulates a battle between player and enemy:
# 1. Takes a logger, player_health, and enemy_health

def battle_enemy(logger, player_health, enemy_health):
    """Simulate a battle with detailed logging"""
    # 2. Logs the start of battle as INFO
    logger.info("Battle has started")
    
    # 3. Simulates 3 rounds of combat, dealing random damage (1-10)    
    # 4. Logs each attack and resulting health as DEBUG
    i = 1
    while i <= 3 and player_health > 0:
        damage = random.randint(1, 10)
        player_health = player_health - damage
        logger.debug(f"Enemy attacks for {damage} damage. Player has {player_health}")    
        i += 1
    
    # 5. Logs the outcome (victory/defeat) as INFO
    if player_health > 0:
        logger.info("Victory")
    else:
        logger.info("Defeat")
    
    # 6. Returns the player's remaining health (0 if defeated)

    return player_health
 
    


# Tests #
def runtests():
    # Clean up any previous log file
    import os
    if os.path.exists("game.log"):
        os.remove("game.log")
    
    # Test Exercise 1: Logger Setup
    print("Test 1: Setting up Logger")
    logger = setup_game_logger()
    
    if logger and isinstance(logger, logging.Logger):
        print("Logger created successfully")
        test1 = True
    else:
        print("Failed to create logger")
        test1 = False
    
    # Test Exercise 2: Movement Logging
    print("\nTest 2: Player Movement")
    
    # Try multiple moves to ensure we see all outcomes
    directions = ["north", "south", "east", "west"]
    results = []
    
    print("Making several moves (see logs for details):")
    for _ in range(10):
        direction = random.choice(directions)
        result = move_player(logger, direction)
        results.append(result)
    
    success_rate = results.count(True) / len(results)
    print(f"Movement success rate: {success_rate:.0%}")
    test2 = True  # We can't easily test random outcomes
    
    # Test Exercise 3: Battle System
    print("\nTest 3: Battle System")
    initial_health = 50
    enemy_health = 30
    
    remaining_health = battle_enemy(logger, initial_health, enemy_health)
    print(f"Player started with {initial_health} health")
    print(f"Player ended with {remaining_health} health")
    
    if 0 <= remaining_health <= initial_health:
        print("Battle simulation completed correctly")
        test3 = True
    else:
        print("Battle returned invalid health value")
        test3 = False
    
    # Check if log file was created and has content
    if os.path.exists("game.log") and os.path.getsize("game.log") > 0:
        print("\nLog file created successfully! Content preview:")
        with open("game.log", "r") as f:
            lines = f.readlines()
            # Show first 5 lines of the log
            for line in lines[:5]:
                print(f"  {line.strip()}")
            if len(lines) > 5:
                print(f"  ... and {len(lines) - 5} more lines")
        print("\nCheck game.log for complete logs")
    else:
        print("\nLog file missing or empty")
    
    print(f"\nTests passed: {all([test1, test2, test3])}")

runtests()

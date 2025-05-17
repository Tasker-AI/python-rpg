### Python RPG
The player is stranded on an island and must build a boat and sail to freedom. The player explores, collects items, battle enemies, and completes quests.

## Getting Started
1. Clone this repository
2. Run `python main.py` to start the game

### Project Structure
assets/
    images/
    maps/
    sounds/
logs/
saves/
src/
    engine/
    entities/
        player/
        enemies/
        resources/
        items/
    game_state/
    interfaces/
        player_menu/
    main_menu/
tests/
main.py
README.md
TODO.md

### Game World
- The game world is represented as a tile-based map (32x32 pixel tiles)
- Different terrain types (grass, water, trees, rocks, etc.) with varying walkability
- Multiple distinct areas (towns, dungeons, forests, etc.)
- NPCs with dialogue and quests
- Collision detection for impassable terrain and objects
- Player character always centered on screen with the map scrolling around them
- All resource images (trees, rocks, etc.) must have transparent backgrounds using colorkey=-1 (top-left pixel color)
- Resources should have a high Z-index to ensure they appear above the player character

### Game Mechanics
1. **Movement**: Tile-based movement system
   - Click on a tile to show a visual indicator and queue movement
   - Movement only occurs on game ticks (every 0.6 seconds)
   - Multiple clicks queue up with only the most recent being processed
   - A* pathfinding to find optimal path
   - Each tile movement takes one game tick (0.6 seconds)
   - Diagonal movement allowed when no obstacles block the way
   - Visual feedback shows where clicks occur
   - Player character remains centered on screen at all times
   - Map scrolls to follow player movement
2. **User Interface**: All interactions are mouse-based
   - Mouse-only controls (no keyboard input)
   - Click to move, click buttons for actions
   - Visual indicators show where clicks occur
   - Actions queue up and execute on game ticks
   - Minimalist UI with clear feedback
   - Health, stats, and inventory displays
3. **Input System**
   - Mouse-only controls
   - Click to show indicator and queue movement
   - Visual feedback for all clicks
   - Tick-based action processing (0.6 seconds per tick)
   - Click on objects to interact
   - Click on UI buttons for menus and actions
   - Click on enemies to attack them
3. **Combat**: Game tick based combat system
   - Each game tick is exactly 0.6 seconds
   - Player attacks each x ticks, depending on the weapon speed
   - Enemy attacks each x ticks, depending on the enemy
   - Damage calculation based on attack, defense, armor, and random factors
   - Enemy has a certain range, and will stop attacking if player is outside of this range
3. **Inventory Management**:
   - Collect and use items (weapons, armor, potions, resources)
   - Equip items to improve stats
   - Drop or sell unwanted items
   - Inventory has 28 slots
   - Bank has 100 slots. Items can be deposited or withdrawn to inventory
4. **Save/Load System**:
   - Save game progress to a file automatically every game tick
   - Load game progress automatically from a file
   - Ability to choose your character before logging in.
5. **Quest System**:
   - Simple quest with objectives
   - Track progress using variables and dictionaries
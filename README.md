# Pygame Platformer Shooter
#### Video Demo:  https://youtu.be/epoN0hi4lVM
#### Description:

A 2D platformer shooter game featuring combat, collectibles, and multiple levels built with Pygame.

Description:
A 2D platformer shooter game built with Pygame that combines classic platformer mechanics with combat elements. Players navigate through multiple levels while battling enemies, collecting items, and avoiding environmental hazards.
Implementation Details
The project consists of several key Python files and resource directories:
game.py (Main Game File)

Implements the core game loop and state management
Handles window creation and basic Pygame setup (800x600 resolution)
Contains the main player class with movement physics, health system, and combat mechanics
Implements enemy AI with patrolling and combat behaviors
Manages collision detection between entities
Handles user input for movement (WASD/Arrow keys) and combat (Space/Q)

button.py (UI Components)

Contains the Button class for menu interface elements
Handles button states (hover, click)
Manages button positioning and scaling

Level Design System

Uses CSV files (level1_data.csv, level2_data.csv, level3_data.csv) for level layouts
Implements tile-based level loading with different tile types:

Ground/platform tiles (collision-enabled)
Water hazards (damage-dealing)
Decoration tiles (background elements)
Item spawn points
Enemy spawn locations



Asset Management

Organized in dedicated directories:

/img: Contains sprite sheets and tile sets
/audio: Stores sound effects and background music
/Background: Parallax scrolling background elements
/explosion: Animation frames for explosions
/icons: UI elements and item icons



Design Choices
Health and Combat System
I chose to implement a health-based combat system instead of one-hit deaths to provide more engaging gameplay. Players have 100 health points and can find health pickups throughout levels. Enemies also have health bars, requiring multiple hits to defeat.
Level Design Approach
The decision to use CSV files for level design allows for easy level creation and modification without changing the game code. I considered using JSON but chose CSV for its simplicity and readability when designing levels.
Movement Physics
The player's movement uses velocity-based physics with gravity (0.75) and jump mechanics. I experimented with different values and settled on these numbers to achieve a balance between responsive controls and realistic feel.
Enemy AI
Enemies use a simple but effective patrol-and-chase AI system. They patrol within set boundaries until the player enters their vision range (150 pixels), then switch to attack mode. This creates predictable but challenging encounters.
Technical Challenges
The biggest challenge was implementing smooth collision detection between entities. Initially, I used simple rectangle collisions, but this led to clipping issues. The solution was to implement separate collision checks for horizontal and vertical movement.
Another significant challenge was optimizing the background rendering with parallax scrolling. The initial implementation caused frame rate drops on slower systems. I solved this by pre-rendering background elements and implementing view culling for off-screen objects.
Future Improvements

Add saving/loading system for game progress
Implement more enemy types with different behaviors
Add power-ups that modify player abilities
Create a level editor for custom level design
Improve particle effects for explosions and impacts

## Requirements
- Python 3.x
- Pygame

## Installation
```bash
# Install Pygame
pip install pygame

# Clone the repository
git clone https://github.com/yourusername/pygame-shooter.git

# Navigate to game directory
cd pygame-shooter
```

## Controls
- A/Left Arrow: Move left
- D/Right Arrow: Move right
- W/Up Arrow: Jump
- SPACE: Shoot
- Q: Throw grenade
- ESC: Pause game

## Project Structure
```
pygame-shooter/
├── audio/
│   ├── jump.wav
│   ├── shot.wav
│   ├── grenade.wav
│   └── music2.mp3
├── img/
│   ├── Background/
│   ├── Tile/
│   ├── explosion/
│   ├── icons/
│   └── player/
├── level{1,2,3}_data.csv
├── button.py
└── game.py
```


## License
This project is licensed under the MIT License.

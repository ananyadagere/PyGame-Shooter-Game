# Pygame Platformer Shooter

A 2D platformer shooter game featuring combat, collectibles, and multiple levels built with Pygame.

## Features
- Player movement with platform physics
- Combat system with shooting and grenades
- Enemy AI with patrol and attack behaviors
- Health and ammunition management
- Collectible items and coins
- Multiple levels with CSV-based level design
- Parallax scrolling background
- Sound effects and background music
- Pause and settings menu
- Screen transitions and fade effects

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

## Features Documentation

### Player
- Health system with regeneration pickups
- Ammunition management
- Grenade throwing with blast radius
- Smooth animation system

### Combat
- Bullet-based shooting system
- Grenade explosions with varying damage radius
- Enemy AI with patrol and combat behaviors
- Health bars and damage indicators

### Level Design
- CSV-based level loading system
- Multiple tile types (terrain, water, decorations)
- Collectible items and power-ups
- End-level exits

### UI System
- Health and ammo display
- Coin counter
- Pause menu
- Settings with music controls
- Death screen with restart option

## License
This project is licensed under the MIT License.

# ZLOCK CHAINER

A 3D blockchain-themed puzzle game inspired by classics like Lumines and Columns. Match colored chain links in a 6×6×25 grid to clear blocks and unleash devastating special abilities!

**Arcade Version:** 0.21.2  
**Tunnels Version:** 0.2.10  
**Created by:** CyberAxe of [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

---

## About

ZLOCK CHAINER is a **two-game universe** combining arcade puzzle action with dungeon crawler RPG adventure:

### **ZLOCK CHAINER (Arcade Game)** - `zlock_consensus.html`
A fast-paced 3D puzzle game where you drop falling chains into a grid and match 6 or more connected blocks of the same color to clear them. As you progress through levels, unlock new chain types including encrypted chains, glowing chains, and multi-colored chains. Charge up four unique character abilities to turn the tide when the grid gets full!

### **TUNNELS OF PRIVACY (Dungeon Crawler)** - `tunnels_of_privacy.html`
A classic dungeon crawler RPG inspired by TI-99's "Tunnels of Doom". Take the same four heroes from the arcade game into a 10-level dungeon quest to find the king's scepter. Features D&D-style stats, turn-based combat, and roguelike exploration.

### **Portal System - Seamless Game Integration**
Both games share a unified save file system with **bidirectional hero progression**:
- Play arcade, power up heroes, enter portal → continue in dungeon with same heroes
- Explore dungeon, level up heroes, exit portal → return to arcade with upgraded stats
- Single save file (`top_shared_save`) stores progress for both games
- Download/upload save files for backups and cross-browser play

## Features

### Arcade Game (zlock_consensus.html)
- **3D Puzzle Gameplay** - 6×6×25 grid with full 3D chain placement
- **Four Character Abilities** - Each with unique board-clearing powers
- **Progressive Difficulty** - Speed increases each level, new chain types unlock at levels 10, 25, and 50
- **Gamepad Support** - Full Xbox/PlayStation/Steam controller support
- **20 Visual Grid Effects** - Customize the grid with effects like Pulse Wave, Rainbow Spectrum, Plasma Field, and more
- **Particle System** - Custom particle effects for abilities and chain destruction
- **High Score Tracking** - Local high score persistence
- **Portal to Dungeon** - Enter portal button to launch Tunnels of Privacy with shared heroes

### Dungeon Crawler (tunnels_of_privacy.html)
- **Classic Dungeon Crawling** - Inspired by TI-99's "Tunnels of Doom"
- **Four Playable Heroes** - Same heroes from arcade with D&D-style stats (STR, DEX, CON, INT, WIS, CHA)
- **Hero Progression** - Stats, HP, AC, XP, and levels carry between both games
- **Educational Ticker** - Learn about Zcash and privacy tech while browsing menu
- **Music System** - 10 theme tracks with scrolling ticker display
- **Loading Screen** - Full asset preload system with progress tracking
- **Settings Panel** - Independent music/volume controls
- **Exit Portal** - Return to arcade game with preserved progress

### Portal Save System
- **Unified Save Format** - Single save file with hero stats + game states for both games
- **Download Save File** - Backup your progress as JSON file to computer
- **Load Save File** - Upload save files to restore progress or play across browsers
- **Cross-Game Progression** - Hero stats update in real-time across both games
- **localStorage Persistence** - Automatic save on portal entry/exit
- **Version Migration** - Future-proof save system with version compatibility

## How to Play

### Getting Started
1. Open `zlock_consensus.html` to play the arcade puzzle game
2. OR open `tunnels_of_privacy.html` to start the dungeon crawler
3. Use the **Portal System** to switch between games while preserving hero progress

### Portal System Usage
**From Arcade Game:**
- Press **ESC** to pause
- Click **ENTER PORTAL** button (purple, with 🌀 icon)
- Game saves automatically and launches Tunnels of Privacy
- Your arcade progress and hero stats transfer to dungeon

**From Dungeon Game:**
- Click **EXIT PORTAL** button on main menu (purple, with 🌀 icon)
- Game saves automatically and returns to arcade
- Your dungeon progress and upgraded hero stats return to arcade
- Arcade game resumes from where you left off

**Save File Management:**
- **Download Save File** - Backup progress as `zlock-save-level{X}-{date}-{time}.json`
- **Load Save File** - Upload save file from title screen to restore progress
- Works across browsers and computers
- Compatible with both arcade and dungeon games

### Arcade Game Objective
Connect 6 or more blocks of the same color to clear them and score points. Don't let the grid fill to the top!

### Controls

**Keyboard:**
- **Arrow Keys** - Move falling chain left/right/forward/back
- **A/D** - Rotate chain 90°
- **Space** - Drop faster (double-tap for instant drop)
- **Q/E** - Rotate camera
- **T** - Toggle top-down view
- **1/2/3/4** - Activate character special abilities

**Gamepad:**
- **Left Stick** - Move chain
- **A Button** - Drop (double-tap for instant)
- **B Button** - Rotate chain
- **Y Button** - Flip chain
- **LB/RB** - Rotate camera
- **D-Pad** - Character abilities (Up/Down/Left/Right)
- **Start** - Pause
- **Select** - Toggle top-down view

## Chain Types

- **Standard Chains** - Four colors (Gold, Blue, Green, Red)
- **Multi-Color Chains** - Unlocks at level 10, random colors per link
- **Encrypted Chains** - Unlocks at level 25, takes 9 seconds to decrypt
- **Glowing Chains** - Unlocks at level 50, break connections and worth bonus points

## Character Abilities

Charge abilities by clearing matching colored chains:

- **Zooko (1 or D-Pad Up)** - Destroys all blocks of the most common type
- **Nate (2 or D-Pad Down)** - Eliminates all glowing links, then tornado shuffle
- **Zancas (3 or D-Pad Left)** - Transforms the 2 most common types to gold
- **CyberAxe (4 or D-Pad Right)** - Fires laser down the falling chain's column

## Installation

### Quick Start
1. Clone or download this repository
2. **IMPORTANT:** Run the Python server: `python zlock_server.py`
   - Server runs on `http://localhost:4243`
   - Required for proper MIME types for 3D models (.glb files)
   - Do NOT use other simple HTTP servers (they will fail on GLB files)
3. Open browser to:
   - `http://localhost:4243/zlock_consensus.html` - Arcade game
   - `http://localhost:4243/tunnels_of_privacy.html` - Dungeon crawler
4. No build process required - runs entirely in the browser!

### File Structure
- `zlock_consensus.html` - Main arcade puzzle game
- `tunnels_of_privacy.html` - Dungeon crawler RPG
- `particle_editor.html` - Particle effect creation tool
- `zlock_server.py` - Development server (REQUIRED for local play)
- `effect/` - Particle effect JSON files
- `models/` - 3D models (GLB format)
- `music/` - Theme music tracks (10 songs shared across both games)
- `sound_effects/` - SFX for gameplay
- `story/` - Story intro/outro animations
- `ticker_facts.json` - Educational Zcash/privacy facts for ticker

### Save Files
- **Shared Save:** `localStorage['top_shared_save']` - Heroes + arcade state + dungeon state
- **Arcade Settings:** `localStorage['zlock_settings']` - Arcade-specific settings
- **Tunnels Settings:** `localStorage['top_tunnels_settings']` - Dungeon-specific settings
- **Download Format:** JSON files compatible with both games

## Development

### Technology Stack
- **Three.js** - 3D rendering for arcade game
- **GLTFLoader** - 3D model loading
- **Vanilla JavaScript** - No frameworks, no build step
- **Custom Particle System** - Sprite sheet animation engine
- **localStorage API** - Cross-game save system
- **FileReader/Blob APIs** - Save file download/upload

### Project Architecture
- **Monolithic Design** - Both games are single-file HTML with embedded JavaScript
- **No Build Step** - Edit HTML/JS files directly, refresh browser to test
- **Python Server Required** - `zlock_server.py` serves correct MIME types for GLB models
- **Particle Editor** - Standalone tool (`particle_editor.html`) for creating visual effects

### AI Coding Standards for This Project

**CRITICAL RULES - ALL AI ASSISTANTS MUST FOLLOW:**

1. **Standardization is MANDATORY:**
   - When told to implement features "the same way" as arcade game, DO NOT create new names/structures
   - Use EXACT variable names, function names, and patterns from reference code
   - Example: Use `themeTracks` NOT `dungeonMusicTracks`
   - Example: Use `loadMusic()` NOT `loadDungeonMusic()`
   - Search ALL occurrences before renaming - fix all references in ONE operation

2. **Complete Feature Copying:**
   - When copying a system from arcade to tunnels (or vice versa), copy ALL parts
   - Do NOT skip features like ticker facts, hover effects, or educational content
   - If arcade has ticker facts system, tunnels MUST have identical ticker facts system
   - "The same" means IDENTICAL, not "similar" or "close enough"

3. **Multi-Operation Changes:**
   - Use `multi_replace_string_in_file` for related changes across same/multiple files
   - Do NOT make partial changes that require follow-up fixes
   - Example: Renaming a function? Fix ALL call sites in same operation
   - Search for dependencies BEFORE making changes, not after

4. **No Assumptions - Verify Everything:**
   - Do NOT assume code works without reading it
   - Do NOT claim features exist without verifying in actual code
   - If unsure, read the file and search for actual implementation
   - User reports are accurate - trust them over assumptions

5. **File Structure Awareness:**
   - `zlock_consensus.html` - Arcade game (~16,500 lines)
   - `tunnels_of_privacy.html` - Dungeon crawler (~1,400 lines)
   - Both are monolithic single-file architectures
   - Search before adding to avoid duplication

6. **Save System Standards:**
   - Shared save key: `top_shared_save`
   - Contains: `saveVersion`, `lastPlayed`, `arcadeState`, `dungeonState`, `heroes`
   - Heroes object has 4 heroes: `zooko`, `nate`, `zancas`, `cyberaxe`
   - Each hero has: `str`, `dex`, `con`, `int`, `wis`, `cha`, `hp`, `maxHp`, `ac`, `xp`, `level`
   - NEVER export just `gameState` - always export complete shared save

7. **Music System Standards (BOTH GAMES):**
   - Variable name: `themeTracks` (NOT dungeonMusicTracks, NOT musicTracks)
   - Function name: `loadMusic()` (NOT loadDungeonMusic, NOT playMusic)
   - Ticker format: `♫ Theme Song: [name] ♫ • [Random Fact]`
   - Ticker structure: `#musicTicker` > `#musicTickerWrapper` > `.tickerText` spans
   - Hover effect: 30s animation → 60s on hover
   - Facts loaded from: `ticker_facts.json`

8. **Volume System Standards:**
   - Slider range: 1-150 (user-facing)
   - Audio element range: 0.0-1.0 (browser API)
   - Conversion: `Math.min(1.0, sliderValue / 100)`
   - NEVER set audio.volume above 1.0 (causes IndexSizeError)

9. **Testing Requirements:**
   - After implementing feature, verify it works
   - Check for console errors
   - Test hover effects, button clicks, state changes
   - If user reports bug, investigate actual code - don't guess

10. **Documentation Updates:**
    - Update version numbers in BOTH title and GAME_VERSION constant
    - Add comprehensive changelog entries with technical details
    - Document breaking changes and migration paths
    - Include code examples in changelogs for complex features

### Particle System Development
Includes a particle effect editor (`particle_editor.html`) for creating and editing particle effects. Effects saved as JSON in `effect/` directory and loaded by both games.

### Common Development Tasks

**Starting Development Server:**
```powershell
python zlock_server.py
```

**Editing Game Logic:**
- Search for existing functions before adding new ones (files are large)
- Read surrounding code to understand state flow
- UI elements are HTML overlaid on canvas (`#hud`, `#titleScreen`)

**Creating Particle Effects:**
1. Open `particle_editor.html` in browser
2. Design effect with visual editor
3. Export JSON to `effect/` directory
4. Reference in game code by filename

**Testing Portal System:**
1. Start from arcade game
2. Play a few levels to generate save data
3. Click "Enter Portal" in pause menu
4. Verify hero stats appear in dungeon game
5. Click "Exit Portal" in dungeon
6. Verify return to arcade with same state

**Save File Testing:**
1. Download save file from arcade game
2. Clear localStorage or switch browser
3. Load save file from title screen
4. Verify all data restored correctly
5. Test in both arcade and dungeon games

## Support the Developer

If you enjoy ZLOCK CHAINER, consider donating:

**Zcash Address:**  
`u1gvnthgukm0ecnan3tgj3h6pdhrmmv8zyqx8ayup9yg9er4t5l7nesas6leavc4x3rsj98n65nn2w3ekzur9yejadlmv7k4vjgu8kp58q`

---

**License:** All rights reserved  
**Website:** [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

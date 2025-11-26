# TUNNELS OF PRIVACY - Game Design Document

**Current Version:** v0.2.10  
**Last Updated:** November 25, 2025  
**Status:** Phase 1 Complete - Portal & Menu System Fully Implemented

## Project Overview
Tunnels of Privacy is a dungeon crawler game inspired by the classic TI-99/4A game "Tunnels of Doom" (1982). It shares a universe with ZLOCK CHAINER (arcade puzzle game) through a bidirectional save/load portal system.

## Current Implementation Status

### ✅ COMPLETED - Phase 1: Portal & Menu System
- [x] Portal system with seamless arcade ↔ dungeon navigation
- [x] Complete unified save system with hero progression
- [x] Title screen with animated background
- [x] Hero party display with live stats
- [x] Music system with 10 theme tracks
- [x] Music player controls (play/pause, prev/next, volume)
- [x] Educational ticker with Zcash/privacy facts
- [x] Settings panel with independent music controls
- [x] Loading screen with asset preload
- [x] Save file download/upload functionality
- [x] Complete standardization with arcade naming conventions

### 🚧 IN PROGRESS - Phase 2: Core Dungeon Systems
- [ ] Dungeon generation (procedural levels)
- [ ] Movement and exploration
- [ ] Combat system (turn-based)
- [ ] Inventory and equipment
- [ ] Hero stat progression

### 📋 PLANNED - Phase 3: Content & Polish
- [ ] Enemy types and AI
- [ ] Loot tables and items
- [ ] Quest system
- [ ] Boss encounters
- [ ] Story integration

## Core Concept
- **Genre**: Dungeon crawler RPG
- **Theme**: D&D-style fantasy adventure in blockchain-themed dungeons
- **Inspiration**: Tunnels of Doom (1982) + roguelike mechanics
- **Connection**: Same 4 heroes from ZLOCK CHAINER arcade game

## The Two-Game Loop System

### ZLOCK CHAINER → Tunnels of Privacy
1. Player clicks "Enter Portal" button (under TV in arcade)
2. ZLOCK CHAINER saves arcade state to localStorage
3. Opens `tunnels_of_privacy.html` in same window
4. Tunnels of Privacy loads shared save data
5. Imports: level (dungeon depth), hero stats, score (gold)

### Tunnels of Privacy → ZLOCK CHAINER
1. Player clicks "Exit Portal" button (in dungeon menu)
2. Tunnels of Privacy saves dungeon state + updated hero stats
3. Opens `zlock_consensus.html` in same window
4. ZLOCK CHAINER loads arcade save + updated hero stats
5. Resumes arcade game with powered-up heroes

## Shared Save File Structure

### Storage Key
`zlock_crossgame_save` - Single save file shared between both games

### Save Data Schema
```javascript
{
  version: "1.0.0",  // Versioning for save upgrades
  timestamp: 1234567890,
  
  // Arcade game state
  arcade: {
    level: 42,
    score: 15000,
    combo: 1.0,
    startLevel: 1,
    usedAI: false,
    occupiedCells: [...],
    zookoCharge: 75,
    nateCharge: 50,
    zancasCharge: 60,
    cyberaxeCharge: 80,
    gameStartTime: 1234567890,
    totalPausedTime: 5000,
    fallingChain: {...},
    chainQueue: [...]
  },
  
  // Dungeon crawler state
  dungeon: {
    currentLevel: 5,
    gold: 500,
    inventory: [],
    questProgress: {},
    dungeonSeed: "abc123",
    position: { x: 10, y: 15 },
    inCombat: false
  },
  
  // Shared hero stats (both games use these)
  heroes: {
    zooko: {
      name: "Zooko",
      class: "Wizard",
      str: 8, dex: 11, con: 10, int: 15, wis: 13, cha: 9,
      hp: 22, maxHp: 25, ac: 12,
      level: 3, xp: 1250
    },
    nate: {
      name: "Nate",
      class: "Rogue",
      str: 10, dex: 15, con: 11, int: 11, wis: 12, cha: 8,
      hp: 26, maxHp: 28, ac: 14,
      level: 3, xp: 1100
    },
    zancas: {
      name: "Zancas",
      class: "Cleric",
      str: 12, dex: 13, con: 13, int: 9, wis: 14, cha: 10,
      hp: 28, maxHp: 30, ac: 15,
      level: 3, xp: 1300
    },
    cyberaxe: {
      name: "CyberAxe",
      class: "Fighter",
      str: 14, dex: 10, con: 14, int: 8, wis: 9, cha: 10,
      hp: 32, maxHp: 35, ac: 16,
      level: 3, xp: 1400
    }
  }
}
```

## Save Version System

### Version Format
`MAJOR.MINOR.PATCH` (e.g., "1.0.0")

### Upgrade Path
When loading a save with older version:
1. Check `save.version` vs `CURRENT_SAVE_VERSION`
2. Apply migration functions in sequence
3. Update `save.version` to current
4. Save updated file

### Migration Functions
```javascript
// Example: v1.0.0 → v1.1.0 adds hero equipment slots
function migrateSave_1_0_0_to_1_1_0(save) {
  save.heroes.zooko.equipment = { weapon: null, armor: null, accessory: null };
  save.heroes.nate.equipment = { weapon: null, armor: null, accessory: null };
  save.heroes.zancas.equipment = { weapon: null, armor: null, accessory: null };
  save.heroes.cyberaxe.equipment = { weapon: null, armor: null, accessory: null };
  save.version = "1.1.0";
  return save;
}
```

## Tunnels of Privacy - Standalone Requirements

### Must Run Independently
- Own HTML file: `tunnels_of_privacy.html`
- Own settings system (separate from ZLOCK CHAINER)
- Own localStorage keys (prefixed `tunnels_`)
- Own start menu / title screen
- Own game loop / rendering system

### Start Menu Features
- NEW GAME - Create new dungeon run (initializes default hero stats)
- CONTINUE - Load from portal save (if exists)
- EXIT PORTAL - Return to ZLOCK CHAINER with save
- SETTINGS - Sound, music, display options
- CONTROLS - Keyboard/gamepad reference

### Settings Storage
`tunnels_settings` - Separate from arcade settings
```javascript
{
  sfxEnabled: true,
  musicEnabled: true,
  sfxVolume: 75,
  musicVolume: 50,
  showTutorial: true,
  difficulty: "normal"
}
```

## Implementation Phases

### ✅ Phase 1: Portal & Menu System (v0.1.0 - v0.2.10) - COMPLETED
**Status:** Fully implemented and standardized with arcade game

**Completed Features:**
- [x] Portal system with Enter/Exit buttons in both games
- [x] Unified save system (`top_shared_save`) with heroes, arcade state, dungeon state
- [x] Save file download/upload for backups and cross-browser play
- [x] Title screen with animated background (story intro sprite sheet)
- [x] Hero party display with live stat updates (STR, DEX, CON, INT, WIS, CHA, HP, AC, Level, XP)
- [x] Music system with 10 theme tracks (same tracks as arcade)
- [x] Music player controls: play/pause, previous/next, volume slider (1-150 range)
- [x] Educational ticker system with Zcash/privacy facts from `ticker_facts.json`
- [x] Ticker hover slow-down effect (30s → 60s animation)
- [x] Settings panel with independent music controls
- [x] Loading screen with progress bar and asset preload
- [x] Standardized naming: `themeTracks`, `loadMusic()` matching arcade
- [x] Proper HTML/CSS structure matching arcade exactly

**Technical Implementation:**
- Functions: `exitPortal()`, `loadSharedSave()`, `saveSharedSave()`, `createDefaultSharedSave()`
- Music system: `loadMusic()`, `fadeMusic()`, `musicPlayPause()`, `musicPrevious()`, `musicNext()`
- Ticker system: Loads `ticker_facts.json`, picks random fact per track, displays with music info
- Asset preloading: Images + music with progress tracking
- localStorage keys: `top_shared_save`, `top_tunnels_settings`

**Files Modified:**
- `tunnels_of_privacy.html` - Complete UI and save system (1,398 lines)
- `zlock_consensus.html` - Portal entry, save download fix
- `ticker_facts.json` - Shared educational content

### 🚧 Phase 2: Core Dungeon Systems (NEXT) - NOT STARTED
**Target:** First playable dungeon gameplay

**Features to Implement:**
- [ ] Dungeon level generation (procedural or pre-designed)
  - Grid-based or free-form movement
  - Room generation with corridors
  - Entrance/exit stairs placement
  
- [ ] Player movement and exploration
  - Keyboard/gamepad controls
  - First-person or top-down view
  - Collision detection
  - Fog of war / unexplored areas
  
- [ ] Basic combat system
  - Turn-based encounters
  - Attack/defend/flee options
  - Damage calculation using hero stats
  - Enemy AI patterns
  
- [ ] Inventory management
  - Item pickup and storage
  - Equipment slots (weapon, armor, accessory)
  - Item usage (potions, scrolls)
  - Weight/capacity limits
  
- [ ] Hero stat progression
  - XP gain from combat
  - Level up system
  - Stat increases on level up
  - Skill/ability unlocks

**Technical Requirements:**
- Dungeon data structure (grid, rooms, entities)
- Rendering system (2D canvas or Three.js)
- Input handling (movement, combat, inventory)
- Game state machine (exploring, combat, menu, paused)
- Entity system (heroes, monsters, items, NPCs)

### 📋 Phase 3: Content & Polish (FUTURE) - NOT STARTED
**Target:** Full game experience with story progression
**Features to Implement:**
- [ ] Enemy types and behaviors
  - 50+ unique monster types across dungeon levels
  - Boss encounters on milestone levels
  - Enemy AI with different attack patterns
  - Loot drops and XP rewards
  
- [ ] Item and equipment system
  - Weapons (swords, staffs, bows, etc.)
  - Armor (light, medium, heavy)
  - Accessories (rings, amulets, cloaks)
  - Consumables (health potions, scrolls, bombs)
  - Rarity tiers (common, uncommon, rare, legendary)
  - Equipment stats and bonuses
  
- [ ] Quest system
  - Main quest: Find the Sceptre of Privacy (Level 100)
  - Side quests from NPCs
  - Quest tracking UI
  - Rewards (gold, XP, unique items)
  
- [ ] Merchant and town systems
  - Safe zones with shops
  - Buy/sell items
  - Equipment upgrades
  - Inn for healing/saving
  
- [ ] Story integration
  - Cutscenes on milestone levels
  - NPC dialogue system
  - Lore books and environmental storytelling
  - Connection to arcade game story (TV broadcasts)
  
- [ ] Visual and audio polish
  - Particle effects for spells/abilities
  - Sound effects for combat/exploration
  - Music tracks for different dungeon zones
  - UI animations and transitions

**Technical Requirements:**
- Enemy database with stats and behaviors
- Item/equipment database with properties
- Quest management system
- Dialogue engine
- Save/load for all new systems
- Achievement tracking

---

## AI Coding Standards for Tunnels of Privacy

**MANDATORY RULES - ALL AI ASSISTANTS WORKING ON THIS PROJECT:**

### 1. STANDARDIZATION WITH ARCADE GAME
When implementing features that exist in `zlock_consensus.html` (arcade), you MUST use identical naming and structure:

**Music System:**
- ✅ Variable: `themeTracks` (NOT dungeonMusicTracks, musicTracks, or trackList)
- ✅ Function: `loadMusic()` (NOT loadDungeonMusic, playMusic, or startMusic)
- ✅ Ticker format: `♫ Theme Song: [name] ♫ • [Random Fact]`
- ✅ HTML structure: `#musicTicker` > `#musicTickerWrapper` > `.tickerText` spans
- ✅ Animation name: `scrollTicker` (NOT scroll-left or ticker-scroll)

**Save System:**
- ✅ Shared save key: `top_shared_save` (NOT zlock_crossgame_save or portal_save)
- ✅ Properties: `saveVersion`, `lastPlayed`, `arcadeState`, `dungeonState`, `heroes`
- ✅ Heroes: `zooko`, `nate`, `zancas`, `cyberaxe` (lowercase, exact spelling)
- ✅ Download function MUST export complete shared save (NOT just gameState)

**Volume System:**
- ✅ Slider range: 1-150 (user-facing)
- ✅ Conversion: `Math.min(1.0, sliderValue / 100)` to clamp at 1.0
- ✅ NEVER set `audio.volume` above 1.0 (causes IndexSizeError)

### 2. COMPLETE FEATURE IMPLEMENTATION
When told to "add X system the same way as arcade":
- ❌ DO NOT skip any sub-features (like ticker facts when implementing ticker)
- ❌ DO NOT create "simplified" or "minimal" versions
- ✅ Copy ALL components: HTML structure, CSS styling, JavaScript logic, data loading
- ✅ Include hover effects, animations, error handling, console logging
- ✅ Verify feature completeness by comparing side-by-side with arcade code

### 3. MULTI-OPERATION CHANGES
When making changes that affect multiple locations:
- ✅ Use `multi_replace_string_in_file` to batch all related changes
- ✅ Search for ALL occurrences of old name/pattern BEFORE making changes
- ✅ Fix all references in ONE operation, not iteratively
- ❌ DO NOT rename a function and leave broken call sites for later

**Example - Renaming a function:**
```javascript
// WRONG: Change function name only
function loadMusic() { ... }  // Renamed but calls still use old name

// RIGHT: Find all 6 call sites, fix in one multi_replace operation
// 1. Function definition
// 2. ended event listener
// 3. musicPlayPause() call
// 4. musicPrevious() call  
// 5. musicNext() call
// 6. initialization call
```

### 4. VERIFICATION REQUIREMENTS
Before marking a feature complete:
- ✅ Read the actual code to verify implementation exists
- ✅ Check browser console for errors after implementation
- ✅ Test interactive features (hover, clicks, volume changes)
- ✅ Compare with arcade version for identical behavior
- ❌ DO NOT assume code works without verification
- ❌ DO NOT claim features exist without reading source

### 5. FILE STRUCTURE AWARENESS
- `tunnels_of_privacy.html` - Monolithic single-file architecture (~1,400 lines)
- All CSS in `<style>` tag within HTML
- All JavaScript in `<script>` tag within HTML
- Search for existing functions before adding new ones
- Use `grep_search` or `read_file` to get context before editing

### 6. VERSION AND CHANGELOG MANAGEMENT
When updating code:
- Update BOTH `<title>` tag and `GAME_VERSION` constant
- Add entry to `TUNNELS_OF_PRIVACY_CHANGELOG.md` with:
  - Version number (follow sequence: v0.2.9 → v0.2.10 → v0.2.11)
  - Summary of changes
  - Detailed feature descriptions
  - Technical implementation notes
  - Code examples for complex features
- Include date (format: 2025-11-25)
- List all modified files

### 7. USER FEEDBACK HANDLING
When user reports a bug or missing feature:
- ✅ Trust the user's report - they are seeing the actual behavior
- ✅ Investigate the actual code to find root cause
- ✅ Provide detailed explanation of what was wrong
- ❌ DO NOT guess at solutions without reading code
- ❌ DO NOT defend incorrect implementations
- ❌ DO NOT claim "it should work" - verify it DOES work

### 8. DOCUMENTATION ACCURACY
- README.md contains overall project documentation
- TUNNELS_OF_PRIVACY_DESIGN.md contains design specs and progress tracking
- TUNNELS_OF_PRIVACY_CHANGELOG.md contains version history
- All docs must be kept in sync with actual implementation
- Update phase completion status as features are implemented

### 9. TESTING CHECKLIST
After implementing any feature:
```
[ ] Code compiles without syntax errors
[ ] No console errors on page load
[ ] Feature works as intended (manual test)
[ ] Matches arcade behavior (if applicable)
[ ] All related functions updated
[ ] Version number incremented
[ ] Changelog updated
[ ] Design doc updated if phase complete
```

### 10. COMMON PITFALLS TO AVOID
- ❌ Renaming variables without fixing all references
- ❌ Copying only part of a feature (missing CSS, HTML, or JS)
- ❌ Using different animation names, IDs, or class names than arcade
- ❌ Making assumptions about localStorage key names
- ❌ Setting audio.volume outside 0.0-1.0 range
- ❌ Exporting gameState instead of complete shared save
- ❌ Adding global event listeners that trigger unwanted behavior
- ❌ Skipping error handling or null checks
- ❌ Forgetting to update version numbers
- ❌ Implementing features without reading reference code first

---

## Technical Notes

### Portal Transition Flow
```
ARCADE                          DUNGEON
  |                                |
  | Click "Enter Portal"           |
  |                                |
  | Save arcade state              |
  | Save hero stats                |
  |                                |
  | window.location = "tunnels..." |
  |                                |
  | ─────────────────────────────> |
  |                                |
  |                         Load shared save
  |                         Show start menu
  |                                |
  |                  Click "Exit Portal"
  |                                |
  |                    Save dungeon state
  |                    Save hero stats
  |                                |
  |     window.location = "zlock..." |
  |                                |
  | <───────────────────────────── |
  |                                |
  | Load arcade save               |
  | Load updated hero stats        |
  | Resume gameplay                |
```

### File Structure
```
~workingfolder/
  ├── zlock_consensus.html      # Arcade puzzle game
  ├── tunnels_of_privacy.html   # Dungeon crawler (NEW)
  ├── zlock_server.py            # Development server (serves both)
  ├── models/                    # Shared 3D models
  ├── sound_effects/             # Shared audio (or separate folders)
  └── story/                     # Shared story animations
```

## Hero Classes (Initial Stats)

### Zooko (Wizard)
- STR: 8, DEX: 11, CON: 10, INT: 15, WIS: 13, CHA: 9
- Role: Ranged magic damage, crowd control
- Special: Shield ability (from arcade)

### Nate (Rogue)
- STR: 10, DEX: 15, CON: 11, INT: 11, WIS: 12, CHA: 8
- Role: High mobility, critical hits, traps
- Special: Time manipulation (from arcade)

### Zancas (Cleric)
- STR: 12, DEX: 13, CON: 13, INT: 9, WIS: 14, CHA: 10
- Role: Healing, support, buffs
- Special: Orb/energy attacks (from arcade)

### CyberAxe (Fighter)
- STR: 14, DEX: 10, CON: 14, INT: 8, WIS: 9, CHA: 10
- Role: Tank, melee damage, area attacks
- Special: Electric wall ability (from arcade)

## Story Integration

### THE 1,000-LEVEL ZCASH DUNGEON (FINAL STRUCTURE)

#### DESCENT ARC (Levels 1–100)
Going down into the deep cryptographic underworld, culminating in the ultimate boss and the Sceptre of Privacy.

**Levels 1–10 — The Unshielded Approach**
- Tutorial surface tunnels
- Weak monsters: Leak Imps, Dustlings, Metadata Wisps

**Levels 11–20 — The Broken Ledger Halls**
- Enemies representing surveillance and transparency decay
- Monsters: Auditor Fragments, Watcher Golems

**Levels 21–30 — The Trusted Setup Catacombs**
- Crypts full of failed parameters and ceremony relics
- Miniboss: The Parameter Shade

**Levels 31–40 — The Forked Maze**
- Shifting corridors, unstable consensus, block ghost illusions

**Levels 41–50 — The Fungibility Labyrinth**
- Hydra-tainted coins, shifting purity, value illusions

**Levels 51–60 — The Counterfeit Vaults**
- Nullifier Shades, Supply Phantoms, Issuance Oozes

**Levels 61–70 — The Orchard Sanctum**
- Shielded temples, proof angels, unified-address spirits

**Levels 71–80 — The Halo Spiral**
- Recursive paradox rooms, proof-clones, anti-entropy storms

**Levels 81–90 — The Identity Depths**
- Sybil illusions, multiplicity monsters, identity storms

**Levels 91–99 — Descent to the Core**
- Total darkness, decentralization pressure, proto-boss entities

**LEVEL 100 — THE MAIN BOSS: THE CENTRALIZER**
- The one true final boss of the entire storyline
- A world-eating machine-god that thrives on concentration of power, surveillance, single points of failure, and economic oppression
- Defeating it grants **The Sceptre of Privacy**:
  - Mythical artifact forged from shielded proof light, distributed consensus fire, entropy crystals, and the last purified nullifier seal
  - Protects identity, value, and autonomy
  - Enables the heroes to ascend back to the surface

#### ASCENT ARC (LEVELS 101–1000)
The story flips: You climb up, escaping the depths, bringing privacy back to the surface world.

**Levels 101–300 — The Rising Tunnels**
- Fight upward against collapsing caverns and corrupted constructs
- "Echo" monsters from Descent Arc (weaker versions of previous threats)

**Levels 301–600 — The Breaking Shadows**
- Mid-ascent enemies attempt to reclaim the Sceptre
- Enemies: Chain Reorg Worms, Entropy Thieves, Proof Leeches
- Light of the surface grows brighter as you climb

**Levels 601–800 — The Great Uprising**
- Begin meeting villages, towns, and resistance factions who cheer you on
- Light replaces darkness, monsters become rare
- Traps and environmental puzzles dominate

**Levels 801–899 — The Air of Freedom**
- Open caverns resemble the surface world
- Wildlife returns
- Shops, shrines, and resting spots appear
- Occasional minibosses tied to "unfinished business"

**LEVELS 900–990 — THE FINAL BOSS RUSH (ASCENT GAUNTLET)**
- Not story bosses - remaining echoes of the Centralizer's power
- Final remnants of corruption trying to stop your return
- Bosses include:
  - The Auditor Titan Shade
  - The Last Forking Wyrm
  - The Fungibility Hydra Remnant
  - The Halo Paradox Echo
  - The Sybil King's Final Form
  - The Inflation Demon's Shell
  - The Ledger Colossus Fragment

---

## Development Progress Summary

**Version:** v0.2.10 (November 25, 2025)

**Phase 1 Complete:**
- Portal system (enter/exit between games)
- Unified save with heroes (download/upload)
- Title screen with animated background
- Hero party display (4 heroes, live stats)
- Music system (10 tracks, controls, ticker)
- Educational ticker (ticker_facts.json)
- Settings panel
- Loading screen with preload
- Full standardization with arcade

**Phase 2 - NOT STARTED:**
- Dungeon gameplay
- Combat system
- Inventory/equipment
- Level generation
- Hero progression

**Next Steps:** Implement core dungeon systems
- Each weaker than original form, appearing back-to-back
- Tone: Not grim - this is cleanup, a heroic march

**LEVELS 991–1000 — THE VICTORY CLIMB**
- No combat - only beauty, story, nostalgia

**Level 991–995 — The Golden Caverns**
- Gentle crystalline halls that glow with shielded light
- Peaceful NPCs, memory echoes of your journey, merchants, music

**Level 996–998 — The Echo of Good Times**
- Snapshots of major victories
- Old friends, small puzzles, optional lore

**Level 999 — The Final Sunwell**
- The end of the tunnel
- You see daylight, soft music
- NPCs begin gathering at the exit

**LEVEL 1000 — SURFACE RETURN: THE CELEBRATION**
- You emerge to cheering crowds
- The world celebrates the return of freedom, privacy, and autonomy
- The Sceptre of Privacy illuminates the sky
- No battle - only victory
- **This is the true ending**

## Design Philosophy
- Keep it simple and fun
- Respect player time (quick save/load)
- Seamless integration (feels like one game)
- Standalone playability (dungeon works alone)
- Stat synergy (dungeon progress helps arcade, arcade progress helps dungeon)

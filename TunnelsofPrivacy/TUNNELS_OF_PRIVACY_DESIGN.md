# TUNNELS OF PRIVACY - Game Design Document

**Current Version:** v0.2.22  
**Last Updated:** November 26, 2025  
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


TITLE / HIGH CONCEPT

This is a Zcash-themed, D&D-style dungeon crawler inspired by Tunnels of Doom, Eye of the Beholder, and classic turn-based RPGs. The focus is on:

- Menu-driven exploration instead of FPS or free movement.
- A 1 000 level mega-dungeon.
- Deep procedural generation using Level Profiles, not prebuilt maps.
- Party based, turn-based combat against monsters and bosses that personify cryptography, privacy, and Zcash ideas.

The player controls 1–4 heroes. Battles are side-view, turn-based. Exploration is abstracted into menus and procedural room generation, not walking around a 3D dungeon.


CORE LOOP OVERVIEW

1. Player clicks “Start Adventure”.
2. A new run is created with a global seed and 1 000 level profiles.
3. The player is taken to the Dungeon Menu for the current level.
4. From the Dungeon Menu they choose actions like Explore Level, Inventory, Rest, etc.
5. “Explore Level” resolves into opening rooms and encounters based on that level’s profile.
6. Battles, traps, events, and NPC interactions are resolved through menus and separate combat scenes.
7. After dealing with rooms and finding the exit, the player descends or ascends a level.
8. Main story is completed at level 100 when the main boss is defeated and the Sceptre of Privacy is obtained.
9. Levels 101–1000 are the ascent back to the surface, including a late-game boss rush and finally a non-combat victory climb.


DUNGEON MENU (LEVEL HUB UI)

This replaces FPS movement. Every level has a Dungeon Menu that appears as a centered UI panel styled to match the main arcade game UI (same fonts, colors, visual language).

Core entries:

1. Explore Level  
   - Main exploration button.
   - When pressed, it rolls to determine what kind of room or encounter the party enters next, based on the Level Profile and remaining room counts.

2. Explorer Level  
   - Shows current depth (1–1000), overall danger rating, environmental modifiers, and discovered traits of this level.

3. Level Store (Enter Level Store, if found)  
   - Only active after the player discovers a Store Room on this level.
   - Allows buy, sell, repair, and possibly identify items depending on store type.

4. Inventory  
   - Manage items, equipment, consumables.
   - Equip gear, inspect stats, sort items.

5. Rest / Sleep  
   - Use camp resources to restore HP, mana, and remove some conditions.
   - May trigger Rest events (ambush, dreams, NPC visits) based on level risk.

Additional menu entries that complete the Tunnels of Doom style loop:

6. Party Status  
   - Overview of party members, HP, mana, buffs, debuffs, experience, and conditions.

7. Level Map  
   - Abstract auto-map. No FPS. Just a list or simple node map of known rooms, room types, and which ones still have unknown content.
   - Shows Entry, Exit, Store, Boss, and key rooms once discovered.

8. Camp / Use Skills  
   - Non-sleep actions.
   - Activate out-of-combat skills, rituals, crafting, short buffs, detection spells, etc.

9. Identify Items  
   - Spend resources, gold, scrolls, or skills to identify unknown items.
   - Supports classic “this sword might be cursed” style gameplay.

10. Manage Party / Formation  
    - Choose which heroes are active.
    - Set formation (frontline, midline, backline) if your combat system uses it.

11. Bestiary / Lore Log  
    - View info on monsters, bosses, rooms, and lore unlocked through exploration.


1 000 LEVEL STRUCTURE

The dungeon has 1 000 levels. The structure is:

- Levels 1–100: Descending into the deep. Main story arc.
- Level 100: Main boss battle against The Centralizer. Defeat it to obtain the Sceptre of Privacy.
- Levels 101–1000: Ascending back to the surface with the sceptre. Endgame arc.
- Levels 900–990: Final boss rush sequence, fighting remnant echoes of earlier bosses.
- Levels 991–1000: Ease-off, non-combat victory climb back to the surface and final celebration.

Detailed structure:


DESCENT ARC: LEVELS 1–100

Theme: Going down into the cryptographic underworld, discovering how privacy, surveillance, and decentralization clash.

Suggested narrative beats by range:

Levels 1–10: The Unshielded Approach  
- Tutorial zone.
- Basic monsters (Leak Imps, Dustlings, simple traps).
- Teaches rest, inventory, and basic room types.

Levels 11–20: The Broken Ledger Halls  
- Surveillance themes.  
- Enemies: Auditor Fragments, Watcher Golems.  
- Rooms with public ledgers, scrying mirrors, listening devices.

Levels 21–30: The Trusted Setup Catacombs  
- Crypts of failed ceremonies and forgotten parameter shards.  
- Mini-boss: Parameter Shade, guarding relics of the old trusted setup.

Levels 31–40: The Forked Maze  
- Shifting paths, timelines, and chain splits.  
- Instability, chain-reorg style events.

Levels 41–50: The Fungibility Labyrinth  
- Hydra-like monsters representing tainted coins and chain analysis.  
- Boss or mini-boss: Fiend of Fungibility.

Levels 51–60: The Counterfeit Vaults  
- NULL and inflation threats.  
- Boss: Inflation Demon, attempting to create undetectable counterfeit currency.

Levels 61–70: The Orchard Sanctum  
- Sacred forests and temples themed around the shielded pool and unified addresses.  
- Boss: Orchard Seraph (guardian, not necessarily evil unless corrupted).

Levels 71–80: The Halo Spiral  
- Recursive space. Rooms loop forward and backward symbolically.  
- Boss: Halo Prime, a paradoxical entity representing trustless recursive proofs.

Levels 81–90: The Identity Depths  
- Sybil illusions, copies, and deception.  
- Boss: Sybil King, an endlessly cloning shapeshifter.

Levels 91–99: Descent to the Core  
- Extreme darkness, pressure, and residual centralizing forces.  
- Stronger versions of earlier threats.

Level 100: Throne of Decentralization  
- Main story boss: The Centralizer.  
- A machine-god that consumes hashpower, identity, and governance to create a single point of control.

Defeating The Centralizer grants the Sceptre of Privacy.


THE SCEPTRE OF PRIVACY

A legendary artifact that combines:

- Shielded proof light (zero-knowledge proofs).
- Distributed consensus flame.
- Entropy crystals purified from the Catacombs.
- Final sealed nullifier.

Game effect conceptually:

- Protects the party’s identity and transactions.
- Opens the path upward toward freedom.
- Might grant bonuses to stealth, resistance to surveillance, and special abilities in later levels.


ASCENT ARC: LEVELS 101–1000

Now the story flips. You are climbing up to the surface, bringing privacy to the world above. Enemies are remnants and echoes trying to drag you back down.

High level zones:

Levels 101–300: The Rising Tunnels  
- Still dangerous, but difficulty gradually shifts from oppressive to hopeful.
- You encounter weakened forms of previous enemies and new threats now trying to reclaim the Sceptre.

Levels 301–600: The Breaking Shadows  
- Shadows of old power structures crumble.
- Enemies are more opportunistic than dominant.
- This midgame is where growth and mastery are highlighted.

Levels 601–800: The Great Uprising  
- You start finding small settlements, rebels, and underground communities that support you.
- More Safe Rooms, Stores, Shrines, and NPC Rooms.
- Environmental hazards lessen. Focus shifts to story events, choices, and optional encounters.

Levels 801–899: The Air of Freedom  
- Caverns open up. Sky crystals, air vents, and early glimpses of daylight.
- Occasional minibosses representing unresolved conflicts from the lower depths.

Levels 900–990: The Final Boss Rush (Remnants)  
- You fight “echo” versions of major bosses. They are weaker but come in sequence across these levels. Examples:
  - Auditor Titan Shade
  - Last Forking Wyrm
  - Fungibility Hydra Remnant
  - Halo Paradox Echo
  - Sybil King Final Echo
  - Inflation Demon Shell
  - Ledger Colossus Fragment
- This is a heroic cleanup, not a new main story climax. The emotional tone should be victorious and confident, not grim.

Levels 991–995: The Golden Caverns  
- Beautiful crystalline halls, peaceful.  
- Rest, shops, shrines, lore, and nostalgia.  
- No forced combat.

Levels 996–998: Echo of Good Times  
- Scenes that recall major victories or key NPCs from earlier in the run.  
- Optional micro-events, story reflection, last chance to prepare gear.

Level 999: Final Sunwell  
- You see the end of the tunnel and the light of the world.  
- NPCs gather at the threshold.  
- This is the emotional climax of the ascent, still no big fight.

Level 1000: Surface Return – Celebration  
- No battle.  
- The world celebrates the return of privacy and freedom.  
- The Sceptre of Privacy is recognized as a symbol of people’s control over their own information.  
- Endgame and credits area, with possible new game plus hooks.


DND STYLE BOSSES AND MONSTERS (CONCEPTS)

Boss archetypes used in the design:

- Protocol Wraith: bound to failed trusted setup parameters.
- Auditor Titan: giant stone ledger golem representing surveillance.
- Fiend of Fungibility: hydra of tainted vs clean coins.
- Consensys Spider: web of stale blocks and forks.
- Halo Prime: guardian of recursive proofs.
- Inflation Demon: counterfeit supply demon.
- Orchard Seraph: angelic guardian of the shielded pool.
- Sybil King: shapeshifter spawning multiple fake identities.
- The Centralizer: main boss of level 100.

Monster concepts used as room content:

- Leak Imps: whisper transaction metadata to enemies.
- Fee Wisps: drain coins in unstable conditions.
- View-Key Revenants: haunt dropped viewing keys.
- Nullifier Shades: track repeat actions and double spends.
- Dustlings: tiny creatures made of low-value dust.
- Chain-Reorg Worms: undo areas behind you.
- Memo Wisps: carry encrypted messages that may help or explode.
- Sync Ghouls: undead that constantly rescan their own memory.
- Watcher Golems: constructs that enforce total visibility.
- Anchor Slimes: sticky blobs representing outdated anchors.


PROCEDURAL GENERATION SYSTEM

Goal: Make many levels and rooms feel fresh each game without pre-generating or storing every room. The player might see only a fraction of the content in any run, but the world should still be consistent within that run.

Approach: Level Profiles and on-demand room generation.

Key principles:

1. You do not generate the entire map or all rooms in advance.
2. You only generate a small Level Profile for each level at the start of the run, based on a seed.
3. When a room is entered for the first time, its content is rolled based on the Level Profile and remaining counts.
4. Once generated, that room’s content is fixed for the rest of the run.
5. Using deterministic RNG with the global seed and room coordinates guarantees that the same run is reproducible.


LEVEL PROFILE

Every level from 1 to 1000 has a Level Profile that contains:

A. Room Type Distribution  
   Counts or weights for each room category (see the 50 room types below). Example for a simple early level:

   - Monster Rooms: 10
   - Elite Monster Rooms: 2
   - Mini-Boss Rooms: 1
   - Store Rooms: 0
   - Loot Rooms (Common): 5
   - Trap Rooms: 5
   - Safe Rooms: 2
   - Hidden Rooms: 2
   - Treasure Chest Rooms: 4
   - etc.

B. Level Modifiers  
   Global modifiers that affect all encounters on that level. Examples:

   - Acidic air: small poison chance at the start of each combat.
   - Blessed floor: increased loot quality, reduced trap frequency.
   - Cursed floor: increased curse rolls, higher enemy crit rate.
   - Wandering merchant present.
   - Hidden rooms spawn rate increased.
   - Environmental storms: occasional cave-ins, lightning events.

C. Encounter Tables  
   Weighted lists of possible encounters for this level:

   - Monster table: which enemies can appear and how often.
   - Trap table: trap types, damage ranges, status effects.
   - NPC table: friendly, neutral, hostile NPC types.
   - Loot table: item rarity, gold range, special drops.
   - Event table: text-based scenarios and choices.

D. Special Rooms Flags  
   - Must contain 1 Entry Room and 1 Exit Room.
   - Some levels contain required rooms, such as Boss Room for key milestones.
   - For level 100, the Boss Room for The Centralizer is mandatory.


ON DEMAND ROOM GENERATION

1. At the start of the level, the Level Profile is known but rooms are not instantiated.
2. When the player chooses “Explore Level”, choose or create the next room by:
   - Checking how many rooms of each type are still available (according to counts).
   - Rolling a room type using weighted probabilities constrained by remaining counts.
   - Generating the room’s specific content (monsters, NPCs, traps, loot) using that level’s encounter tables.
3. Decrease the remaining count for that room type.
4. Store the generated room result keyed by a deterministic identifier (for example, room index or coordinate plus level number and global seed).
5. Future visits to the same room reuse the stored result. No rerolling.

The result is that levels feel large and handcrafted, but you never waste CPU or design effort on rooms the player will not see.


FULL ROOM TYPE LIST (50 TYPES)

The dungeon uses 50 distinct room archetypes. These are abstract types used by the procedural system. Each gets a short behavior description.

1. Entry Room  
   - Spawn point for the level. No threats. Establishes the theme.

2. Exit Room  
   - Leads to the next level up or down. May be locked or gated by conditions.

3. Monster Room  
   - Standard enemies. Main combat content. Drops common loot.

4. Elite Monster Room  
   - Tougher enemies with better stats and skills. Increased rewards.

5. Mini-Boss Room  
   - Strong unique enemy or group. Often guards keys or major items.

6. Level Boss Room  
   - The main boss of this level (for story or milestone levels). Level 100 uses this for The Centralizer.

7. Loot Room (Common)  
   - Low to mid tier items, gold, consumables. Usually little or no combat.

8. Loot Room (Rare)  
   - High tier gear or rare items. Usually has traps, puzzles, or tough defenders.

9. Trap Room  
   - Focused on traps. Light or no monsters. Includes arrows, pits, magical traps, gas vents.

10. Environmental Hazard Room  
    - Hazards like collapsing ceilings, lava flows, toxic pools, extreme cold or heat. May require skill checks.

11. Puzzle Room  
    - Riddles, pattern matching, symbol combinations, logic or resource puzzles. Often gates good loot or shortcuts.

12. Skill Check Room  
    - Requires specific stats or skills (strength to push a block, magic to dispel a ward, tech to hack a device). Success or failure alters the room outcome.

13. Store Room  
    - A merchant or vending construct. Buy, sell, repair, identify. Only accessible if discovered on the level.

14. Shrine / Blessing Room  
    - Offers blessings, buffs, heals, or curses based on choices or offering resources.

15. Good NPC Room  
    - Friendly NPC. Quests, lore, trading, healing, or temporary ally.

16. Bad NPC Room  
    - Hostile or deceptive NPC. Might ambush, scam, or trigger bad events.

17. Event Room  
    - Text or menu based random event. Multiple choice outcomes.

18. Safe Room  
    - No combat. Safe place to rest, manage inventory, talk, or save.

19. Hidden Room  
    - Only accessible through secret doors, hidden switches, spells, or skills. Weighted toward rare loot or lore.

20. Secret Door Room  
    - Appears as a normal wall until detected. May connect important shortcuts.

21. Critter Room  
    - Non lethal creatures (mice, bats, small spirits). Used for flavor, small resources, or subtle hints.

22. Treasure Chest Room  
    - One or more chests. Some may be mimics or trapped. Contains concentrated loot.

23. Cursed Room  
    - Strong negative aura. Higher curse chance, debuffs, corruption effects, but sometimes high reward.

24. Magic Well / Mana Recharge Room  
    - Recharges mana or special abilities. Possibly with side effects.

25. Weapon Forge / Repair Room  
    - Smith, magical forge, or tech bench. Repair gear, upgrade items, or craft new equipment.

26. Library / Archive Room  
    - Shelves and archives. Discover lore, spell scrolls, map fragments, or secrets.

27. Armory Cache Room  
    - Racks of weapons and armor. High chance for combat gear. May be guarded or trapped.

28. Alchemy Lab Room  
    - Potions, ingredients, experimentation. Can brew or loot potions, with chance of accidents.

29. Rune Chamber  
    - Floor or wall runes. Activating them triggers buffs, debuffs, traps, or teleports.

30. Fountain of Restoration  
    - Heals HP or removes conditions. Sometimes cursed or tainted, occasionally offering risk vs reward choices.

31. Teleporter Chamber  
    - Sends the party to another discovered room or unknown location. May create shortcuts or risks.

32. Mirror Room  
    - Magical mirrors. Can show future events, create clones, or reveal illusions. Sometimes spawns mirror enemies.

33. Beast Lair Room  
    - Nest or lair of a particular creature. Optional or mandatory fight. Good loot if cleared.

34. Hall of Whispers  
    - Voices in the dark. Provide cryptic hints, reveal secrets, or mislead the player.

35. Treasure Vault (Heavy Lock)  
    - Defense focused room with a high security chest or vault. Requires multi-step unlocks or puzzles.

36. Prison Cell Block  
    - Cells with captives, dead prisoners, or hostile inhabitants. Releasing captives can create allies or new problems.

37. Portal Fragment Room  
    - Contains a fragment of a broken portal. Collecting or repairing multiple fragments may open shortcuts or secret realms.

38. Tomb of the Ancients  
    - Sarcophagi and coffins. Undead guardians and ancient relics. High risk, high reward.

39. Mushroom Grove / Myconid Den  
    - Fungal biome. Spores can heal, poison, or alter consciousness. Possible fungal NPC faction.

40. Dimensional Rift Room  
    - Reality is unstable. Random stat shifts, time distortions, or physics changes for this room or for a short duration.

41. Sound Trap Hall  
    - Sound reactive. Stepping or acting triggers traps via noise. Can be navigated quietly or by using sound-based skills.

42. Observation Room  
    - Scrying mirrors, crystals, or tech monitors. Lets the player peek at upcoming rooms, bosses, or secret areas.

43. Abandoned Camp  
    - Old adventurer camp. Leftover supplies, journals, or remains. May contain traps or clues.

44. Training Hall  
    - Targets, dummies, magical trainers. Temporary stat boosts, skill unlocks, or challenges.

45. Artifact Pedestal Room  
    - A single major item on a pedestal. Taking it can trigger traps, curses, guardian fights, or environmental changes.

46. Puzzle Lock Hallway  
    - Corridor that is itself a puzzle. Must align symbols, levers, or mechanisms to proceed.

47. Collapsed Passage  
    - Blocked path. Can be cleared with strength, spells, explosives, or special items. Possibly reveals new room clusters.

48. Infested Corridor  
    - Hordes of small enemies or spreading corruption. Damage over time zone, but yields resources or XP.

49. Echo Chamber  
    - Amplifies sound and illusions. Enemies appear duplicated, or echoes track the player’s choices.

50. Crystal Conduit Room  
    - Crystals channel energy. Can amplify spells, recharge items, or overload and explode if mishandled.


SUMMARY

The game is a menu driven mega dungeon inspired by Tunnels of Doom and D&D. It uses:

- 1 000 level structure with a 100 level descent and 900 level ascent.
- A deterministic procedural system based on Level Profiles and on demand room generation.
- A rich list of 50 room archetypes, bosses, monsters, and level modifiers.
- A Dungeon Menu that replaces FPS movement, letting you ship something solid in a short timeframe.

This document contains all necessary concepts for another AI or engine system to understand the world structure, procedural design, and core gameplay loops without needing external context.

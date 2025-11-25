# TUNNELS OF PRIVACY - Game Design Document

## Project Overview
Tunnels of Privacy is a dungeon crawler game inspired by the classic TI-99/4A game "Tunnels of Doom" (1982). It shares a universe with ZLOCK CHAINER (arcade puzzle game) through a bidirectional save/load portal system.

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

### Phase 1: Portal & Menu System (CURRENT)
- [ ] Add "Enter Portal" button to ZLOCK CHAINER (under TV)
- [ ] Create save function for cross-game data
- [ ] Create `tunnels_of_privacy.html` with basic structure
- [ ] Build start menu (based on ZLOCK CHAINER template)
- [ ] Add "Exit Portal" button to return
- [ ] Test seamless back-and-forth navigation

### Phase 2: Core Dungeon Systems (FUTURE)
- Dungeon generation (procedural levels)
- Movement and exploration
- Combat system (turn-based)
- Inventory and equipment
- Hero stat progression

### Phase 3: Content & Polish (FUTURE)
- Enemy types and AI
- Loot tables and items
- Quest system
- Boss encounters
- Story integration

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

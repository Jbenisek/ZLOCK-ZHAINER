# TUNNELS OF PRIVACY - Changelog

# Changelog

## v0.2.5 - Music Player UI Enhancement (2025-11-25)
- **Summary:**
  - Updated music player to match arcade game styling exactly
  - Added volume value display
  - Improved layout and centering
  - Added music icon to title

- **UI Improvements:**
  - **Music Controls Title**:
    - Added 🎵 music note icon to title
    - Changed from "Music Controls" to "🎵 Music Controls"
    - Matches arcade game branding
  
  - **Volume Display**:
    - Added real-time volume value display next to slider (e.g., "75")
    - Volume number updates instantly as slider moves
    - Styled with #2D9CDB color, JetBrains Mono font
    - Min-width: 30px, right-aligned for consistency
  
  - **Layout Improvements**:
    - Volume label now centered above slider
    - Slider and value display in flex container with proper alignment
    - Slider max-width: 200px for better proportions
    - Gap spacing matches arcade (8px between slider and value)
    - Proper vertical spacing (12px margin-bottom)

- **Functionality:**
  - `updateVolume()` now updates both slider and display value
  - `loadSettings()` initializes volume display on page load
  - Volume display syncs between main controls and settings panel
  - All volume changes reflected in real-time

- **Visual Consistency:**
  - Matches arcade game's music control layout exactly
  - Same font sizing (10px for labels)
  - Same color scheme (#BFD1E0 for labels, #2D9CDB for values)
  - Consistent spacing and alignment

---

## v0.2.4 - Volume Clamping Fix (2025-11-25)
- **Summary:**
  - Fixed HTMLMediaElement volume errors with proper clamping
  - Volume slider maintains 1-150 range but caps actual volume at 1.0
  - All volume assignments now properly validated

- **Bug Fixes:**
  - **Volume Clamping**:
    - Added `Math.min(1.0, musicVolume / 100)` to all volume assignments
    - Prevents "IndexSizeError: volume outside range [0, 1]" errors
    - Slider still shows 1-150 range for user control
    - Values above 100 are clamped to 1.0 before applying to audio element
  
  - **Fixed Functions**:
    - `updateVolume()` - Main volume slider now clamps correctly
    - `updateSettings()` - Settings panel slider clamps correctly
    - `loadDungeonMusic()` - Initial music load uses clamped volume
    - `fadeMusic()` - Already had proper 0-1 clamping

- **Technical Details:**
  - HTMLMediaElement.volume property only accepts 0.0 to 1.0
  - Slider range 1-150 divided by 100 gives 0.01-1.5
  - Math.min() ensures values never exceed 1.0
  - Maintains arcade game's slider range while respecting browser API limits

---

## v0.2.3 - Settings System Fixes (2025-11-25)
- **Summary:**
  - Fixed volume slider range to match arcade game exactly
  - Corrected HTMLMediaElement volume errors
  - Separated Tunnels settings from arcade settings
  - Improved volume control synchronization

- **Bug Fixes:**
  - **Volume System**:
    - Fixed volume slider range from incorrect 0.01-1.5 to correct 1-150 (matching arcade)
    - Fixed "IndexSizeError: volume outside range [0, 1]" errors
    - Volume now correctly divides by 100 (1-150 → 0.01-1.5) before applying to audio
    - Changed from parseFloat to parseInt for volume values
    - Display shows raw value (75) instead of percentage (75%)
  
  - **Settings Storage**:
    - Changed from shared `top_settings` to independent `top_tunnels_settings`
    - Tunnels now has its own separate settings file
    - Removed misleading "sync with arcade" message
    - Settings no longer conflict with arcade game settings
  
  - **Volume Control Synchronization**:
    - Main volume slider now syncs with settings panel slider
    - Both sliders update each other in real-time
    - Settings panel slider updates when using main controls
    - Volume changes persist to localStorage from both sliders

- **Improvements:**
  - Volume system now identical to arcade game implementation
  - Better error handling for volume clamping in fadeMusic()
  - More reliable settings persistence
  - Independent settings allow different preferences per game

---

## v0.2.2 - Settings System (2025-11-25)
- **Summary:**
  - Added settings panel matching arcade game structure
  - Music settings accessible from title screen
  - Settings persist via localStorage
  - Improved user control over music experience

- **Settings Panel:**
  - **Features**:
    - Music Enabled checkbox (toggle music on/off)
    - Music Volume slider (1-150 scale)
    - Settings modal with overlay dimming
    - Close button with keyboard-friendly icon
    - Version display in panel footer
  
  - **Functionality**:
    - Settings accessible from title screen via SETTINGS button
    - Click overlay to close panel
    - Settings persist to localStorage with "top_" prefix
    - Settings load automatically on page init
    - Volume changes apply immediately to playing music
    - Syncs with main volume slider in music controls
  
  - **Visual Design**:
    - Matches arcade game's panel styling
    - Gradient background with border glow (#2A9D8F)
    - Backdrop blur effect
    - Centered modal positioning
    - Responsive scrolling for smaller screens

- **Integration:**
  - Settings sync between title screen controls and settings panel
  - Music volume updates apply to currentMusic instantly
  - Settings saved to localStorage using STORAGE_KEYS.SETTINGS
  - loadSettings() called during init()
  - Prepared for future dungeon-specific settings

---

## v0.2.1 - Music Control Fixes (2025-11-25)
- **Summary:**
  - Fixed music control functionality bugs
  - Improved stat display error handling
  - Enhanced music playback behavior

- **Bug Fixes:**
  - **Music Controls**:
    - Fixed Play/Pause button not responding correctly
    - Fixed Previous/Next buttons not working
    - Fixed button state not updating properly
    - Next/Previous now auto-enable music if paused and start playing
  
  - **Hero Stats Display**:
    - Added null checks for all stat elements (CON, CHA)
    - Fixed "Cannot set properties of null" error on page load
    - Properly handles missing DOM elements gracefully
  
  - **Music System**:
    - Fixed `musicPlayPause()` function matching HTML button calls
    - Added proper music state tracking with `musicStarted` flag
    - Button text now updates based on actual playback state (▶/⏸)
    - Volume control works without requiring display element

- **Improvements:**
  - Music controls now behave identically to arcade game
  - Clicking Next/Previous while paused will resume playback
  - Better error handling throughout music system
  - More reliable button state synchronization

---

## v0.2.0 - UI Enhancements & Music System (2025-11-25)
- **Summary:**
  - Major UI overhaul with 3-column layout matching arcade game
  - Complete music system with 10 theme tracks
  - Enhanced hero party display with portraits and themed styling
  - Improved visual consistency across both games

- **Layout & UI:**
  - **3-Column Layout**:
    - Left Column: Hero Party cards (2x2 grid)
    - Center Column: Dungeon level display, menu buttons
    - Right Column: Available for future content
  - Changed from centered flexbox to absolute positioning for consistency
  - Matches arcade game's spatial organization

- **Hero Party Improvements:**
  - **Character Portraits**:
    - Circular 60px headshot images for each hero
    - Character-themed colored borders and glows:
      - Zooko: Red (#EB5757)
      - Nate: Yellow (#F2C94C)
      - Zancas: Green (#27AE60)
      - CyberAxe: Blue (#2E86DE)
  
  - **Stat Formatting**:
    - White monospace text (JetBrains Mono, bold)
    - HP displayed in red (#ff6b6b)
    - Two-column stat layout: STR/INT, DEX/WIS, CON/CHA
    - Added CON and CHA stats to complete D&D attribute set
    - Colored card borders matching character themes
    - Glowing box shadows on each card

- **Music System:**
  - **Track List** (10 theme songs):
    - Electric Coin Company
    - Zcash Foundation
    - Proof of Work Battle
    - ZecWallet Lite
    - Private by Default
    - Halo Arc Dreams
    - Mining the Future
    - zkSNARK Symphony
    - Trusted Setup Ceremony
    - Shielded Sunset
  
  - **Music Controls**:
    - Positioned at bottom center (65px from bottom)
    - Three-button layout: Previous, Play/Pause, Next
    - Volume slider (1-150 range)
    - Teal theme (#2A9D8F) with yellow text (#F2C94C)
    - Matches arcade game styling exactly
  
  - **Music Ticker**:
    - Positioned at bottom center (10px from bottom)
    - 600px width, scrolling animation
    - Displays current track name
    - Teal border with yellow text
  
  - **Playback Features**:
    - Random track selection from playlist
    - Automatic progression to next track on song end
    - Smooth 1-second crossfade between tracks
    - Non-blocking audio playback
    - Volume control affects all tracks

- **Visual Consistency:**
  - All UI elements now match arcade game styling:
    - Same fonts (JetBrains Mono for stats/controls)
    - Same color schemes (teal/yellow theme)
    - Same positioning system (absolute coords)
    - Same button styles and hover effects
  - Hero portraits use same compressed headshot images
  - Consistent backdrop blur and shadow effects

- **Technical Details:**
  - Music system functions:
    - `loadDungeonMusic(trackData)`: Load and crossfade tracks
    - `fadeMusic()`: 20-step fade in/out
    - `musicPlayPause()`: Toggle playback
    - `musicPrevious()` / `musicNext()`: Track navigation
    - `updateVolume()`: Volume slider handler
  - CSS Grid for hero party (2x2 layout)
  - Absolute positioning for all major UI sections
  - Responsive width constraints (max-width: 90%)

---

## v0.1.0 - Portal System & Initial Framework (2025-11-24)
- **Summary:**
  - Initial release of Tunnels of Privacy dungeon crawler
  - Portal system integration with ZLOCK CHAINER arcade game
  - Hero party display with shared progression
  - Menu framework ready for future dungeon gameplay

- **Portal System Features:**
  - **Exit Portal Button**: Returns to ZLOCK CHAINER arcade game
    - Purple-themed button with portal emoji (🌀)
    - Saves dungeon state before returning
    - Preserves hero stats and progression
  
  - **Shared Save System**:
    - localStorage key: `top_shared_save`
    - Seamless data sharing with arcade game
    - Version system (v1) for future save migrations
    - Automatic hero stat loading on launch

- **Hero Party Display:**
  - Four playable heroes: Zooko, Nate, Zancas, CyberAxe
  - D&D-style character stats displayed:
    - Level and HP (current/max)
    - STR, DEX, CON, INT, WIS, CHA attributes
  - Real-time stat updates from shared save
  - Stats carry over from arcade game progression

- **Main Menu:**
  - Title screen with purple portal aesthetic
  - Hero party cards showing current stats
  - Exit Portal button for return to arcade
  - Placeholder buttons for future features:
    - Start Adventure (coming soon)
    - Continue (coming soon)

- **Technical Implementation:**
  - Standalone HTML file (no dependencies on arcade game)
  - Separate localStorage namespace with "top_" prefix
  - Portal system functions:
    - `exitPortal()`: Save dungeon state and navigate to arcade
    - `loadSharedSave()`: Load cross-game save data
    - `saveSharedSave()`: Write cross-game save data
    - `migrateSharedSave()`: Version migration support
    - `updateHeroDisplay()`: Refresh hero stat UI
  - Initialization on page load (`init()` function)

- **Save Data Structure:**
  ```javascript
  {
    saveVersion: 1,
    lastPlayed: timestamp,
    arcadeState: { /* arcade game state */ },
    dungeonState: {
      currentLevel: 1,
      inventory: [],
      gold: 0,
      questProgress: {
        hasScepter: false,
        hasReturned: false,
        bossesDefeated: []
      }
    },
    heroes: {
      zooko: { name, str, dex, con, int, wis, cha, hp, maxHp, ac, xp, level },
      nate: { ... },
      zancas: { ... },
      cyberaxe: { ... }
    }
  }
  ```

- **Design Notes:**
  - Based on TI-99's "Tunnels of Doom" classic game
  - Story: Four heroes descend 10 dungeon levels
  - Quest: Find treasure and king's scepter, return to village
  - Shared narrative with ZLOCK CHAINER (story plays on TV screen)

- **Coming Soon (Phase 2):**
  - Dungeon crawler gameplay implementation
  - First-person or top-down dungeon navigation
  - Turn-based or real-time combat system
  - Procedurally generated dungeon levels
  - Inventory and equipment management
  - Merchant and treasure systems
  - Boss encounters on each floor
  - Quest progression tracking
  - Character leveling and stat growth
  - Permadeath or respawn mechanics
  - Sound effects and music
  - Story cutscenes and dialogue

---

**Installation:**
- Runs alongside ZLOCK CHAINER
- Access via "Enter Portal" button in arcade game
- No separate installation required

**System Requirements:**
- Modern web browser with localStorage support
- JavaScript enabled
- Same requirements as ZLOCK CHAINER

**Known Issues:**
- Dungeon gameplay not yet implemented (menu only)
- Hero stats are read-only (no leveling in dungeon yet)
- Inventory system placeholder only

**Credits:**
- Created by CyberAxe
- Part of the ZLOCK CHAINER universe
- Inspired by TI-99's "Tunnels of Doom"

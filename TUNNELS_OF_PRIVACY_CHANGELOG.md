# TUNNELS OF PRIVACY - Changelog

# Changelog

## v0.2.25 - Healing System & Action Economy (2025-11-26)
- **Summary:**
  - Implemented healing system with 2 heals per hero per room
  - Added action point system (heal costs 1 action, can follow with light attack)
  - Visual heart indicators show remaining heals
  - Fixed skip action and save game creation

- **Healing Mechanics:**
  - Each hero gets 2 heals per room (resets at battle start)
  - Heal restores 50% of max HP
  - Healing costs 1 action point
  - After healing, heavy and special attacks are disabled (1 action remaining)
  - Light attack, defend, swap, taunt, and skip remain available after heal
  - Visual heart display: ❤️ for available heals, ❌ for used heals

- **Action Economy:**
  - Heroes have 2 action points per turn
  - Heal uses 1 action point
  - Light attack uses 1 action point (can be used after heal)
  - Heavy and special attacks use 2 action points (disabled after heal)
  - All buttons re-enable at start of next turn

- **UI Improvements:**
  - Added heart icons to hero battle cards
  - Hearts update in real-time as heals are used
  - Disabled buttons are greyed out (50% opacity)
  - Skip button remains functional after healing

- **Bug Fixes:**
  - Fixed skip action not advancing turn
  - Fixed save game creation when no save exists
  - Save system now creates default save instead of showing error

- **Technical Changes:**
  - Added healsRemaining property to hero objects (initialized to 2)
  - Added usedHeal flag to track action state
  - Modified updateBattleHeroCards() to render heart icons
  - Modified advanceTurn() to reset button states
  - Added battleHeavyBtn and battleSpecialBtn IDs for state management
  - Modified saveGameFromPause() to create default save if none exists

## v0.2.24 - Combat UI Feedback Improvements (2025-11-26)
- **Summary:**
  - Added visual feedback for button clicks
  - Implemented enemy highlighting during targeting mode
  - Continuous animation loop for pulsing effects

- **Button Feedback:**
  - Added :active CSS state for click response
  - Scale down animation (0.95) on button press
  - Shadow change on click for tactile feedback
  - Immediate visual confirmation of user input

- **Enemy Targeting Highlights:**
  - Yellow pulsing border around hostile enemies in targeting mode
  - Glow shadow effect using ctx.shadowBlur
  - Pulse animation using sin wave (Date.now() / 200)
  - Only hostile enemies are highlighted as clickable targets
  - Non-hostile/friendly enemies remain unhighlighted

- **Hitbox Improvements:**
  - Accurate hitbox detection for mobs (1.75:1 aspect ratio)
  - Accurate hitbox detection for bosses (200x200 scaled)
  - Depth-scaled hit areas matching sprite sizes
  - Only hostile enemies respond to clicks

- **Animation System:**
  - Added battleAnimationLoop() using requestAnimationFrame
  - Continuous rendering while battleState.active is true
  - Enables smooth pulsing highlight effects
  - Automatic cleanup when battle ends

- **Technical Changes:**
  - Modified battleAction() to call renderBattle() when entering targeting mode
  - Updated handleBattleClick() to check enemy.hostile flag
  - Added pulsing highlight rendering in enemy drawing loop
  - CSS :active pseudo-class for button press feedback

## v0.2.23 - Combat System Implementation (2025-11-26)
- **Summary:**
  - Implemented full D&D-style turn-based combat system
  - Added initiative calculation using DEX modifiers
  - Integrated bosses_data.json and mobs_data.json for enemy loading
  - Implemented dice rolling mechanics (d20, d6) with visible results

- **Combat Mechanics:**
  - Initiative: DEX modifier + d20 roll determines turn order
  - Light Attack: 1d6 + DEX modifier damage
  - Heavy Attack: 2d6 + STR modifier damage
  - Special Attack: 3d6 + WIS modifier damage
  - Attack Roll: d20 + STR modifier vs target AC
  - Defend: 50% damage reduction, active until next turn

- **AI Behavior:**
  - Hostile enemies auto-attack random heroes
  - Non-hostile NPCs skip their turns
  - AI processes automatically with 1-second delay

- **Player Interaction:**
  - Click attack button to enter targeting mode
  - Click enemy sprite to execute attack
  - Crosshair cursor during targeting
  - Dice roll results displayed above action buttons

- **Data Integration:**
  - Load bosses from tunnelsofprivacy/bosses/bosses_data.json
  - Load mobs from tunnelsofprivacy/mobs/mobs_data.json
  - Mix boss + 2 random hostile mobs per encounter
  - Enemy stats (HP, AC, attackDamage, speed) loaded from JSON

- **Technical Changes:**
  - startBattle() now async to load JSON data
  - calculateModifier() function: (stat - 10) / 2
  - rollD20(), rollD6(count) dice functions
  - executeAttack() handles damage calculation and AC checks
  - processAITurn() handles enemy attacks
  - advanceTurn() manages turn order progression
  - handleBattleClick() for enemy targeting on canvas
  - Added diceRollDisplay element for combat feedback

- **UI Updates:**
  - Renamed battle buttons: WEAK ATTACK → LIGHT ATTACK, STRONG ATTACK → HEAVY ATTACK
  - Added dice roll display div with gold border and dark background
  - Targeting mode shows crosshair cursor

## v0.2.22 - Boss File Organization (2025-11-26)
- **Summary:**
  - Renamed all boss sprite files to match boss names from bosses_data.json
  - Updated all sprite paths to use individual level folders (lvl2-lvl21)
  - Organized boss assets into proper folder structure

- **Boss File Renaming:**
  - Level 2: boss_lvl2.png → metadata_swarm_mass.png
  - Level 3: boss_lvl3.png → open_ledger_golem.png
  - Level 4: boss_lvl4.png → leak_channel_imp.png
  - Level 5: boss_lvl5.png → trace_hound_construct.png
  - Level 6: boss_lvl6.png → clear_torch_sentinel.png
  - Level 7: boss_lvl7.png → echo_signal_wraith.png
  - Level 8: boss_lvl8.png → data_trail_collector.png
  - Level 9: boss_lvl9.png → scan_mask_idol.png
  - Level 10: boss_lvl10.png → unmasked_scribe_apparition.png
  - Level 11: boss_lvl11.png → watcher_eye_construct.png
  - Level 12: boss_lvl12.png → pattern_matcher_phantasm.png
  - Level 13: boss_lvl13.png → chain_analysis_serpent.png
  - Level 14: boss_lvl14.png → compliance_herald.png
  - Level 15: boss_lvl15.png → identity_probe_specter.png
  - Level 16: boss_lvl16.png → telemetry_spider.png
  - Level 17: envato-labs-image-edit.png → observer_node_golem.png
  - Level 18: boss_lvl18.png → cross_correlation_beast.png
  - Level 19: boss_lvl19.png → surveillance_lens_knight.png
  - Level 20: boss_lvl20.png → record_keeper_titan.png
  - Level 21: boss_lvl21.png → broken_entropy_shade.png

- **Sprite Path Updates:**
  - Changed from grouped folders (lvl1-10, lvl11-20, lvl21-30) to individual level folders
  - All paths now follow pattern: `tunnelsofprivacy/bosses/lvl{N}/{boss_name}.png`
  - Matches actual folder structure in filesystem

- **Technical Changes:**
  - Updated all 21 boss entries in bosses_data.json
  - Sprite paths now accurately reflect file locations
  - Boss names, files, and data now fully synchronized

## v0.2.21 - Boss Data Alignment (2025-11-26)
- **Summary:**
  - Fixed all boss names in bosses_data.json to match bosses_details.md exactly
  - Updated boss stats based on visual descriptions and level scaling
  - Corrected 18 boss entries (levels 4-21)

- **Boss Name Corrections:**
  - Level 4: Chain-Bound Horror → Leak-Channel Imp
  - Level 5: Address Reuse Wraith → Trace Hound Construct
  - Level 6: Dust Trail Demon → Clear-Torch Sentinel
  - Level 7: Transaction Graph Spider → Echo-Signal Wraith
  - Level 8: Heuristic Hunter → Data-Trail Collector
  - Level 9: Cluster Analysis Fiend → Scan-Mask Idol
  - Level 10: Fingerprint Leviathan → Unmasked Scribe Apparition
  - Level 11: Linkability Phantom → Watcher-Eye Construct
  - Level 12: Timing Correlation Beast → Pattern-Matcher Phantasm
  - Level 13: Deanonymizer Construct → Chain-Analysis Serpent
  - Level 14: Surveillance Eye Swarm → Compliance Herald
  - Level 15: zkProof Breaker → Identity-Probe Specter
  - Level 16: Shielded Transaction Knight → Telemetry Spider
  - Level 17: Note Plaintext Specter → Observer Node Golem
  - Level 18: Encrypted Memo Guardian → Cross-Correlation Beast
  - Level 19: Value Pool Hydra → Surveillance Lens Knight
  - Level 20: JoinSplit Amalgam → Record-Keeper Titan
  - Level 21: Commitment Scheme Titan → Broken Entropy Shade

- **Boss Stat Rebalancing:**
  - Small/fast bosses (imps, wraiths, specters): Lower HP, higher speed, lower AC
  - Heavy/armored bosses (golems, knights, titans): Higher HP, lower speed, higher AC
  - Mechanical constructs: Balanced stats with moderate AC
  - Serpents/beasts: High HP pools with moderate all-around stats
  - Stats now properly reflect visual descriptions from bosses_details.md

- **Technical Changes:**
  - All boss IDs updated to match new names (snake_case format)
  - Sprite paths updated to reference correct boss images
  - Maintained existing loot tables and special abilities
  - Preserved behavior flags and drop chances

## v0.2.20 - Mob System Implementation (2025-11-26)
- **Summary:**
  - Added 20 unique mobs with full stats, behaviors, and loot tables
  - Implemented multi-enemy battles (boss + 2 mobs)
  - Added proper mob rendering with correct aspect ratio and positioning
  - Created mobs_data.json for mob definitions
  - Fixed enemy visual styling (red names and HP bars)

- **Mob System:**
  - Created `tunnelsofprivacy/mobs/mobs_data.json` with 20 mob definitions:
    - beetles, blobs, creatures, gnawers, goblins, insects, mites, moths, orbs, rats, spiders, worms
  - Each mob includes: hp, attackDamage, ac, speed, experience
  - Behavior flags: hostile, friendly, canChat, fleeThreshold
  - Loot tables with drop chances and item varieties
  - Special abilities with cooldowns
  - Dialogue for chattable/friendly mobs

- **Multi-Enemy Battles:**
  - Updated platform detection to support 7 platforms (4 heroes + 3 enemies)
  - Boss + 2 mobs spawn in test battles
  - Each enemy positioned on separate platform with spatial separation
  - Fallback layout supports multiple enemies

- **Mob Rendering:**
  - Mobs use 1344x768 sprite dimensions (aspect ratio 1.75:1)
  - Rendered at 4x smaller scale than original (base height ~75px)
  - Feet positioned at ground level (enemy.y = feet position)
  - Hitboxes match sprite dimensions and aspect ratio
  - Depth scaling applies to both sprite and hitbox

- **Enemy Visual Styling:**
  - Enemy names displayed in RED (#FF4444)
  - Enemy HP bars use RED gradient:
    - Healthy (>50%): #E74C3C
    - Medium (25-50%): #C0392B
    - Low (<25%): #A93226
  - HP text remains white for readability
  - Name and HP bar positioned above sprite for both mobs and bosses

- **Mob vs Boss Rendering:**
  - `isMob` flag differentiates rendering logic:
    - Mobs: 1344x768 aspect ratio, feet at enemy.y, smaller scale
    - Bosses: 300x300 square, centered on enemy.y, standard scale
  - Hitboxes adapt to entity type:
    - Mobs: rectangle matching sprite aspect ratio from feet upward
    - Bosses: square centered on position
  - Floor contact point (magenta dot) shows at feet for mobs, bottom of hitbox for bosses

- **Platform Positioning:**
  - Mobs positioned with feet directly at platform center Y
  - Bosses use iterative solver for floor contact at platform center Y
  - All enemies use correct depth scaling

- **Technical Changes:**
  - `generateBattleLayout()` now selects 7 platforms and positions 3 enemies
  - `generateFallbackLayout()` supports multiple enemy positions
  - Enemy sprite rendering checks `isMob` flag for dimension calculations
  - HP bar positioning calculates sprite height to place bars above
  - Hitbox debug rendering adapts to mob vs boss sizing

## v0.2.19 - Depth-Based Rendering & Platform Positioning (2025-11-26)
- **Summary:**
  - Added depth-based scaling for characters based on Y position
  - Fixed platform positioning to place characters at detection box centers
  - Added per-character sprite offset adjustments
  - Implemented depth test for better platform validation
  - Fixed cache clearing to force fresh asset reload

- **Depth-Based Rendering:**
  - Characters scale from 0.6x (top/far) to 1.0x (bottom/near)
  - Scale calculation: `0.6 + (y / canvas.height) * 0.4`
  - Affects sprites, hitboxes, HP bars, and text
  - Creates proper perspective in battle scenes

- **Platform Positioning:**
  - Characters positioned so floor contact point is at detection box center
  - Iterative solver accounts for depth-based hitbox scaling
  - Floor contact point = `character.y + (scaledHitboxSize / 2)`
  - Ensures consistent positioning across all backgrounds

- **Sprite Offsets:**
  - Per-character vertical offset adjustments:
    - Zooko: 10px down
    - Nate: 10px down
    - Zancas: 20px down
    - CyberAxe: 13px down
  - Offsets align character feet with hitbox floor contact

- **Depth Test Validation:**
  - `calculateDepthScore()` traces downward from platforms
  - Measures distance to ground (max 200px trace)
  - Rejects floating platforms (score < 0.5)
  - Scores platforms: 1.0 at ground, 0.5 at 50px+ height
  - Validates continuous support path

- **Cache & Asset Loading:**
  - Clear cache now deletes browser caches via Caches API
  - Forces hard reload with `location.reload(true)`
  - Hero sprites load with timestamp parameter to bypass cache
  - Ensures updated images appear immediately

- **Debug Visualization:**
  - Hitboxes now scale with depth (matching sprite scale)
  - Floor contact point shown as large magenta dot with white outline
  - Center point shown as smaller green/red dot
  - Platform detection boxes remain visible for debugging

- **Technical Changes:**
  - `generateBattleLayout()` uses iterative Y position solver
  - `renderBattle()` calculates `depthScale` for all character elements
  - `clearCache()` clears both localStorage and browser caches
  - All 3 detection methods (`detectByAdaptiveThreshold`, `detectByMultiAngle`, `detectByColorClustering`) now use depth scoring

## v0.2.18 - Spawn Randomization & Background Filtering (2025-11-25)
- **Summary:**
  - Added spawn point randomization for battle variety
  - Removed problematic backgrounds from rotation
  - Each battle now uses different platform combinations

- **Spawn Randomization:**
  - Shuffles detected platforms before selection
  - Different hero/enemy positions each battle
  - Uses `Math.random()` to randomize platform order
  - Maintains spatial separation checks on randomized set

- **Background Updates:**
  - Reduced from 12 to 7 backgrounds in lvl1-10 pool
  - Removed backgrounds with poor platform detection:
    - backgrounds_lvl1 (1, 2, 3, 5, 6, 7, 9, 11, 13, 17, 18, 19)
  - Kept only backgrounds with reliable platform detection:
    - backgrounds_lvl1 (4, 8, 10, 12, 14, 15, 16)

- **Technical Changes:**
  - `generateBattleLayout()` now creates shuffled copy of safe platforms
  - Random sort applied before spatial separation loop
  - Background options array updated to exclude problematic files

## v0.2.17 - Platform Detection Fix (2025-11-25)
- **Summary:**
  - Fixed platform detection system to use discrete box scanning instead of continuous spans
  - Added spatial separation checking to prevent overlapping hero/enemy spawns
  - Added ground verification to prevent floating platform detection
  - Complete rewrite of detection algorithms for better accuracy

- **Platform Detection Fixes:**
  - **Box-Based Scanning:**
    - Changed from 3px line scans to 150x50px box scans
    - Scans discrete boxes instead of continuous horizontal spans
    - Each box independently evaluated for platform viability
    - Prevents detecting long sky/cloud areas as platforms
  
  - **Ground Verification:**
    - Checks 5px below each detected box for darker area
    - Platform must be 20+ brightness units brighter than area below
    - Exception for boxes at bottom edge of image
    - Eliminates floating platform false positives
  
  - **Spatial Separation:**
    - Added minimum 200px distance check between selected platforms
    - Prevents overlapping hero/enemy spawns (300x300px sprites)
    - Iterates through detected platforms to find non-overlapping set
    - Falls back to manual positioning if insufficient platforms found

- **Detection Method Updates:**
  - **Adaptive Threshold:**
    - Box dimensions: 150x50px
    - Step size: 50px horizontal, 25px vertical
    - Scans bottom 60% of image
    - Samples entire box area (every 5px) for brightness
  
  - **Multi-Angle Detection:**
    - Same box dimensions as adaptive
    - Tests 0°, 5°, -5° angles for sloped platforms
    - Step size: 50px horizontal, 30px vertical
    - Ground verification on all detected boxes
  
  - **Color Clustering:**
    - Analyzes 150x50px boxes for color consistency
    - Averages RGB across entire box
    - Step size: 50px horizontal, 25px vertical
    - Ground verification required for all detections

- **Technical Implementation:**
  - `detectByAdaptiveThreshold()` - Complete rewrite with box scanning
  - `detectByMultiAngle()` - Complete rewrite with box scanning
  - `detectByColorClustering()` - Complete rewrite with box scanning
  - `generateBattleLayout()` - Added spatial separation loop
  - Console logging for debugging platform counts

- **Benefits:**
  - No more full-width platform spans that cause overlaps
  - Discrete platform detection matches actual floor regions
  - Ground verification eliminates sky/cloud false positives
  - Spatial checks ensure heroes/enemies spawn in separate locations
  - More reliable platform detection across different backgrounds

## v0.2.11 - Dungeon Menu Screen (2025-11-25)
- **Summary:**
  - Added dungeon menu screen for room-based navigation
  - Hero cards repositioned to four corners
  - New center menu with dungeon options
  - Music controls and ticker now persist across all screens

- **Dungeon Menu Screen:**
  - Click "START ADVENTURE" switches from title to dungeon menu
  - Separate screen state (title screen hidden, dungeon menu shown)
  - Solid background gradient (no animation)
  - Hero cards in corners:
    - Zooko: Top Left
    - Nate: Bottom Left
    - Zancas: Top Right
    - CyberAxe: Bottom Right
  - Same hero card styling as title screen
  - Stats sync between both screens

- **Center Menu Buttons:**
  - **EXPLORER LEVEL** - Enter dungeon exploration (not implemented yet)
  - **ENTER LEVEL STORE** - Shop system (disabled, coming soon)
  - **INVENTORY** - View/manage items (not implemented yet)
  - **REST / SLEEP** - Restore HP/resources (not implemented yet)
  - All buttons styled matching arcade game aesthetic
  - Level display at top of menu

- **Music System Fix:**
  - Moved music controls outside titleScreen container
  - Moved ticker outside titleScreen container
  - Changed from `position: absolute` to `position: fixed`
  - Increased z-index to 500 for proper layering
  - Now visible on both title screen and dungeon menu

- **Technical Implementation:**
  - New `#dungeonMenuScreen` container
  - `.dungeonHeroCard` class for corner positioning
  - `startAdventure()` function switches screens
  - Hero stats use `d` prefix for dungeon screen (e.g., `dzooko-hp`)
  - `updateHeroDisplay()` now updates both title and dungeon screens
  - Dungeon level syncs from arcade save state

- **Next Steps:**
  - Implement pause menu (ESC key)
  - Add functionality to each dungeon menu button
  - Create room-based exploration system

## v0.2.10 - Complete Standardization with Arcade (2025-11-25)
- **Summary:**
  - Complete overhaul to match arcade game systems exactly
  - Added ticker facts educational system
  - Fixed all non-standard naming and structures
  - Full feature parity with arcade's music/ticker system

- **Ticker Facts System (NEW):**
  - Loads `ticker_facts.json` with Zcash/crypto educational facts
  - Displays random fact alongside music info
  - Format: `♫ Theme Song: [name] ♫ • [Random Fact]`
  - Picks new random fact every time track changes
  - Educational content while players browse menu
  - Same ticker facts pool as arcade game

- **Ticker Structure Fixes:**
  - Fixed HTML structure: `#musicTicker` > `#musicTickerWrapper` > `.tickerText` spans
  - Was reversed (wrapper > ticker), now matches arcade exactly
  - Added hover slow-down effect (30s → 60s on hover)
  - Added `pointer-events: auto` to enable hover despite parent blocking
  - Changed animation name from `scroll-left` to `scrollTicker` (arcade standard)
  - Proper seamless scrolling with two identical spans

- **Naming Standardization:**
  - Renamed `dungeonMusicTracks` → `themeTracks` (arcade standard)
  - Renamed `loadDungeonMusic()` → `loadMusic()` (arcade standard)
  - Updated all 6 references to use standard naming
  - Ticker text: "Dungeon Music" → "Theme Song" (arcade standard)
  - Consistent variable/function names across both games

- **Technical Implementation:**
  - Added `tickerFacts` array and `currentTickerFact` variable
  - Fetch `ticker_facts.json` on page load
  - `loadMusic()` picks new random fact from array
  - Combines music info + fact with ` • ` separator
  - Falls back to music-only if facts not loaded
  - Logs fact count to console for debugging

- **Benefits:**
  - Educational: Players learn about Zcash/privacy while browsing
  - Consistency: Same ticker behavior as arcade
  - Engagement: Dynamic content changes with each track
  - Polish: Hover interaction for readability
  - Maintainability: Identical code structure to arcade

## v0.2.9 - Loading Screen & Music Fix (2025-11-25)
- **Summary:**
  - Added complete loading screen system matching arcade
  - Fixed music autoplay to only start from loading screen button
  - Removed title/subtitle text (already in animated background)
  - Complete standalone preload system

- **Loading Screen:**
  - Full modal with progress bar and percentage display
  - Category breakdown: Art (5 images), Sound (optional music)
  - Purple/dungeon theme matching game aesthetic
  - "🎮 CLICK TO ENTER 🎮" prompt when ready
  - Fades out smoothly after user clicks
  - Preloads all assets before allowing play

- **Music System Fix:**
  - Removed global click/keydown event listeners that started music anywhere
  - Music now ONLY starts when clicking loading screen button
  - Respects browser autoplay policies properly
  - No more unwanted music playback on random clicks

- **Visual Polish:**
  - Hidden duplicate title text ("TUNNELS OF PRIVACY" and subtitle)
  - Animated background shows title, no need for overlay text
  - Cleaner title screen presentation

- **Technical Details:**
  - Asset tracking: `assetsToLoad`, `assetsLoaded`, `artTotal`, `artLoaded`, `audioTotal`, `audioLoaded`
  - Progress updates via `updateLoadingProgress()`
  - `checkAllAssetsReady()` shows click prompt when complete
  - Music timeout (3 seconds) prevents hanging on music load
  - Uses `loadedmetadata` event instead of `canplaythrough`

## v0.2.8 - Unified Save System (2025-11-25)
- **Summary:**
  - Load Save File now accepts shared save format from arcade
  - Complete compatibility with arcade save file downloads
  - Added `createDefaultSharedSave()` function for fallback initialization
  - Single unified save format across both games

- **Save File System:**
  - **Load Save File** validates for heroes property (shared save format)
  - Works with save files downloaded from arcade game
  - Supports complete save data: heroes, arcade state, dungeon state
  - Updates hero displays from loaded data
  - Updates dungeon level from arcade state

- **Technical Details:**
  - Added `createDefaultSharedSave()` with default hero stats
  - Matches arcade's hero initialization (str, dex, con, int, wis, cha, hp, maxHp, ac, xp, level)
  - Default heroes: Zooko, Nate, Zancas, CyberAxe
  - Save format includes saveVersion, lastPlayed, arcadeState, dungeonState, heroes

## v0.2.7 - Load Save File Feature (2025-11-25)
- **Summary:**
  - Added Load Save File option to main menu
  - File input panel for uploading save files
  - Validates and imports save data to localStorage

## v0.2.6 - Animated Background & UI Polish (2025-11-25)
- **Summary:**
  - Added animated background matching arcade game
  - Improved menu button layout
  - Enhanced Exit Portal button formatting
  - Complete visual consistency with arcade game

- **Visual Enhancements:**
  - **Animated Background**:
    - Added story intro background animation system
    - Uses same `story/intro/intro_a.png` sprite sheet as arcade (8x16 atlas, 128 frames)
    - 16fps ping-pong animation (forward then backward loop)
    - 30% opacity for subtle atmospheric effect
    - Positioned behind all UI elements (z-index: -1)
    - Starts automatically on page load
  
  - **Menu Button Improvements**:
    - Changed button text alignment from `space-between` to `center`
    - Button labels now properly centered
    - Icons positioned correctly with margins
    - Improved visual balance
  
  - **Exit Portal Button**:
    - Split text into two lines: "EXIT PORTAL" and "(Return to Arcade)"
    - Second line uses smaller font (10px) and lighter weight
    - Better readability and visual hierarchy
    - Maintains centered alignment

- **Technical Implementation:**
  - **Background Animation Functions**:
    - `startStoryIntroAnimation()` - Initializes and runs sprite sheet animation
    - `stopStoryIntroAnimation()` - Cleans up animation interval
    - Calculates frame position in 8-column x 16-row atlas
    - Updates background position every ~62.5ms
    - Ping-pong direction reversal at boundaries (0 and 127)
  
  - **CSS Additions**:
    - `#storyIntroBackground` div with full-screen positioning
    - Background-size calculated from atlas dimensions
    - Smooth 2s opacity transition
    - Proper layering behind title screen

- **Integration:**
  - Animation starts in `init()` function after settings load
  - Shares same sprite sheet asset with arcade game
  - Consistent visual theming across both games
  - Adds atmospheric depth to title screen

---

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

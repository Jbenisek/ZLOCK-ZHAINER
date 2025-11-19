# ZLOCK CHAINER - Changelog

# Changelog

## v0.19.45 - Special Abilities UI Improvements (2025-11-18)
- **Summary:**
  - Enhanced special abilities panel with improved typography and controller support
  - Moved High Scores close button to top for consistency

- **Special Abilities UI Enhancements:**
  - Character names now bold (font-weight: 900) and larger (15px)
  - Keyboard hints larger (12px) and bolder (font-weight: 700)
  - Added D-pad controller button icons to all special abilities:
    - Zooko: D-pad UP ▲ (key 1)
    - Nate: D-pad DOWN ▼ (key 2)
    - Zancas: D-pad LEFT ◀ (key 3)
    - CyberAxe: D-pad RIGHT ▶ (key 4)

- **UI Improvements:**
  - High Scores panel close button moved to top of panel

## v0.19.44 - Hint Popup Controller Icons (2025-11-18)
- **Summary:**
  - Added controller button icons to all hint popup buttons
  - Added gamepad support for hint popups (A to close, Y to skip all)

- **Gamepad UI Enhancements:**
  - Green A button icon on all "GOT IT!" buttons
  - Yellow Y button icon on all "SKIP ALL" buttons
  - A button now closes current hint popup
  - Y button skips all remaining hints

## v0.19.43 - Gamepad Support & Server Improvements (2025-11-18)
- **Summary:**
  - Added full Xbox/Steam/generic controller support
  - Fixed server stop command to properly kill Python processes
  - Added "Skip All" button to hint popups
  - Fixed gamepad analog stick interfering with keyboard input
  - Added controller A button to close hint popups

- **Gamepad/Controller Support:**
  - Full support for Xbox, PlayStation, Steam Controller, and generic gamepads
  - Standard Gamepad API mapping with 60Hz polling
  - Left analog stick: Move chain (WASD equivalent)
  - A button: Drop/Fast drop (double-tap for instant drop)
  - B button: Rotate piece
  - Y button: Flip chain
  - LB/RB: Rotate camera left/right
  - D-Pad: Character special abilities (Up=Zooko, Down=Nate, Left=Zancas, Right=CyberAxe)
  - Start: Pause/Resume
  - Select: Toggle top-down view
  - Automatic detection with on-screen notifications
  - Analog stick deadzone prevents interference with keyboard

- **UI Improvements:**
  - Added "Skip All" button to all hint popups (Level 10, 20, 50, Glowing Links Guide)
  - Skip All marks all hints as seen and closes current popup
  - A button on gamepad now closes visible hints before performing gameplay actions
  - Added "1-4" keyboard hint for special abilities to HUD instructions
  - Reduced hint button font size to 14px for better single-line fit

- **Server Script Fix:**
  - `zlock_server.sh stop` command now properly terminates Python server
  - Added graceful shutdown (SIGTERM) followed by force kill (SIGKILL) if needed
  - Uses `lsof` to detect and clean up processes still using port 4243
  - Handles cases where PID file is missing but server is still running
  - Provides helpful status messages during shutdown process

- **Bug Fixes:**
  - Fixed gamepad analog stick resetting WASD keys every frame
  - Keyboard input now works reliably alongside gamepad support
  - Analog stick only overrides keyboard when actively moved beyond deadzone

## v0.19.42 - Linux GLB Binary Serving Fix (2025-11-18)
- **Summary:**
  - Fixed critical GLB model loading issue on Linux Mint servers
  - Created custom Python HTTP server with proper binary MIME types
  - Resolved "Invalid typed array length" errors in GLTFLoader

- **Server Implementation:**
  - Created `zlock_server.py` - Custom HTTP server with binary file support
  - Explicitly sets `model/gltf-binary` MIME type for `.glb` files
  - Added CORS headers for proper cross-origin asset loading
  - Disabled caching for development workflow
  - Proper binary file handling prevents data corruption

- **Bug Fix:**
  - **Issue:** GLB files loaded fine on Windows but failed on Linux Mint with `RangeError: Invalid typed array length`
  - **Root Cause:** Python's default `http.server` served GLB files with incorrect MIME type on Linux
  - **Solution:** Custom server forces correct binary MIME types, preventing browser misinterpretation
  - Models now load identically on Windows and Linux platforms

- **Updated:**
  - `zlock_server.sh` now launches `zlock_server.py` instead of basic http.server
  - Added support for audio MIME types (.mp3, .wav, .ogg)
  - Added support for image MIME types (.png, .jpg, .jpeg)

## v0.19.41 - Linux Hosting Compatibility Fix
- **Summary:**
  - Fixed case-sensitive file path for QR code image (Linux compatibility)
  - Reverted Zooko model path after testing

- **File Path Fixes:**
  - QR code image: `CyberAxeZcashWalletQR.png` → `CyberAxeZcashWalletQR.PNG`
  - Fixed 404 error on Linux servers (case-sensitive filesystems)
  - Zooko model: Tested `zooko_b.glb` for GLB loading issues, reverted to `zooko_a.glb`

- **Web Hosting:**
  - Created `zlock_server.sh` bash script for easy server start/stop on Linux
  - Port: 4243 with public access (0.0.0.0 binding)
  - Includes firewall configuration, PID management, and status checking

## v0.19.40 - UI Compacting & Color Picker Positioning
- **Summary:**
  - Compacted theme settings panel (gameControls) to reduce screen space usage
  - Made all control buttons smaller and tighter
  - Reduced color picker modal size for better usability
  - Fixed color picker modal to appear directly above its button instead of screen center

- **Theme Settings Panel Compacting:**
  - Panel padding: 8px → 4px
  - Border radius: 12px → 8px
  - Button gap: 8px → 4px
  - Overall panel footprint reduced by ~35%

- **Control Buttons (💡✨💠🧍🎬🎨) Reduction:**
  - Button size: 45×45px → 32×32px (29% smaller)
  - Button padding: 10px 14px → 6px 8px
  - Font size: 20px → 16px
  - Border radius: 8px → 6px
  - More compact appearance while maintaining usability

- **Color Picker Modal Optimization:**
  - Modal padding: 20px → 12px
  - Modal min-width: 320px → 280px
  - Border radius: 10px → 8px
  - Title font: 14px → 12px
  - Label font: 12px → 11px
  - Color input size: 60×40px → 50×32px
  - Button gaps: 10px → 8px
  - "None" button font: 11px → 10px, padding: 8px → 6px
  - Accept/Cancel button padding: 10px → 7px
  - All margins reduced throughout
  - Overall modal size reduced by ~25%

- **Color Picker Positioning Fix:**
  - Changed from fixed center-screen position to dynamic positioning
  - Modal now uses `position: fixed` with button's getBoundingClientRect()
  - Calculates position to appear directly above the 🎨 button
  - Uses `transform: translateX(-50%)` to center modal over button
  - Bottom offset calculated from window height minus button top position
  - Improves UX by keeping modal near related control

## v0.19.39 - COMPREHENSIVE Memory Leak Elimination
- **Summary:**
  - Fixed all major memory leaks causing 1125MB usage after 12 hours (expected: 150MB)
  - Eliminated ~23.4 million orphaned THREE.js objects created overnight
  - Achieved zero object allocation in all hot loops (60 FPS particle updates)
  - Memory usage now stable at ~150MB during extended gameplay sessions

- **Critical Fixes - Hot Loop Leaks (60 FPS):**
  - **Particle Update Loop:** Color.clone().lerp() created new Color object every frame per particle
    - Fixed: Use .copy().lerp() to modify material color in place
    - Impact: Eliminated thousands of Color objects created per second
  
  - **Bone Tracking Update:** Created 3 new Vector3/Quaternion objects per frame per effect
    - 60 FPS × 3 effects × 3 objects = 540 allocations/second
    - 12 hours = 23.3 million leaked objects
    - Fixed: Created 6 reusable objects at module scope (_boneTempWorldPos, _boneTempOffsetVec, etc.)
    - Impact: Zero allocations in particle position tracking

- **Major Fixes - Particle System:**
  - **Bone-Tracked Spawn Loops:** Vector3 created every 1.1 seconds (Zooko shield/hat, CyberAxe chest)
    - 3 loops running continuously = 117,819 Vector3 objects over 12 hours
    - Fixed: Reuse _boneTempHeadPos for all bone position queries
  
  - **Camera-Relative Spawning:** 3 new Vector3 objects per particle spawn
    - Fixed: Created _spawnTempCamDir and _spawnTempSpawnPos reusable objects
  
  - **Special Animation Hand Tracking:** 4 Vector3 per special (Zancas/CyberAxe hands)
    - Fixed: All hand tracking now uses shared _boneTempHeadPos

- **Code Quality Fixes:**
  - Removed 2 duplicate spawnZookoHeadShield() functions (3 copies existed)
  - Functions were causing 3× particle spawn rate and additional leaks

- **Memory Cleanup Fixes:**
  - Particle textures: Now dispose texture.map before material disposal
  - stopParticleEffect(): Full cleanup of textures, materials, geometries
  - Chain column rebuild: Proper disposal of link/arrow geometries and materials

- **Reusable Objects Added:**
  ```javascript
  _boneTempWorldPos       // Bone world position
  _boneTempOffsetVec      // Bone offset vector
  _boneTempWorldQuat      // Bone world quaternion
  _boneTempHeadPos        // General bone position queries
  _spawnTempCamDir        // Camera direction for spawning
  _spawnTempSpawnPos      // Calculated spawn position
  ```

- **Performance Metrics:**
  - Before: 1125MB after 12 hours, ~23.4M leaked objects
  - After: ~150MB stable, zero object allocation in hot loops
  - Particle count display added to performance monitor (FPS/Memory/Particles)

## v0.19.35 - Performance Monitoring & Memory Leak Fixes
- **Performance Display:**
  - Added particle count to performance display window (FPS, Memory, Particles)
  - Particle count updates every second showing total active particles across all effects
  - Helps monitor particle system performance and memory usage

- **Memory Leak Fixes:**
  - Fixed particle texture memory leak: cloned textures now properly disposed when particles die
  - Fixed stopParticleEffect() memory leak: now disposes textures, materials, and geometries
  - Fixed chain column rebuild memory leak: chain link geometries and materials now disposed
  - Fixed chain column arrow memory leak: arrow geometries and materials now disposed
  - All particle cleanup now properly disposes texture.map before disposing materials
  - Prevents GPU memory accumulation during long gameplay sessions

- **Particle Placement Updates:**
  - Changed particle placement id 2 effect from cyberaxe_electric_walls_spark to cyberaxe_electric_walls

## v0.19.34 - Zooko Head Particle Effects
- **Visual Effects:**
  - Added looping shield particle effect to Zooko's head during idle animation (zooko_shield.json)
  - Added looping hat particle effect to Zooko's head during idle animation (zooko_hat.json)
  - Both effects track Zooko's head bone with independent adjustable offsets
  - zookoHeadOffset: controls shield particle position relative to head bone
  - zookoHatOffset: controls hat particle position relative to head bone
  - Effects loop seamlessly at emitDuration interval (1.1s)

- **Technical Changes:**
  - Added zookoHeadBone variable and head bone detection (searches for "head" in bone names)
  - Added zookoHeadOffset and zookoHatOffset variables for independent positioning
  - spawnZookoHeadShield() and spawnZookoHat() functions for looping particle effects
  - Both effects added to particle preload list
  - Bone rotation applied to particle offsets for accurate tracking

## v0.19.33 - Particle System Cleanup
- **Visual Changes:**
  - Removed CyberAxe special laser particle effects (cyberaxe_special_laser_a/b/c)
  - Simplified laser blast visual to purple tube and yellow particles only

## v0.19.32 - CyberAxe Special Chain Wait Fix
- **Bug Fix:**
  - Fixed CyberAxe special aborting if no chain exists when activated
  - Special now waits for chain to spawn instead of canceling
  - Prevents players from losing special charge during brief chainless moments
  - Checks for chain every 50ms until one spawns, then executes special
  - Split triggerCyberAxeSpecialEffect() into wait logic and executeCyberAxeSpecial()

## v0.19.31 - Particle Rotation System
- **Particle Rotation System:**
  - Implemented spawnRotation: initial rotation angle in degrees (from particle editor)
  - Implemented randomRotation: randomizes each particle's initial rotation (0-360°)
  - Implemented randomRotationSpeed: randomizes rotation speed per particle
  - Particles now rotate correctly using individual rotationSpeed values
  - Rotation system matches particle editor functionality (parity fix)
  - Non-sprite particles apply rotation to mesh.rotation.z

- **Technical Changes:**
  - createEffectParticle() now calculates and stores individual particle rotation/rotationSpeed
  - updateParticleEffects() applies rotation using particle.rotation += particle.rotationSpeed
  - Particle data structure expanded: rotation, rotationSpeed properties per particle

## v0.19.30 - CyberAxe Shield Particle Effect
- **Visual Effects:**
  - Added looping shield particle effect to CyberAxe's chest during idle animation
  - Shield effect uses cyberaxe_shield.json particle configuration
  - Chest bone tracking with adjustable offset (cyberAxeChestOffset)
  - Bone rotation properly applied to particle offset for accurate positioning
  - Effect loops seamlessly at emitDuration interval (1.1s)
  - Particles remain visible while new ones spawn (overlapping effect)

- **Technical Changes:**
  - Added cyberAxeChestBone and cyberAxeChestOffset variables
  - Chest bone detection: searches for "spine1" in bone names
  - Particle effect offset now rotates with bone quaternion
  - Fixed bone-attached particle effects to respect bone rotation

## v0.19.29 - Chain Column Management System
- **Chain Column Management:**
  - Added interactive management UI for decorative chain columns (orange boxes and arrows when hitboxes enabled)
  - Click column box to open compact menu with all properties
  - Click arrows to move columns by 2 units in any direction
  - Editable properties: position (x, y, z), rotation, chain length, color mode, single color, direction (up/down), enabled
  - Duplicate button creates copy offset by +2 on x-axis
  - Delete button removes column completely from scene
  - Copy Data button exports column settings as JSON to clipboard
  - Real-time rebuilding when properties change
  - Direction property: chains can scroll up or down
  - Chain animations respect effects bar animation toggle (🎬 button)

## v0.19.28 - Decorative Chain Column Templates
- **Chain Column System:**
  - Created template system for decorative chain columns around the room
  - Template properties: position (x, y, z), rotation, colorMode, singleColor, chainLength, enabled
  - Color modes: 'single' (one color) or 'random' (random per link)
  - chainLength modifier: negative values = shorter columns, positive = taller
  - Y position controls starting height of chain links
  - Enable/disable individual columns without removing from template array
  - 5 default columns: 4 corners + 1 custom red column demonstration

## v0.19.27 - Grid Color Customization
- **UI Enhancements:**
  - Added grid color picker button (🎨) to game controls (replaced unused button)
  - Color picker modal for customizing laser line and floor hint colors
  - Option to disable laser lines or floor hints entirely with "None" button
  - Toggle "None" buttons on/off to re-enable color selection
  - Accept/Cancel buttons for applying or discarding color changes
  - Custom colors persist during gameplay session
  - Default colors remain cyan (#00FFFF) for both elements

## v0.19.26 - Drop Effect Particle System
- **Visual Effects:**
  - Added drop effect particles that spawn while chains are falling
  - Color-coded drop effects for each chain type (yellow, blue, green, red)
  - Drop effects spawn every 1/4 second at the bottom of the falling chain
  - Added particle effects: drop_effect_yellow.json, drop_effect_blue.json, drop_effect_green.json, drop_effect_red.json
  - Multi-type chains use the color of their first link for drop effects

## v0.19.25 - Particle Placement Updates
- **Particle System:**
  - Added copy data button to particle placement menu (similar to model placement)
  - Added new particle effects: cyberaxe_electric_walls_red.json, cyberaxe_electric_walls_yellow.json, cyberaxe_electric_walls_spark.json
  - Updated particle placements with new effects and positions
  - Copy button exports particle placement data in JSON format to clipboard

## v0.19.24 - Particle Editor Compact Layout
- **Particle Editor Updates:**
  - See PARTICLE_EDITOR_CHANGELOG.md v0.19.7 for detailed changes
  - Reorganized editor panel with 2-column and 3-column grid layouts
  - Grouped related controls for intuitive layout (Size Start/End, Opacity Start/End, etc.)
  - Reduced font sizes, input widths, and margins for compact display
  - Prepared layout for future expansion with additional particle options

## v0.19.23 - Particle Editor UI Improvements
- **Particle Editor Updates:**
  - See PARTICLE_EDITOR_CHANGELOG.md v0.19.6 for detailed particle editor improvements
  - Compact template list design with single-line items
  - Sort functionality for templates (Name A-Z or Last Updated)
  - Grid defaults to 6x6 for sprite sheet textures
  - Toast notifications instead of popup alerts
  - Improved button layout and spacing

## v0.19.22 - Particle Loop System Fix
- **Particle Looping Improvements:**
  - Fixed particle loop timing to use emitter duration only (not emitter + particle lifetime)
  - Particle effects now loop seamlessly at emitDuration boundary
  - New particles can spawn while previous particles are still alive and fading
  - Enables seamless continuous particle effects without gaps
  - Fixes issue where loops waited for all particles to die before restarting

- **Technical Changes:**
  - Updated `startLoopingParticle()` to use only `emitDuration` for loop interval
  - Removed `particleLifetime` from loop duration calculation
  - Both game and particle editor now use consistent loop timing

## v0.19.21 - Particle System Improvements
- **Particle Editor Updates:**
  - Replaced misc1_effects.png with new atlas files (atlas_a.png through atlas_g.png)
  - Added 7 new texture atlas options in particle editor dropdown
  - Fixed atlas preview display - image now correctly flips vertically to match Three.js texture coordinates
  - Canvas preview now shows sprites exactly as they appear in-game
  - Click coordinates work correctly with flipped preview

- **Particle System:**
  - Particle system automatically loads new atlas textures from JSON configurations
  - Support for atlas_a.png through atlas_g.png texture atlases
  - Dynamic texture loading system supports any atlas path specified in effect files

## v0.19.20 - Model Position Refinements
- **Model Position Adjustments:**
  - Female_1_idle: y -8.5 → -8.25 (refined floor alignment after shadow implementation)
  - Male_2_sitting_idle: z -29 → -28 (improved scene placement)
  - Fine-tuned model positions for better visual consistency with shadow system

- **Development Tools:**
  - Created chain_render.html: Standalone chain renderer for AI asset generation
  - Added 6x6 sprite sheet view with all link colors and rotations
  - Includes single chain view with adjustable length and spacing
  - Toggle grid, adjustable camera, background colors, and screenshot export
  - Sprite sheet displays all link types at 0° and 90° rotations for reference

## v0.19.19 - Game Controls Enhancement
- **New Toggle Buttons:**
  - Added 3D Models toggle button (🧍/❌) to show/hide all model placements
  - Added Animations toggle button (🎬/❌) to enable/disable all character and model animations
  - Both buttons start enabled with proper active state styling
  - Animations freeze at current frame when disabled for performance optimization

- **Model Position Adjustments:**
  - Female_1_idle: y -7 → -8.5
  - Female_3_idle: y -7 → -8.25
  - Female_4_idle: y -7 → -8.25
  - Alien_male_1_idle: y -7 → -9
  - Fine-tuned model heights for better floor alignment and visual consistency

## v0.19.18 - Performance & Visual Improvements
- **View Change Performance:**
  - Disabled frustum culling for all character models (Zooko, CyberAxe, Zancas, Nate)
  - Eliminated hitching when switching between camera views
  - Models now stay cached in GPU memory and render pipeline
  - Prevents shader recompilation and render list rebuilding on view changes

- **Shadow System Implementation:**
  - Enabled shadow mapping in renderer with soft shadows (PCFSoftShadowMap)
  - Configured shadow camera coverage for entire play area (-40 to +40 units)
  - Extended shadow far plane from 50 to 100 units
  - Added shadow bias to reduce artifacts
  - Floor now receives shadows from all models and characters
  - Characters, table, and chain links cast realistic soft shadows

- **Model Adjustments:**
  - Adjusted female_1_idle model position (y: -7 → -8.5)
  - Fine-tuned CyberAxe model position for better scene placement

## v0.19.17 - Audio System Removal & UI Polish
- **Complete Audio System Removal:**
  - Removed entire generative music system (~850 lines)
  - Removed all CSS music control styles (55 lines)
  - Removed music control panel and settings UI elements
  - Removed Web Audio API implementation (oscillators, filters, reverb, compression)
  - Removed all music functions: bassline, drums, synth pads, victory songs
  - Removed all sound effect functions: link notes, floor hits, collisions
  - Removed music state tracking: intensity, tempo, hyper mode
  - Game now runs silently without any audio dependencies

- **Game Controls UI Improvements:**
  - Redesigned game control buttons bar with modern gradient styling
  - Added active state highlighting for toggle buttons (lights, particles, wall emissive)
  - Improved hover effects with teal glow and lift animation
  - Enhanced button spacing and consistent sizing
  - Grayed out and disabled 3 unused placeholder buttons
  - Added smooth transitions and shadow effects
  - Updated color scheme to match game aesthetic (teal #2A9D8F, gold #F2C94C)

## v0.19.16 - Critical Bug Fixes
- **Special Effects Environment Reset:**
  - Added default light intensity constants (keyLight: 1.2, fillLight: 0.6, ambientLight: 0.3, rimLight: 0.4)
  - All specials now restore to default constants instead of saved values
  - Fixed CyberAxe saving wrong light values when previous effect had modified them
  - Fixed sandblasting saving wrong light values when previous effect had modified them
  - All 4 specials verified to properly reset time scale and active flags

- **Sandblasting Event Fixes:**
  - Fixed sandblasting bar blink animation (border pulse on container, not clipped box-shadow)
  - Fixed lights flickering during sandblasting after CyberAxe special
  - Tracked and cleared CyberAxe flicker timeouts (7 setTimeout calls at 200-2100ms)
  - Tracked and cleared CyberAxe wall flash interval (50ms updates for 8 seconds)
  - Tracked and cleared CyberAxe cleanup timeout (3s delay that was restoring lights mid-sandblast)
  - Lights now stay off for full 11-second sandblasting duration

- **Memory Leak Fixes:**
  - Added proper geometry disposal for laser tube effect
  - Added proper material disposal for laser tube effect
  - Added proper geometry/material disposal for laser particles (30 spheres per blast)
  - Added proper geometry/material disposal for shockwave rings (8 toruses per blast)
  - Prevents memory accumulation during repeated CyberAxe special usage

- **CyberAxe Special Updates:**
  - Changed notification text from "CyberAxe Execution!" to "CyberAxe Node Overload!"
  - Updated tooltip from "System Overload" to "Node Overload"

## v0.19.14 - Model Placement System
- **Model Placement Tool:**
  - Press M (when hitboxes enabled) to create model placement boxes
  - Interactive 3D placement with magenta wireframe boxes and arrows
  - Click box to open model placement menu with:
    - Model dropdown (19 models: all .glb files from models/ and people/)
    - Position X/Y/Z inputs (type exact coordinates)
    - Rotation X/Y/Z inputs (degrees)
    - Scale input (0.1-1000 range)
    - Loop Animation checkbox
    - Test/Duplicate/Delete/Close buttons
    - Copy Data button (copies JSON to clipboard)
  - Click arrows to move models 2.0 units in any direction
  - Box positioned at model center (Y+3 offset from feet)
  - All models hardcoded in loadModelPlacements() (no localStorage)
  - Animation mixers update every frame for looping animations

- **Background Characters Added:**
  - 7 animated background characters positioned around game area
  - female_1_idle, female_3_idle, female_4_idle
  - alien_female_1_sitting_idle, alien_male_1_idle, alien_male_1_sitting_idle
  - male_2_sitting_idle
  - All with scale 12-14 and looping animations

- **UI Improvements:**
  - Number keys 1-4 now only trigger specials when NOT typing in input fields
  - Fixed scale input to allow values up to 1000
  - Copy Data button with visual feedback (green checkmark for 2 seconds)

## v0.19.13 - Particle Placement Improvements
- **Manual Coordinate Entry:**
  - Added X, Y, Z input fields to placement menu
  - Can now type exact coordinates instead of only using arrows
  - All coordinate inputs update placement in real-time

- **Improved Arrow Movement:**
  - Increased movement distance from 0.5 to 2.0 units per arrow click
  - Faster particle positioning for large adjustments

- **Hardcoded Permanent Particles:**
  - Removed localStorage for particle placements
  - Two permanent cyberaxe_electric_walls particles hardcoded at:
    - Position 1: (-28.0, 1.5, 40.5)
    - Position 2: (-35.0, 1.0, -30.0)
  - All particles now defined directly in HTML code
  - Placement system now for development/testing only

## v0.19.12 - Particle System Accuracy Update
- **Particle Emission Shapes:**
  - Fixed all emission shapes to exactly match particle editor implementation
  - Added missing 'cone' emission shape (0.5 radius at Y=0)
  - Fixed 'ring' emission shape radius (now 1.0-1.3, was 0.5-1.0)
  - All shapes now use same values as particle_editor.html: point, sphere, box, cone, ring

- **Particle Velocity System:**
  - Velocity calculation now exactly matches particle editor
  - Uses velocityDirX/Y/Z as base direction vector
  - Applies spread randomness using theta/phi angles
  - Removed incorrect normalization and complex spread calculations

- **Particle Placement UI:**
  - Increased arrow size for easier clicking (3.0 length, 1.0/0.6 head)
  - Arrows positioned further from box (3 units instead of 2)
  - Improved hitbox interaction for placement manipulation

## v0.19.11 - Particle Placement System (Developer Tool)
- **Particle Effect Map Editor:**
  - Press P (when hitboxes enabled) to create particle placement boxes
  - Interactive 3D placement boxes with 6 directional arrows
  - Click box to open placement menu with:
    - Dropdown to select from all available particle effects
    - Enable/Disable toggle
    - Loop checkbox for continuous effects
    - Position display (X, Y, Z coordinates)
    - Test button to preview particle
    - Duplicate button to copy placement
    - Delete button to remove placement
  - Click arrows to move placements 0.5 units in any direction
  - All placements saved to localStorage (survives refresh)
  - Visual indicators: Green box = enabled, Red box = disabled
  - Only visible when "Show Hitboxes" is enabled
  - Acts as live particle effect map editor for game development

- **Hand-Tracked Particle Effects:**
  - Added CyberAxe electric effects to both hands
  - `cyberaxe_electric.json` on right hand
  - `cyberaxe_electric_left.json` on left hand
  - Particles follow hand bones during special animation

## v0.19.10 - Game Controls & Lighting Enhancements
- **New Game Controls Panel:**
  - Added game controls panel left of music controls with 6 buttons
  - Toggle Lights (💡/🌑) - Turn all scene lights on/off
  - Toggle Particles (✨/❌) - Enable/disable particle effects
  - Toggle Wall Emissive (💠/⚫) - Control wall LED pulsing animation
  - 3 placeholder buttons for future features
  - All buttons show visual state with emoji changes

- **Sandblasting Lighting Improvements:**
  - Wall emissives now dim by 90% during sandblasting event
  - Wall LED pulse animation pauses during sandblasting
  - Walls stay dark for full 11-second sandblasting duration
  - Proper restoration of wall emissives after event completes

## v0.19.9 - Rogue Government Sandblasting Event
- **New Game Feature:**
  - Added Rogue Government Sandblasting event system
  - Charges 25% per special ability activation (all 4 specials contribute)
  - At 100% charge, triggers automatic sandblasting event
  - Drops 60-100 random single links from random columns over 7 seconds
  - Links alternate rotation (0° and 90°) for proper stacking
  - New HUD panel in bottom-right with charge meter and icon
  - Custom tooltip explaining the mechanic
  - Icon uses items/sandblast_compressed.png
  - Orange/red color scheme (#FF6B35)
  - Links fall with gravity physics and lock into grid on collision
  - Auto-triggers consensus checking after links settle

## v0.19.8 - Console Logging Cleanup
- **Code Cleanup:**
  - Removed console.log statement from Zooko particle spawn diagnostic
  - Cleaned up debug logging in particle effect system
  - Improved performance by removing unnecessary console output

## v0.19.7 - Bone-Tracked Particle System
- **Particle System Enhancements:**
  - Added bone tracking support for particles to follow 3D model bones in real-time
  - Particles can now be parented to skeleton bones with customizable offsets
  - Added `parentBone`, `parentModel`, and `boneOffset` options to particle effects
  - Zancas special now spawns hand-tracking orb particles that follow his hand bone
  - Fixed particle position updates to maintain offset from parent bone
  - Particles with bone parents update position every frame to stay attached
  - Changed default spawn mode back to 'camera' for camera-relative positioning
  - zancas_special.json now properly uses camera-relative positioning
  - zancas_special_orb.json uses world-space with bone tracking

## v0.19.6 - Particle System Improvements
- **Particle System Changes:**
  - Removed old cube-based particle explosion system entirely
  - All effects now use JSON-based particle system exclusively
  - Added zancas_special.json particle effect on Zancas special ability activation
  - Added zancas_special_break.json particle effect for link conversions (50% spawn chance)
  - Added zancas_special_orb.json test particle for world-space positioning
  - Nate special break particles reduced to 25% spawn chance to reduce visual clutter
  - Improved particle system world-space positioning capabilities

## v0.19.5 - Console Spam Cleanup
- **Code Cleanup:**
  - Removed all console.log, console.warn, and console.error statements from zlock_consensus.html
  - Removed debug TRACE logs from particle effect system
  - Removed special ability charge/activation console messages
  - Removed model loading error console messages
  - Cleaned up particle editor localStorage console logs
  - Improved performance by eliminating unnecessary console output

## v0.19.4 - Particle Editor LocalStorage Fixes
- **Particle Editor Bug Fixes:**
  - Fixed localStorage not saving template changes when adjusting sliders/inputs
  - Added `saveTemplatesToStorage()` call after `updateCurrentTemplateFromControls()`
  - Fixed atlas and UV coordinate changes not persisting to localStorage
  - Added `saveTemplatesToStorage()` in `onAtlasClick()` and `updateUV()` functions
  - Fixed template array initialization preventing proper storage loading
  - Templates now correctly load from localStorage on page load
- **Particle Editor New Features:**
  - Added file input button to import modal for uploading .json particle files
  - Import modal now supports both file upload AND paste JSON text
  - Created `loadJsonFile()` function to read uploaded files
- **Particle Editor Improvements:**
  - Added debug console logging for template save/load operations
  - Shows number of templates loaded from localStorage
  - Indicates when defaults are used vs. stored templates

## v0.19.3 - CyberAxe Special Bug Fixes
- **CyberAxe Special Fixes:**
  - Fixed game freeze after CyberAxe special ends
  - Removed fog references (scene has no fog - indoors)
  - Chain now unfreezes immediately when special completes
  - Reset chainVelocity to 0 after freeze to prevent instant drops
  - Auto-spawn new chain if none exists after special
  - Fixed TypeError from accessing null scene.fog.color
  - Time scale restored immediately (no 500ms delay)
  - Added console logging for debugging chain state
- **Zooko Special Timing:**
  - Increased destruction duration from 3 seconds to 5 seconds
  - More time to see particle effects on destroyed links
- **Nate Special Particle:**
  - Added nate_special.json particle effect on activation
  - Spawns in camera view like Zooko's effect

## v0.19.2 - Particle Position Fix
- **Zooko Link Break Particles:**
  - Adjusted Y-coordinate spawn position for link break particle effects
  - Changed from `y + 0.5` to `y + 1.0` for better visual alignment with block centers
  - Particles now appear properly centered on destroyed links during Zooko special ability

## v0.19.1 - Code Refactoring
- **Game Initialization Refactoring:**
  - Unified all 6 duplicate `startGame()` functions into single `startGame(startingLevel)` function
  - Reduced code from ~360 lines to ~95 lines (saved ~265 lines)
  - Automatic score calculation: `(level - 1) * 1000`
  - Dynamic notification flag setting based on starting level
  - Skip button wrapper functions now call unified function with level parameter
  - Easier maintenance - bug fixes apply to all start levels automatically
  - Cleaner codebase with no duplicate initialization logic

## v0.19.0 - Advanced Particle System
- **JSON-Based Particle Effects:**
  - New particle effect system with JSON configuration files
  - Support for texture atlas sprite sheets with UV coordinate selection
  - Configurable particle properties: size, color, opacity, velocity, lifetime
  - Multiple emission shapes: point, sphere, box, cone, ring
  - Blend modes: normal, additive, multiply
  - Per-axis velocity direction controls (velocityDirX, velocityDirY, velocityDirZ)
  - Rotation speed and turbulence effects
  - Particle type options: sprite (billboard) or plane with face camera toggle
- **Zooko Special Particle Effects:**
  - Main visual effect spawns in camera view when Zooko special activates
  - Individual particle effects on each destroyed link during chain break
  - Camera-relative positioning system for consistent visual placement
  - World-space positioning for block destruction effects
- **Particle System Architecture:**
  - `loadParticleEffectFromJSON()` - Load effect configurations from JSON
  - `createParticleEffect()` - Instantiate effects with position/rotation/delay
  - `spawnParticleEffect()` - Helper with camera-relative or world positioning modes
  - `updateParticleEffects()` - Animation loop with lifetime management
  - Texture caching system for efficient atlas reuse
  - Emission accumulator for fractional particle rates
- **Technical Features:**
  - Fixed sprite rendering issues with camera-relative positioning
  - Proper velocity calculation without unwanted acceleration
  - Directional movement separate from initial velocity spread
  - Support for delayed particle emission
  - Automatic cleanup of completed effects

## v0.18.13 - Transparent Special Notifications
- **Special Ability Notification Improvements:**
  - Changed all special ability notification popups to use transparent backgrounds
  - Background opacity set to 20% (0.2 alpha) using `rgba()` colors
  - Added `backdrop-filter: blur(10px)` for frosted glass effect
  - Allows players to see gameplay through the notification
  - Maintains color-coded gradients for each character:
    - Zancas: Blue gradient (86, 204, 242) → (47, 128, 237)
    - Nate: Orange/Gold gradient (242, 153, 74) → (242, 201, 76)
    - Zooko: Purple gradient (155, 81, 224) → (187, 107, 217)
    - CyberAxe: Cyan gradient (0, 255, 255) → (0, 191, 255)
  - Text remains white and fully opaque for readability

## v0.18.12 - Chain Preview Queue
- **Chain Preview Display:**
  - New preview panel at top-center showing next 3 chains queued to spawn
  - Labels: "NEXT", "THEN", "AFTER" for each preview slot
  - Visual chain representation with colored blocks (24x24px each)
  - Shows actual link types, colors, and special properties
  - Encrypted chains display as gray blocks
  - Glowing/broken chains display as white blocks with glow effect
  - Semi-transparent dark background with blur effect
  - Updates in real-time as chains spawn
- **Chain Queue System:**
  - `chainQueue[]` array maintains 3 upcoming chains
  - `generateChainData()` creates chain configuration data
  - Determines chain length, types, and special properties
  - Respects all special chain configs (multi-color, encrypted, glowing)
  - `initializeChainQueue()` called on all game start functions
  - Queue shifts when chain spawns, new chain added to end
- **Technical Implementation:**
  - Chain data pre-generated before spawn for consistent preview
  - `updateChainPreview()` renders visual blocks in preview
  - Color mapping uses LinkType color values
  - Special chain logic applied during generation, not spawn
  - Integrated with all 6 game start functions (level 1, 10, 50, 100, 1000, 10000)

## v0.18.11 - Clickable Compass & Top-Down Button
- **Clickable Compass Directions:**
  - Click N, E, S, or W on compass to switch to that camera view
  - Compass directions now have hover effects (lighter color + glow)
  - Clicking a direction while in top-down view switches back to that side view
- **Top-Down View Button:**
  - New "TOP DOWN" button below compass
  - Toggles top-down view on/off
  - Button highlights when top-down view is active (blue glow)
  - Positioned at bottom-left (60px left, 15px bottom)
- **Keyboard Shortcut:**
  - T key instructions added to HUD: "T Top Down View"
  - Fixed T key handler to call `switchToTopDown()` function
- **UI Improvements:**
  - Added `pointer-events: auto` to compass directions
  - `updateCompass()` now updates top-down button active state
  - `switchToView(viewIndex)` exits top-down mode when switching to side view

## v0.18.10 - CyberAxe Special AI Compatibility & Tooltip Corrections
- **Tooltip Accuracy Updates:**
  - Zooko: Changed from "Red blocks" to "most common block type"
  - Nate: Changed from "Gold consensus" to "destroys all glowing links, then unleashes a cleanup tornado that shuffles the board"
  - Zancas: Changed from "Green chaos" to "transforms the two most common block types into Gold"
  - CyberAxe: Updated to "Technologist using game mod unleashes an overload of laser fury, maximizing node output and clearing entire columns"
- **CyberAxe Special AI Compatibility:**
  - Disabled instant drop when CyberAxe special is active (blocks AI's 20x gravity multiplier)
  - Clear `instantDrop` flag when CyberAxe special starts (fixes issue with subsequent activations)
  - Slowed AI movement speed 3x during CyberAxe special (`effectiveMoveDelay` multiplier)
  - Laser interval slowed from 200ms to 400ms when AI is enabled
  - Total duration remains 5 seconds for all modes
- **Bug Fixes:**
  - CyberAxe special now properly visible and effective when AI mode is enabled
  - AI no longer instantly drops chains during laser animation
  - All special ability tooltips now accurately describe their actual game mechanics

## v0.18.6 - Click-to-Activate Specials
- Click special ability icons to activate (in addition to keyboard 1-4)
- Icons now show hover effect (scale + glow) and click feedback
- **Color swap fix:** Zooko now Red (ZEC-D), Nate now Gold (ZEC-A)
- **Charge rate:** 1 point per link (100 links needed to fill)
- Version updated to v0.18.6

## v0.18.5 - Special Abilities Charge System
- **MAJOR FEATURE:** Special abilities panel with charge bar system
- **Visual Design:**
  - Left-side panel with 4 character special abilities
  - Character icons: 80x80px (doubled from initial 40x40)
  - Vertical charge bars: 12px wide, 80px tall, positioned left of each icon
  - Bars fill from bottom to top using linear gradients
  - Color-matched gradients: Red (Zooko), Gold (Nate), Green (Zancas), Blue (CyberAxe)
  - Tooltips on hover showing character names and special descriptions
  - Semi-transparent dark background with border radius
- **Charge System:**
  - Charge range: 0-100 for each character
  - **Charge rate: 5 points per link placed** (need 20 links to fill = 100 points)
  - Block type to character mapping:
    - `ZEC-A` (Gold 0xF2C94C) → Nate
    - `ZEC-B` (Blue 0x2D9CDB) → CyberAxe
    - `ZEC-C` (Green 0x27AE60) → Zancas
    - `ZEC-D` (Red 0xEB5757) → Zooko
  - **Charge gained when chain locks**, not when clusters clear
  - Each link in a chain adds 5 points to the matching character
  - Each special ability requires 100% charge to activate
  - Charge consumed (reset to 0) after using special
- **Technical Implementation:**
  - New variables: `zookoCharge`, `nateCharge`, `zancasCharge`, `cyberaxeCharge`
  - `addSpecialCharge(blockType, amount)` function handles charge addition
  - Handles blockType as both object `{color, emissive, name}` and string
  - Uses `blockType.name` property for type detection
  - `updateSpecialAbilityBars()` updates visual bar heights
  - Charge checks added to all 4 special activation functions:
    - `playZookoSpecialAnimation()` - checks charge >= 100
    - `playNateSpecialAnimation()` - checks charge >= 100
    - `playZancasSpecialAnimation()` - checks charge >= 100
    - `playCyberAxeSpecialAnimation()` - checks charge >= 100
- **Bug Fixes:**
  - Fixed blockType detection: was object, now extracts `.name` property
  - Added charge requirement gates to prevent infinite special usage
  - Removed debug console.log statements for cleaner production code
- **Integration:**
  - Charge system integrated with `lockChain()` function
  - Each link placed adds 5 points to corresponding character charge
  - Special abilities reward strategic placement of specific link types
  - Visual feedback shows progress toward unlocking each special
- Version tracking: All 4 version locations updated to v0.18.5

## v0.18.4 - Score Per Minute Fix & Pause Time Tracking
- **BUG FIX:** Score/Min display was always showing 0
- **ROOT CAUSE:** Duplicate `startGame()` functions causing critical initialization failure
- **Issue Details:**
  - TWO `startGame()` functions existed (lines 4618 and 7170)
  - Second function overwrote the first, making first function unreachable dead code
  - Second function was incomplete - missing `gameStartTime` initialization
  - Second function missing `modelLoaded` check, broken links clear, many state resets
  - Result: `gameStartTime` always remained `null`, breaking score/min calculation
- **Fix:**
  - Deleted duplicate `startGame()` function at line 7170
  - Merged stats reset from duplicate into the complete version
  - Added `gameStartTime`, `pauseStartTime`, `totalPausedTime` initialization
  - Now only ONE complete `startGame()` function exists
- **ENHANCEMENT:** Pause time tracking for accurate score/min
- **New Variables:**
  - `pauseStartTime` - tracks when pause began
  - `totalPausedTime` - accumulates total paused duration
- **Pause Behavior:**
  - `pauseGame()` records pause start time
  - `resumeGame()` adds pause duration to total paused time
  - Score/min calculation: `activePlayTime = totalElapsedTime - totalPausedTime`
  - Only counts actual playing time, excludes paused time
- **HUD Update:**
  - `updateHUD()` now called every frame in animation loop during gameplay
  - Score/min updates continuously instead of only on scoring events
  - Removed debug console spam
- **Code Quality:**
  - Eliminated 40+ lines of duplicate/dead code
  - Fixed function shadowing bug
  - Cleaner initialization flow
- Version tracking: All 4 version locations updated to v0.18.4

## v0.18.3 - Material Property Bug Fix
- **BUG FIX:** Removed invalid emissive properties from MeshBasicMaterial
- **Issue:** 1170+ console warnings about invalid material properties
- **Root Cause:** MeshBasicMaterial doesn't support `emissive` or `emissiveIntensity` properties
- **Properties only work on:** MeshStandardMaterial or MeshPhongMaterial
- **Fixed in 3 locations:**
  - Purple laser tube material
  - Yellow particle materials (30 particles per blast)
  - Cyan shockwave ring materials (8 rings per blast)
- **Materials now use:** Simple `color` property only with MeshBasicMaterial
- **Effect:** Eliminated all console warnings, visual effects still bright and visible
- Version tracking: All 4 version locations updated to v0.18.3

## v0.18.2 - CyberAxe Visual Effects Polish
- **ENHANCED:** CyberAxe laser execution visual effects
- **Visual Effects:**
  - Purple laser tube (0x9D00FF) - solid center beam without transparency issues
  - Yellow particle system (0xFFFF00) - 30 particles swirling down around the tube
  - Cyan shockwave rings (0x00FFFF) - 8 rings pulsing down the column with expansion effect
  - Ring sizing reduced to 0.15 radius (from initial 0.5) for tighter, more focused effect
- **Lighting Effects:**
  - All scene lights (key, fill, ambient, rim) now turn off/on during special
  - Random flicker pattern: lights toggle at 200ms, 400ms, 600ms, 1200ms, 1400ms, 2000ms, 2100ms
  - Each flicker lasts 100ms creating dramatic strobe/electrical malfunction effect
- **Duration Adjustment:**
  - Reduced CyberAxe special from 8 seconds to 3 seconds
  - Now fires 15 laser blasts (down from 40) at 200ms intervals
  - More intense, snappier special ability
- **Character Scaling:**
  - Reduced CyberAxe model scale from 15 to 14 (all axes)
- **Technical Improvements:**
  - Converted scene lights to global variables for dynamic control
  - Removed transparency/alpha from laser effects to prevent rendering bugs
  - Solid materials only for all new visual effects
- Version tracking: All 4 version locations updated to v0.18.2

## v0.18.1 - Critical Floor Collision Bug Fix
- **BUG FIX:** Corrected floor collision formula that was destroying most links on landing
- **Issue:** When any chain hit the floor, all links except one were being destroyed
- **Root Cause:** Incorrect formula in v0.17.2 - used `stopAtY = (fallingChain.length - 1) - i + 0.5` which positioned links below grid bounds
- **Fix:** Changed to `stopAtY = fallingChain.length - 0.5` 
- **Technical Details:**
  - Formula is now independent of which link (i) detects floor collision
  - Always positions chain so bottom-most link lands at gridY=0 (y=0.5)
  - For 2-link chain: `stopAtY = 1.5`, bottom link at y=0.5 (gridY=0), top link at y=1.5 (gridY=1)
  - For 5-link chain: `stopAtY = 4.5`, bottom at gridY=0, links properly stacked at gridY 0-4
- **Removed:** Debug console logging from CyberAxe model loading and special effect
- Version tracking: All 4 version locations updated to v0.18.1

## v0.18.0 - CyberAxe Character & Laser Execution Special
- **NEW CHARACTER:** CyberAxe added to the game room
- **Character Positioning:**
  - Placed at (25, -7, 25) - diagonal opposite corner from Zooko
  - Faces center during idle animation
  - Cyan wireframe hitbox (0x00FFFF)
  - Same scale as other characters (15x)
  - Rotates to face wall during execution special
- **CyberAxe Execution Special:**
  - Click CyberAxe or press **4** to activate
  - 8-second laser execution sequence
  - Time slows down like other specials
  - Room lights flash dramatically (smooth sine wave oscillation)
  - Wall emissive intensity pulses between 0.5 and 1.5
  - Fog color brightness flashes in sync for full room effect
  - Fires cyan laser beams down falling chain column every 200ms (40 total shots)
  - Player can move chain during special to target multiple columns
  - Each laser destroys all blocks in column from top to bottom
  - Awards 10 points per block destroyed
  - Laser beams have cyan glow with fade-out effect
- **Technical Implementation:**
  - Added `cyberAxeModel`, `cyberAxeMixer`, animation actions, click detection
  - Rotation system: base rotation (-135°) for idle, special rotation (90°) for execution
  - `triggerCyberAxeSpecialEffect()` with wall/fog flashing and laser firing
  - `fireLaserBlast()` creates visual laser beam and destroys column blocks
  - Integrated into character animation update loop
  - Keyboard shortcut: **4** key
  - Click detection via raycaster on cyan hitbox
- **Visual Effects:**
  - Smooth oscillating light flash using sine wave (50ms update interval)
  - Scene fog color changes for dramatic room lighting
  - Cyan laser cylinders with transparency and emissive glow
  - Staggered block explosions from top to bottom of column
  - All effects restore to normal after special ends
- Version tracking: All 4 version locations updated to v0.18.0

## v0.17.3 - Glowing Links Tutorial Guide
- **NEW:** Tutorial popup for broken/glowing links
- **Glowing Links Guide:**
  - White/gold styled notification matching other level popups
  - Shows when player first creates a broken link (rotation mismatch)
  - Only displays if game started at level 1 (not on skip levels)
  - Explains broken links can be clicked/shot for 100 points each
  - Mentions auto-destruction when hitting floor
- **Implementation:**
  - Added `glowingLinksGuideShown` tracking variable
  - Created `#glowingLinksGuide` popup with white gradient and gold accents
  - Trigger in `markLinkAsBroken()` function
  - Pauses game during display, resumes on dismiss
  - Styled with pulsing star symbols (★) in preview
- **UI/UX:**
  - Consistent with existing level notification system
  - Slide-in animation from left
  - "GOT IT!" button to dismiss
  - Only shows once per game session
- Version tracking: All 4 version locations updated to v0.17.3

## v0.17.2 - Glowing Chain Floor Collision Fix
- **BUG FIX:** Glowing chains now stop at correct floor position
- **Issue:** Glowing chains were hovering ~0.5-1.0 units above the floor
- **Root Cause:** Floor collision calculation didn't account for chain length when setting stopAtY
- **Fix:** Changed `stopAtY = i + 0.5` to `stopAtY = (fallingChain.length - 1) - i + 0.5`
- **Result:** All chain types (normal, multi-color, encrypted, glowing) now land flush with floor at y=0.5
- **Technical Details:**
  - stopAtY now correctly calculates top link position based on total chain length
  - Bottom link lands at gridY=0, top link at gridY=(length-1)
  - Glowing chains with length 2-5 now behave identically to shorter chains
- Version tracking: All 4 version locations updated to v0.17.2

## v0.17.1 - Nate Tornado + Glowing Links Synergy
- **NEW:** Nate's tornado special now destroys glowing/broken links!
- **Nate Special Enhancement:**
  - Before tornado starts, all broken/glowing links explode
  - Each broken link awards 100 points
  - Particle explosions for each destroyed link
  - Links removed from grid and brokenLinks set
  - Tornado then proceeds with remaining blocks
- **Synergy with Level 50 Glowing Chains:**
  - Glowing chains (pre-broken) are perfect targets for Nate's tornado
  - Strategic combo: Let glowing chains accumulate, then trigger Nate
  - Instant points from all glowing links + tornado shuffle bonus
- **Implementation:**
  - Added broken link destruction phase at start of `triggerNateSpecialEffect()`
  - No changes to existing tornado movement logic
  - Clean separation: destroy first, then tornado
- Version tracking: All 4 version locations updated to v0.17.1

## v0.17.0 - Glowing Chains & Template System (Level 50 Feature)
- **NEW:** Glowing chains unlock at level 50!
- **Level 50 Notification System:**
  - Gold gradient popup with star symbols (★)
  - Shows "NEW CHAIN TYPE: Glowing Chains"
  - Preview displays 5 glowing blocks with pulsing animation
  - Warning text: "These chains are already glowing - click to break them for bonus points!"
  - Fixed CSS styling - notification properly hidden by default with `display: none;`
- **Glowing Chain Mechanics:**
  - 15% chance to spawn glowing chains at level 50+
  - Random length from 2-5 links (longer than normal chains!)
  - **Each link is a random type (mixed colors like multi-chains)**
  - **All links are PRE-BROKEN (glowing white) when they spawn**
  - Links are immediately clickable for bonus points when they land
  - No cluster formation needed - instant clickable bonus links!
  - **Ultra-bright white emissive glow:**
    - Base emissive intensity: 1.5 (nearly double normal links)
    - Pulsing animation: 1.0 to 2.0 intensity range
    - Maximum brightness for maximum visibility!
  - Continuous pulsing glow while falling
  - Links remain glowing and clickable after locking into grid
  - Automatically added to `brokenLinks` set when locked
- **TEMPLATE SYSTEM for Chain Types:**
  - New `CHAIN_TYPE_CONFIGS` array for easy extensibility
  - Each chain type defined by single configuration object:
    - Level threshold
    - Spawn rate percentage  
    - Custom length ranges (optional)
    - Notification styling (gradient, border color, preview blocks)
    - Custom logic function for chain generation
  - **Future chain types can be added in minutes by:**
    1. Adding config object to `CHAIN_TYPE_CONFIGS` array
    2. Defining `customLogic` function for mechanics
    3. System auto-generates notifications, level checks, tracking
  - Eliminates manual code duplication across 5+ locations
  - All existing chain types (multi-color, encrypted, glowing) now use template
- **Chain Type Priorities:**
  - System checks highest-level chains first
  - Only one special chain type per spawn
  - Normal chains spawn if no special type triggers
- **Visual Effects:**
  - Glowing chains have golden-orange gradient preview (★ symbols)
  - CSS animation with pulsing box-shadow and scale transform
  - In-game pulse synced to real-time using `Date.now()`
  - White emissive glow matches standard broken link appearance but much brighter
- Updated all skip functions to properly initialize level 50 notification flag
- Version tracking: All 4 version locations updated consistently

## v0.16.0 - Encrypted Chains (Level 20 Feature)
- **NEW:** Encrypted chains unlock at level 20!
- **Level 20 Notification System:**
  - Purple/blue gradient popup similar to level 10
  - Shows "NEW CHAIN TYPE: Encrypted Chains"
  - Preview displays gray blocks with "?" symbols
  - Animated pulsing effect on encrypted preview
- **Encrypted Chain Mechanics:**
  - 20% chance to spawn encrypted chains at level 20+
  - Chain links appear gray with hidden colors while falling
  - Cannot see what colors you're placing until chain locks
  - Strategic challenge - must plan blind placements!
- **Decryption Animation (when chain lands):**
  - Staggered decryption - each link decrypts 200ms after previous
  - 20 colored particles spiral outward from each decrypting link
  - Smooth 0.5s color transition from gray → actual color
  - Pulsing glow effect during decryption (emissive intensity)
  - Particles rotate, fade out, and slow down naturally
  - Total cascade effect ~0.8s for 4-link chain
- **Visual Effects:**
  - Color lerp interpolates RGB from gray (#333) to link color
  - Particles use actual link colors (gold/blue/green/red)
  - Spiral particle pattern with random variations
  - Emissive intensity pulses 0.6 to 1.0 using sine wave
- Works seamlessly with multi-color chain system from level 10
- Notification management properly handles skip functions

## v0.15.0 - Music Player & 10 Unique Tracks
- **NEW:** On-screen music controls in HUD (bottom right)
- **Music control buttons with emoji icons:**
  - ⏮️ Previous Track
  - ⏹️ Stop
  - ▶️/⏸️ Play/Pause (icon changes based on state)
  - ⏭️ Next Track
  - 🔊/🔇 Mute/Unmute (icon changes based on state)
- **10 completely unique music tracks:**
  1. Deep House Groove (124 BPM) - Classic house with repeating root notes
  2. Ambient Chill (90 BPM) - Ultra-low frequencies (27-32 Hz), very sparse
  3. Techno Drive (140 BPM) - High frequency constant 16th note pulse
  4. Jazz Fusion (110 BPM) - Walking bass with chromatic steps
  5. Trap Beats (150 BPM) - Sub bass (32 Hz) with octave jumps
  6. Lo-Fi Study (85 BPM) - Smooth chromatic progression
  7. DnB Energy (174 BPM) - Rapid fire bass with 1/8th note timing
  8. Synthwave Retro (118 BPM) - Fast arpeggios with octave jumps
  9. Downtempo Groove (95 BPM) - Sparse dub-style with long gaps
  10. Electro Funk (128 BPM) - Syncopated funky rhythm
- Each track has unique frequencies, rhythms, and musical patterns
- Track info display shows current track name and position (e.g., "🎵 Deep House Groove (1/10)")
- Clean, modern button design with hover effects
- Semi-transparent background with blur effect
- BPM dynamically adjusts based on selected track plus game intensity
- **Fixed:** AI toggle now properly resets drop speed when disabled
- **Fixed:** Music duplication on pause/resume and menu navigation

## v0.14.2 - UI Button Text Cleanup
- **Updated skip button layout:** All buttons now use single-line text
- Changed from two-line format (`TEXT<br>START AT LEVEL X`) to single-line with dash separator
- Button text format: `QUESTION? - START AT LEVEL X`
- Examples:
  - `SKIP TUTORIAL - START AT LEVEL 10`
  - `ARE YOU GOOD? - START AT LEVEL 50`
  - `EXPERT? - START AT LEVEL 100`
  - `ARE YOU CRAZY? - START AT LEVEL 1000`
  - `SUPER HUMAN? - START AT LEVEL 10,000`
- Cleaner, more consistent visual presentation
- Easier to read at a glance

## v0.14.1 - AI Usage Tracking & Tutorial Skip Friendly
- **NEW:** AI usage tracking in high scores
- **🤖 AI badge** appears next to scores where AI was used at any point
- Tracks if AI was ever enabled during a game session
- Shows in both "Top 20 High Scores" and "Last 5 Games"
- **Tutorial skip (Level 10) now achievement-friendly!**
  - Starting at Level 1 OR Level 10 allows all achievements
  - Starting at Level 50+ disables most achievements (only milestone achievements allowed)
- **Added NOTE on title screen:** "Skipping past Level 10 disables most achievements"
  - Positioned below the last skip button
  - Informs players about achievement restrictions
- Achievement fairness: `earnedNotSkipped = (startLevel === 1 || startLevel === 10)`

## v0.14.0 - Start Level Tracking & Achievement Fairness
- **NEW:** High scores now track and display what level the game started at
- **Start level icons in scoreboard:**
  - 🟢 Level 1 (Normal start - earned)
  - 🔵 Level 10 (Tutorial skip)
  - 🟠 Level 50 (Good player)
  - 🔴 Level 100 (Expert)
  - 🟣 Level 1000 (Crazy)
  - 🟡 Level 10,000 (Superhuman)
  - ⚪ Custom/other starts
- **Achievement system updated:**
  - Most achievements only unlockable if started from level 1 (earned, not skipped)
  - Specific level milestones (10, 50, 100) can be earned by starting at that exact level
  - Prevents achievement farming by skipping to high levels
  - Encourages legitimate progression from level 1
- Icons appear next to rank in both "Top 20 High Scores" and "Last 5 Games"
- Adds `startLevel` property to saved game data

## v0.13.1 - Add Level 10,000 Skip Button
- **NEW:** "SUPER HUMAN? START AT LEVEL 10,000" skip button
- Bright magenta/pink color (rgba(255, 0, 255)) - the most extreme difficulty
- Positioned below the "Are You Crazy?" (Level 1000) button
- Drop speed at level 10,000: **40.146×** (267× faster than level 1!)
- Starts with 9,999,000 score
- For players who want to experience absolute impossibility
- All 5 skip buttons now available:
  - Level 10 (Teal) - Skip tutorial
  - Level 50 (Orange) - Are you good?
  - Level 100 (Red) - Expert?
  - Level 1000 (Purple) - Are you CRAZY?
  - Level 10,000 (Magenta) - SUPER HUMAN?! ← NEW!

## v0.13.0 - Add Level 1000 Skip Button
- **NEW:** "ARE YOU CRAZY? START AT LEVEL 1000" skip button
- Purple color scheme (rgba(138, 43, 226)) to indicate extreme difficulty
- Positioned below the Expert (Level 100) button
- Drop speed at level 1000: **4.146×** (insanely fast!)
- Starts with 999,000 score
- For players who want to experience true chaos immediately
- All 4 skip buttons now available:
  - Level 10 (Teal) - Skip tutorial
  - Level 50 (Orange) - Are you good?
  - Level 100 (Red) - Expert?
  - Level 1000 (Purple) - Are you CRAZY?!

## v0.12.2 - Remove Drop Speed Cap (Infinite Scaling!)
- **REMOVED 5× CAP** - Drop speed now scales infinitely with level
- Formula: `dropSpeed = 0.15 + (level - 1) × 0.004`
- Game will become progressively harder without limit until it's impossible to play
- **Level progression examples:**
  - Level 1: 0.15× (beginner friendly)
  - Level 100: 0.546×
  - Level 1,000: 4.146×
  - Level 10,000: 40.146× (insanely fast!)
  - Level 100,000: 400.146× (literally impossible)
  - Level 1,000,000+: Beyond human capability
- HUD display also updated to show uncapped speed
- The game WILL eventually become unplayable - this is intentional!

## v0.12.1 - Add Drop Speed Display
- **NEW:** Drop speed indicator in HUD (below SCORE/MIN)
- Shows current level's drop speed multiplier (e.g., "0.15×" at level 1, "0.54×" at level 100)
- Updates in real-time as level increases
- Orange color (#FF9F1C) to match the dynamic nature of the value
- Same styling as SCORE/MIN counter for consistency
- AI indicator moved down to avoid overlap (top: 460px)

## v0.12.0 - Level-Based Drop Speed Scaling
- **NEW:** Drop speed now scales progressively with level (much harder at high levels!)
- **Level 1:** 0.15× gravity (70% slower than before - beginner friendly!)
- **Level 10:** 0.24× gravity (still learning)
- **Level 50:** 0.39× gravity (getting challenging)
- **Level 100:** 0.54× gravity (original speed)
- **Level 250:** 0.84× gravity (fast)
- **Level 1000:** 1.65× gravity (very fast)
- **Level 10000:** 4.65× gravity (extreme difficulty - caps at 5×)
- Fast drop (space key) is 2.5× the normal speed at each level
- Instant drop (double-tap space or AI) remains at 20× for quick placement
- Formula: `baseSpeed = 0.15 + (level - 1) × 0.004` (max 5.0)

## v0.11.2 - Fix AI Drop Speed Isolation
- **FIXED:** AI instant drop no longer affects player controls
- AI now only sets `instantDrop = true` when `aiState.enabled` is true
- When AI is disabled, player has full control over drop speeds (space key, double-tap)
- When AI is enabled, chains drop instantly for fast testing (intended behavior)
- Player can now play normally while AI toggle is off

## v0.11.1 - Remove Old MP3 Sound Effects
- Removed old MP3-based sound effect system (`loadChainBreakSounds()`, `playChainBreakSound()`)
- Removed audio loading variables: `chainBreakSounds`, `audioContext`, `audioBuffers`
- All sound effects now use Web Audio API synthesis (better quality, no file loading)
- Removed all `playChainBreakSound()` calls from break/clear events
- Cleaner codebase - only synthesized audio remains

## v0.11.0 - Unlimited Levels
- **REMOVED LEVEL CAP** - levels now count infinitely (up to JavaScript's max safe integer: 9,007,199,254,740,991)
- Level formula: `level = Math.floor(score / 1000) + 1`
- Expert button now truly starts at level 100 (99,000 score)
- Game will get progressively faster and harder indefinitely
- Eventually becomes unplayable at extreme levels - this is intentional!

**Level Milestones:**
- Level 100 = 99,000 score
- Level 1,000 = 999,000 score
- Level 10,000 = 9,999,000 score
- Level 100,000 = 99,999,000 score
- And beyond...

## v0.10.3 - Skip Button Spacing Fix v2
- Further increased spacing to account for button height + padding
- Level 50 button: 90px below center (accounting for ~60px button height)
- Level 100 button: 180px below center (2x the spacing)
- Proper clearance between all buttons now

## v0.10.2 - Skip Button Spacing Fix
- Increased spacing between skip buttons to prevent overlap
- Level 50 button: 80px below center (was 75px)
- Level 100 button: 160px below center (was 150px)
- No more text overlap between buttons

## v0.10.1 - Skip Button Consistency
- Made all 3 skip buttons the same size (220px width)
- Uniform padding: 14px 32px for all buttons
- Uniform font size: 18px for all buttons
- Consistent spacing: 75px between each button
- All buttons centered with text-align

## v0.10.0 - Advanced Skip Levels
- Added "Are you good? Start at Level 50" button (orange color)
- Added "Expert? Start at Level 100" button (red color) - actually starts at level 99 (max)
- Positioned below the Level 10 skip button on left side
- Level 50 starts with 49,000 score
- Level 100 starts with 98,000 score (level 99 - game max)
- Perfect for testing high-level gameplay and music intensity

## v0.9.2 - AI Initialization Fix
- Fixed AI not activating on page load even when setting is checked
- AI state now properly syncs with saved settings on startup
- AI indicator visibility updates correctly after DOM loads
- No need to toggle AI off/on to activate it anymore

## v0.9.1 - AI Player Bug Fix
- Fixed AI player errors: `rotateChain` and `moveChain` were undefined
- Changed to use correct functions: `rotatePiece()` and `tryMove()`
- AI now properly rotates and moves chains
- Fixed rotation logic to convert rotation count (0-3) to degrees (0-270)

## v0.9.0 - AI Player for Testing
- Added AI player toggle in Settings (Testing section)
- AI automatically plays the game for fast testing
- AI evaluates positions based on:
  - Matching blocks below and adjacent
  - Avoiding stacking too high
  - Preferring lower/faster placements
- Move delay: 100ms (very fast play)
- Visual indicator: "🤖 AI PLAYING" shown when enabled
- All AI code marked with comments for easy removal later
- AI uses simple heuristic scoring (not perfect, but effective)

**How to use:**
1. Open Settings
2. Check "AI Player (Testing)" at bottom
3. Start/resume game and watch AI play
4. Disable to play manually again

## v0.8.5 - Level 10 Notification Fix
- Fixed level 10 notification not showing if player skips level 10 (e.g., jumps from level 9 to 11)
- Now shows when transitioning from any level below 10 to level 10 or above
- Condition changed from `level === 10` to `oldLevel < 10 && level >= 10`

## v0.8.4 - Level 10 Unlock Notification
- Added popup notification when reaching level 10
- Shows on left side with teal/green gradient background
- Displays multi-color chain preview with 4 colored blocks
- Explains new multi-type chain mechanic to player
- Pauses game until player acknowledges with "GOT IT!" button
- Only shows once per game session
- Skipped when using "Skip Tutorial" button (player already knows)

## v0.8.3 - Corner Chain Fix
- Fixed corner feed tube chains developing gaps over time
- Chain links now maintain perfect 1-unit spacing using overshoot calculation
- Prevents drift accumulation that caused gaps at higher levels
- Corner chains remain visually solid indefinitely

**Technical Fix:**
The original code reset links to a fixed position (-4) when they scrolled past the top, causing spacing drift. Now uses `overshoot` calculation: when a link reaches position 25 and has moved 0.3 units past, it resets to -4 + 0.3 = -3.7, maintaining exact spacing.

## v0.8.2 - Auto Restart Setting
- Added "Auto Restart Game" option to Settings panel
- Default: ON - Game automatically restarts on game over
- When OFF: Shows confirmation dialog to restart or return to menu
- Perfect for speedrunning and practice sessions

## v0.8.1 - Skip Tutorial Button
- Added "Skip Tutorial / Start at Level 10" button on title screen
- Button positioned on left middle side for easy access
- Allows experienced players to jump straight to multi-type chains
- Styled with teal/green theme to differentiate from main buttons

## v0.8.0 - Multi-Type Chain Challenge
- Added new ZEC-MULTI chain type that appears at level 10+
- Multi chains contain 1-5 randomly mixed link types (ZEC-A/B/C/D)
- 30% spawn chance at level 10+ for increased difficulty
- Each link in a multi-type chain can be a different color
- Matching logic works with individual link types, not the chain type

## v0.7.1 - SPM Display Fix
- Fixed Score Per Minute display styling and positioning
- SPM now properly positioned below Consensus counter (300px from top)
- Added gold color (#F2C94C) to SPM value for visibility
- SPM counter now updates correctly during gameplay

## v0.7.0 - Dynamic Music System & Score Per Minute
- **Music starts on first block landing** - No music until gameplay begins
- **Score Per Minute (SPM) tracker** - New HUD element displays current scoring rate
- **Dynamic BPM** - Music tempo increases with SPM (124-160 BPM range)
- **Intensity-based instrumentation**:
  - Low SPM (0-1000): Bass + basic drums
  - Medium SPM (1000-3000): + More frequent hi-hats and synth stabs
  - High SPM (3000-6000): + Synth stabs every 2 beats
  - Extreme SPM (6000+): + Maximum intensity
- **Hyper Mode System**:
  - Triggered by combos (3-5.5 seconds) and floor clears (6 seconds)
  - Stacks up to 5x - multiple bonuses compound the effect
  - Adds +4 BPM per stack, increased volume, more frequent effects
  - Gradually fades out after bonus window
- **Responsive music** - Your scoring performance directly shapes the soundtrack
- Music now feels like a reward for good play and builds excitement during streaks

## v0.6.1 - Techno Link Sounds & Collision Audio
- **Techno-style link breaks**: Aggressive sawtooth synths with resonant filters (Q=12)
- **Pitch variation**: ±10 cents random variation on each note for natural, non-repetitive feel
- **Faster envelopes**: Punchy 5ms attack for techno edge
- **Floor hit sounds**: 5 variations of deep impact sounds tuned to C minor key
- **Chain collision sounds**: 6 variations of metallic percussive hits with inharmonic partials
- **Smart collision detection**: Different sounds for floor vs chain-on-chain impacts
- **Pitch drops**: Impact sounds sweep from high to low for satisfying thud
- All sounds integrated with reverb and tuned to match house music key

## v0.6.0 - House/Electronica Background Music
- **16-bar chord progression**: Extended musical arrangement (64 beats before loop)
- **House tempo**: Increased to 124 BPM for authentic house feel
- **Four-on-the-floor kick drum**: Classic house beat on 1 and 3
- **Full drum kit**: Kick, snare/clap on 2 and 4, hi-hats on eighth notes
- **Synth stabs**: Evolving chord stabs every 2 bars with filter sweeps
- **Complex bass patterns**: Syncopated rhythms, octave jumps, passing notes
- **Musical progression**: i-iv-v-iv-VI-III-v-V7 (minor to major shifts for interest)
- **Rhythmic variation**: Different bass patterns in each section
- Background music now listenable for extended periods with proper house groove

## v0.5.7 - Enhanced Bass & Atmospheric Depth
- **5-layer bass**: Added deep sub-bass (2 octaves lower), triangle wave layer for massive depth
- **Continuous atmospheric pad**: 3-note ambient pad (C-E-G) with detuned oscillators runs throughout gameplay
- **Deep sub bypass**: Deepest bass layer bypasses filter for maximum low-end impact
- **Stereo width**: Detuned oscillators create wide, immersive soundscape
- **Fixed floor clear**: Floor clear bonus now resets properly after placing new blocks
- Background music now has substantial depth and warmth befitting AAA production

## v0.5.6 - Victory Song on Floor Clear
- **15-second victory song**: Beautiful, euphoric synthwave composition plays when board is cleared
- **Chord progression**: I-V-vi-IV (C-G-Am-F) with rich harmonies and melody
- **4-voice pad synthesis**: Detuned sawtooth and triangle waves for lush, wide sound
- **Smooth bass line**: Sine wave bass supporting the chord progression
- **Auto-resume**: Normal gameplay music resumes after victory song completes
- Victory song uses same reverb and compression chain for professional quality

## v0.5.5 - AAA Audio Quality & Falling Chain Music
- **Upgraded to professional-grade audio synthesis**:
  - Added convolution reverb for spatial depth (2-second impulse response)
  - Added dynamic compression for polished, consistent sound (-24dB threshold, 12:1 ratio)
  - Layered bass: sub-bass (sine), main bass (sawtooth), detuned bass for stereo width
  - Layered synth leads: 3 oscillators per note (square + detuned square + triangle octave)
  - Proper ADSR envelopes (attack/decay/sustain/release) for expressive sound
  - Resonant filters with sweeps for movement and synthwave character
  - High-pass filtering to remove muddiness
- **Falling chain music**: Hi-hat percussion plays on eighth notes while chain is falling
- **Fixed music settings**: Music now respects enabled/disabled setting and volume control
- **Settings integration**: Music starts/stops based on settings panel toggles in real-time

## v0.5.4 - Musical Puzzle System (Lumines-Style)
- Added Web Audio API music generation system
- Each link type plays a unique musical note when cleared (C5, E5, G5, B5)
- Chain links play sequentially creating rhythmic melodies (50ms intervals)
- Added 120 BPM synthwave bassline with C2-E2-G2-E2 pattern
- Multiple breaking chains create layered procedural music
- Bassline starts on game start, stops on pause/game over
- Square wave synthesis with lowpass filtering for retro synth sound

## v0.5.3 - Character Special Keyboard Shortcuts

### Added
- **Keyboard Shortcuts for Character Specials**: Number keys now trigger character special animations
  - Press **1** to activate Zooko's special animation
  - Press **2** to activate Nate's special animation
  - Press **3** to activate Zancas's special animation
  - Works identically to clicking on character models
  - Available during gameplay and other states

### Technical
- Added keyboard event handlers in `onKeyDown()` for keys 1, 2, 3
- Shortcuts call `playZookoSpecialAnimation()`, `playNateSpecialAnimation()`, and `playZancasSpecialAnimation()`
- Maintains same behavior as clicking character hitboxes

## [v0.5.2] - 2025-11-14

### Added
- **Corner Feed Tubes**: Decorative animated chain feeds at all 4 corners
  - Translucent cylindrical tubes positioned outside grid corners
  - Continuous chain of colored links scrolling upward at 1.5 units/second
  - Links cycle through all 4 types (gold, purple, blue, green) randomly
  - Chains extend below floor and above ceiling for seamless loop effect
  - Creates visual impression of chains being fed into the game

### Technical
- Added `cornerTubes` and `cornerChains` arrays for corner feed system
- Created `createCornerFeedTubes()` function called after model load
- Corner tubes positioned at offset 0.75 units from grid edges
- Each corner has GRID_HEIGHT + 5 links (30 total per corner)
- Links start at y=-4 and wrap to bottom when reaching y>GRID_HEIGHT
- Created `updateCornerChains()` function for smooth scrolling animation
- Links recycle with random new colors when wrapping around

## [v0.5.1] - 2025-11-13

### Added
- **Double-Tap Instant Drop**: Press space bar twice quickly for super-fast drop
  - Double-tap detection within 300ms window
  - Instant drop uses 20× gravity multiplier for near-instant placement
  - Hold space for normal fast drop (1.125× multiplier)
  - Smooth animation maintained even at high speeds
  - Enables advanced play techniques for experienced players

### Technical
- Added `instantDrop` flag and `lastSpaceTime` tracking
- Added `doubleTapThreshold` constant (300ms)
- Modified `updateFallingChain()` to handle three speed modes:
  - Normal: 0.5× gravity
  - Fast drop: 1.125× gravity
  - Instant drop: 20× gravity
- Space key release now clears both fastDrop and instantDrop flags

## [v0.5.0] - 2025-11-13

### Added
- **LED Pulse Effect**: Wall LEDs now have a smooth, slow pulsing animation
  - Emissive intensity oscillates between 0.3 and 0.6 over a 4-second cycle
  - Creates gentle breathing effect on all wall textures
  - Applies to north, south, east, west walls and floor

### Changed
- **Table Color**: Inverted table model colors from white to dark blue-grey (0x0A0E12)
  - Better visual harmony with dark room theme
  - Materials now clone to avoid affecting other instances

### Technical
- Added `roomWalls` array to store references to wall meshes
- Created `updateLEDPulse()` function called every frame
- Uses sine wave calculation for smooth pulse timing
- Removed all debug console.log statements for clean production code

## [v0.4.9] - 2025-11-13

### Fixed
- **Visual Alignment**: Corrected positioning of grid floor, table, and column indicators
  - Floor indicator now positioned at y=0.5 to align with bottom chain link centers
  - Grid frame raised by 0.5 units to match new floor reference
  - Table model raised from y=-10 to y=-9.5 for proper alignment
  - Column tube height adjusted to 24.5 units (y=0.5 to y=25)
  - Eliminated visual gap between floor indicator and landed chains

### Technical
- Grid vertical positioning now consistently uses y=0.5 as floor reference
- Tube geometry: height=24.5, positioned at y=12.75 (center)
- All visual elements now properly aligned with chain link positioning system

## [v0.4.8] - 2025-11-13

### Added
- **Active Chain Column Indicator**: Visual feedback showing where the falling chain will land
  - Thin cyan vertical line (tube) appears in the active chain's column
  - Cyan glowing square on floor shows exact landing position
  - Indicators only visible while chain is falling
  - Automatically hide when chain locks into place
  - Helps players quickly identify chain placement location

### Fixed
- **Tube Rendering Issue**: Resolved frustum culling problem preventing column tubes from rendering
  - Added `frustumCulled = false` to ensure tubes render from all camera angles
  - Changed from transparent materials to solid visibility toggling for reliable rendering
  - Tubes now use color-based system instead of opacity to avoid Three.js transparency sorting issues

### Technical
- Created `createFloorIndicators()` to generate 36 floor plane indicators (one per grid cell)
- Floor indicators positioned at y=0.01 to prevent z-fighting with grid floor
- Modified `updateColumnTubes()` to manage both column tubes and floor indicators
- Tube radius reduced to 0.05 for subtle straw-like appearance
- Removed debug console logs for tube creation

## [v0.4.7] - 2025-11-13

### Added
- **Settings in Pause Menu**: Added SETTINGS button to pause menu for easier access
  - Players can now adjust settings without exiting to main menu
  - Settings button positioned between RESTART and QUIT TO MENU
  - Closing settings panel returns to pause menu instead of resuming game
  - Seamless flow: Pause → Settings → Close → Back to Pause Menu

### Technical
- Added `showSettingsFromPause()` function to hide pause screen before showing settings
- Modified `closeAllPanels()` to check game state and restore pause screen if paused
- Maintains proper screen state transitions when navigating between pause and settings

## [v0.4.6] - 2025-11-13

### Added
- **Top-Down Camera View**: Press **T** to toggle 5th camera view looking straight down at grid
  - Camera positioned directly above grid center at height 24
  - Provides bird's-eye view of entire playfield
  - Independent of 4-direction side views (N/E/S/W)
  - Absolute controls in top-down view for intuitive movement:
    - **W** moves up (north)
    - **S** moves down (south)
    - **A** moves left (west)
    - **D** moves right (east)
  - Press **T** again to return to side view
  - Q/E camera rotation works independently of top-down toggle

### Technical
- Added `isTopDownView` boolean flag to track camera mode
- Added `topDownHeight` constant (24 units)
- Modified `updateCameraPosition()` to handle top-down view case
- Added `toggleTopDownView()` function bound to T key
- Modified `getMovementVector()` to use absolute directions when in top-down view
- Side views maintain camera-relative controls as before

## [v0.4.5] - 2025-11-13

### Fixed
- **Font Loading Performance**: Google Fonts now load asynchronously to prevent game lag when offline
  - Changed from blocking `@import` to async `<link>` with preconnect hints
  - Added fallback fonts (Arial for Inter, Courier New for JetBrains Mono)
  - Game starts immediately even without internet connection
- **Play Again Crash**: Fixed "Cannot read properties of undefined (reading 'rotation')" error
  - Game now properly clears all blocks, meshes, and state when restarting
  - Added safety checks in `lockChain()` to prevent accessing undefined objects
  - `startGame()` now fully resets grid, falling chain, broken links, and game variables
  - Prevents thousands of error messages when clicking "Play again"

### Technical
- Async font loading with `media="print" onload` technique
- Font display set to `swap` for better performance
- Added comprehensive cleanup in `startGame()`: clears grid, removes meshes, resets flags
- Added null/undefined checks in `lockChain()` for fallingChain and links
- Clears `brokenLinks` set on game restart
- Resets `chainVelocity` and `spawnScheduled` flags

## [v0.4.4] - 2025-11-13

### Fixed
- **Broken Links Auto-Destroy**: Glowing broken links now automatically destroy when they reach the floor
  - Prevents unclickable broken links at floor level (y=0)
  - Broken links that fall to floor are instantly destroyed with particle effects
  - Plays chain break sound and removes block from grid automatically
  - Improves gameplay flow by eliminating stuck broken links

### Technical
- Added automatic broken link destruction in `findCluster()` function
- Checks for broken links at floor level when cluster touches floor
- Triggers explosion and cleanup for broken links at y=0

## [v0.4.3] - 2025-11-13

### Changed
- **Character Animations**: Character idle animations now play continuously in the background
  - Zooko, Zancas, and Nate no longer appear in T-pose on the title screen
  - Animations run during menu screens for visual polish
  - Game physics and chain updates still only occur during gameplay

### Technical
- Moved character animation mixer updates outside of `GameState.PLAYING` check
- Animation mixers update every frame regardless of game state
- Gameplay-specific updates (chains, physics) remain gated by game state
- Separate `deltaTime` calculations for animations vs gameplay physics

## [v0.4.2] - 2025-11-13

### Added
- **Nate Special Effect**: Click Nate to trigger chaotic tornado ability
  - Creates a whirlwind effect that shuffles blocks around the board
  - Time slows to 30% during effect for dramatic slow-motion tornado
  - Each block moves 4 times to adjacent empty positions
  - 5 blocks move simultaneously per wave for chaotic tornado movement
  - Blocks spin and rotate during movement for visual tornado effect
  - Effect duration: 3-4 seconds with rapid movements (75ms intervals)
  - Blocks are reset to proper 0° or 90° rotation after tornado completes
  - Gravity applies after tornado to settle blocks into final positions

### Fixed
- **Block Rotation Lock**: After Nate's tornado, all blocks reset to 0° or 90° rotation
  - Prevents blocks from being stuck at 45° or other odd angles
  - Ensures proper interlocking chain link appearance
  - Resets x and z rotation to 0 for clean alignment

### Technical
- Added `nateSpecialActive` flag to prevent overlapping tornado effects
- Created `triggerNateSpecialEffect()` function with wave-based movement system
- Tornado moves blocks in waves (5 blocks per 75ms interval)
- Block movement animations are 40ms with increased rotation speed (0.15 rad/frame)
- Post-tornado rotation normalization based on y-position parity
- Wave counting ensures tornado stops properly after completing all movements

## [v0.4.1] - 2025-11-13

### Changed
- **Zancas Animation**: Special animation now plays exactly once without looping
  - Simplified animation logic to play once then return to idle
  - Removed loop counter system for cleaner code

## [v0.4.0] - 2025-11-13

### Added
- **Zooko Special Effect**: Click Zooko to trigger powerful board-clearing ability
  - Identifies and destroys all blocks of the most common type
  - Time slows to 30% during effect for dramatic slow-motion sequence
  - Blocks explode with particle effects over 3 seconds with staggered timing
  - Gravity automatically applies after all blocks are destroyed
  - Sound effects and visual explosions for each destroyed block
  
- **Zancas Special Effect**: Click Zancas to trigger alchemical transmutation ability
  - Finds the two most common block types on the board
  - Transforms all blocks of those types into gold/yellow chains (ZEC-A)
  - Time slows to 30% during effect for mystical slow-motion sequence
  - Smoke particle effects surround each block as it transforms
  - Transformations occur over 3 seconds with staggered timing
  - Smoke particles drift upward, fade out, and grow gradually
  - Transformed blocks can create new matches after effect completes

### Changed
- **Zancas Animation**: Special animation now loops 1 time (reduced from 2)
- **Time System**: Added global time scale system for slow-motion effects
  - All physics and game updates respect `currentTimeScale`
  - Characters can trigger time slowdown during special abilities

### Technical
- Added `zookoSpecialActive`, `zancasSpecialActive` flags to prevent overlapping effects
- Added `currentTimeScale`, `slowTimeScale`, `normalTimeScale` variables
- Created `triggerZookoSpecialEffect()` function for Zooko's ability
- Created `triggerZancasSpecialEffect()` function for Zancas's ability
- Created `createSmokeEffect()` function for smoke particle system
- Modified `animate()` to apply time scale to deltaTime
- Block type counting algorithm finds most common types across entire grid
- Smoke particles have upward bias, opacity fade, scaling, and velocity dampening

## [v0.3.7] - 2025-11-13

### Added
- **Performance Counter**: Real-time FPS and memory usage display
  - Small overlay on right middle edge of screen
  - Shows current frames per second
  - Displays JavaScript heap memory usage (Chrome only)
  - Updates every second

### Changed
- **Nate Material Adjustments**: Improved skin appearance to reduce copper/red tones
  - Applied full matte finish (roughness = 1.0, metalness = 0.0)
  - Aggressively lightened base color with 60% white blend
  - Applied to all materials on Nate model for consistent appearance

### Technical
- Added `frameCount`, `lastFpsUpdate`, `currentFps` variables for FPS tracking
- Performance stats updated in animation loop every 1000ms
- Memory usage via `performance.memory` API
- Material color adjustment formula: `color * 0.4 + 0.6` (60% white blend)

## [v0.3.6] - 2025-11-13

### Added
- **Enhanced Special Animation System**: Characters now support looped special animations
  - Separate position and rotation control for special animations
  - Characters move to custom position during special, return to idle position after

### Changed
- **Zancas Special**: Animation loops 2 times before returning to idle
- **Nate Special**: Animation loops 4 times before returning to idle
- Characters now store original position and smoothly return after special animation completes

### Technical
- Added `zancasSpecialPosition`, `zancasSpecialRotation`, `zancasSpecialLoopCount` variables
- Added `nateSpecialPosition`, `nateSpecialRotation`, `nateSpecialLoopCount` variables
- Special animations can be customized independently from idle state

## [v0.3.5] - 2025-11-12

### Added
- **Nate Character**: Third animated 3D character model in the game room
- Nate plays idle animation loop continuously
- Click Nate to trigger special animation (plays once then returns to idle)
- "Nate Special!" notification message with orange gradient
- Yellow wireframe collision box for Nate
- Independent rotation control for special animation
- Rim light for better character edge definition

### Changed
- **Improved Lighting**: Softer, more balanced scene lighting
  - Reduced key light intensity (1.2 → 0.8)
  - Reduced fill light intensity (0.6 → 0.3)
  - Increased ambient light (0.4 → 0.5)
  - Changed to neutral white/gray tones
  - Added shadow casting with high quality (2048x2048)
- **Skin Material Adjustment**: Automatically reduces shininess on character skin materials
  - Sets roughness to 0.9 for matte appearance
  - Removes metalness for realistic skin
  - Preserves clothing and accessory materials

### Technical
- Nate positioned at (-10, -9, 10) with 15x scale
- Material detection for skin/face/head/body keywords

## [v0.3.4] - 2025-11-12

### Added
- **Zancas Character**: Second animated 3D character model in the game room
- Zancas plays idle animation loop continuously
- Click Zancas to trigger special animation (plays once then returns to idle)
- "Zancas Special!" notification message with blue gradient
- Green wireframe collision box for Zancas (vs Zooko's red)
- Independent rotation control for special animation

### Changed
- Zancas positioned at (30, -7, -20) with 14x scale
- Zancas rotates to face forward during special animation, returns to base rotation after
- Both character hitboxes controlled by "Show Hitboxes" debug setting

## [v0.3.3] - 2025-11-12

### Added
- **Zooko Character**: Animated 3D character model in the game room
- Zooko plays idle animation loop continuously
- Click Zooko to trigger special animation (plays once then returns to idle)
- "Zooko Special!" notification message on click
- Collision box for reliable click detection
- **Debug Setting**: "Show Hitboxes" toggle in Settings to display collision boxes

### Changed
- Zooko positioned at (-10, -9, -10) with 15x scale
- Click detection works from any camera angle

## [v0.3.2] - 2025-11-12

### Changed
- Enhanced chain link emissive glow (increased intensity to 0.6)
- Removed color overlay to preserve original model textures and logos
- Chain links now glow without altering base colors

### Fixed
- Chain link Z logo colors now preserved correctly

## [v0.3.1] - 2025-11-12

### Added
- Custom wall textures for all four walls (North, South, East, West)
- Custom floor texture with linear filtering for smooth appearance
- Emissive mapping on walls and floor for selective brightness
- Light areas in textures glow while dark areas remain dark

### Changed
- Replaced solid color walls with textured environment
- Enhanced visual atmosphere with custom artwork

## [v0.3.0] - 2025-11-12

### Added
- **Floor Clear Bonus**: Award 10,000 points when all chains are cleared from the game floor
- Special animated bonus message displays for 3 seconds
- **Consensus Counter**: New HUD display showing total chain links cleared
- Floor clear achievement tracking

### Changed
- Bonus awards only once per game session
- Consensus counter displayed below combo on right side of HUD

## [v0.2.5] - 2025-11-12

### Added
- Crosshair cursor appears when hovering over broken links
- Real-time cursor feedback for clickable broken chains

### Changed
- Enhanced visual feedback for broken link interaction

## [v0.2.4] - 2025-11-12

### Changed
- Simplified floor detection logic: entire cluster skips rotation validation if ANY link touches floor
- After gravity, clusters are re-evaluated normally without floor exception

### Fixed
- Floor-connected chains now reliably skip rotation checks on initial landing
- Eliminated edge cases with partial floor connection detection

## [v0.2.3] - 2025-11-12

### Fixed
- Gravity now waits for staggered cluster removal to complete before applying
- Broken link coordinates are updated when blocks fall to new positions
- Broken links remain clickable after falling due to gravity
- Floor-connected vertical chains skip rotation validation correctly
- Only vertical neighbors (same column) trigger rotation checks
- Both links must be floor-connected to skip validation

### Changed
- Improved broken link tracking during gravity application
- Added smooth animation for falling blocks (200ms duration)
- Cleaned up stale broken link entries during mouse clicks

## [v0.2.2] - 2025-11-12

### Added
- Rotation-based chain validation system (Consensus Mechanic)
- Broken links now glow bright white when rotation alignment fails
- Mouse click detection to destroy broken links
- Rotation validation only applies to vertical connections (same column)

### Changed
- Adjacent chain links in vertical stacks must alternate rotation (0°-90°-0° pattern)
- Improved raycasting to exclude grid lines, only checking broken link meshes
- Broken links require manual player intervention (mouse click) to remove

### Fixed
- Grid lines no longer interfere with mouse click detection on broken links

## [v0.2.1] - 2025-11-12

### Added
- High Scores screen with TOP 20 scores and LAST 5 games
- High scores now track: score, level, play time, score per minute
- Game history system stores last 5 games played
- "Clear High Scores" button in Settings (with confirmation)
- High Scores button on main menu

### Changed
- Quit and Restart now save scores to history
- High score display shows proper #1, #2, #3 numbering
- High scores kept to top 20 (up from 10)

### Fixed
- High scores panel hidden on game start
- Crashes when displaying old score data without time/scorePerMinute fields

## [v0.2.0] - 2025-11-12

### Added
- Chain break sound effects (5 variations: a-e)
- Web Audio API integration with AudioContext
- Randomized sound playback on each link break
- Audio buffer caching for performance
- Staggered cluster clear animation (center outward, 50ms delay per link)

### Changed
- Fall speed reduced by 50% for starting levels (gravity multiplier: 1.0→0.5, fast drop: 2.25→1.125)
- Blocks now clear with cascading effect from consensus point outward
- Game blocks start until chain link model loads

### Fixed
- Crash when chain model not loaded (added modelLoaded check to startGame)

## [v0.1.9] - 2025-11-12

### Added
- 3D table model (Zcash_GameTable_A.glb) replaces geometric table
- Table model scaled 10x and positioned at y=-10

### Removed
- Geometric table creation (box primitives for table top and legs)
- All model loading fallback code and error handlers
- Debug console logging from model loaders

### Changed
- Models now load silently without fallbacks
- Table is now fully 3D model-based

## [v0.1.8] - 2025-11-12

### Fixed
- Table positioning corrected to true mathematical center (3, -1.2, 3)
- Table now properly centered under game grid from all four camera angles (North, East, South, West)

### Technical
- Removed temporary X and Z offsets that caused misalignment in different views
- Table position now uses exact grid center calculations: GRID_WIDTH/2, GRID_DEPTH/2

## [v0.1.7] - 2025-11-12

### Added
- GLB model loading support with GLTFLoader
- 3D chain link model (Zcash_Chain_Link_A.glb) replaces placeholder boxes
- Realistic alternating 90° Y-axis rotation for interlocking chain links
- Debug logging for model loading (can be removed in production)

### Changed
- Chain links now use custom 3D model instead of box geometry
- Model scale set to 1.25x for optimal visual appearance
- Links alternate rotation (0°, 90°, 0°, 90°) like real chain links

### Technical
- Requires local web server due to GLB file loading
- Fallback to box geometry if model fails to load

## [v0.1.6] - 2025-11-12

### Added
- Environmental design: 4 colored walls (Blue North, Red South, Green East, Yellow West)
- Room floor at y=-8 with ceiling at y=29
- Wooden table beneath game grid with 4 legs
- Spacious room with 35-unit distance from game to walls

### Changed
- Room dimensions expanded for more breathing room
- Table positioning at y=-1.2 with proper clearance above game grid

## [v0.1.5] - 2025-11-12

### Changed
- Game renamed from "ZLOCK Consensus" to "ZLOCK CHAINER"
- Updated all branding and title screens to reflect new name

## [v0.1.4] - 2025-11-12

### Added
- Particle explosion effects when blocks are cleared
  - 12 particles per block that explode outward in random directions
  - Particles fade out, shrink, and fall with gravity
  - Particle colors match the block type being cleared
- 1 second delay before clusters disappear after reaching consensus
  - Allows players to see which blocks formed the consensus before they clear

### Removed
- All console logging statements removed from production code

## [v0.1.3] - 2025-11-11

### Changed
- Removed grace period - chains now lock instantly upon collision with floor or blocks
- Chains lock immediately when they can no longer fall

### Removed
- 200ms lock grace timer removed from collision system

## [v0.1.2] - 2025-11-11

### Added
- 3D compass/direction indicator in bottom-left corner
  - Shows N/E/S/W cardinal directions
  - Active direction highlights in gold with glow effect
  - Animated blue needle rotates to point at current viewing direction
  - Smooth 0.45s transitions when rotating camera

### Fixed
- Corrected cube frame positioning to align perfectly with grid boundaries
- Fixed camera lookAt point to properly center on grid
- Grid boundaries now correctly span from 0 to GRID_WIDTH/DEPTH instead of offset positions
- Cube frame and grid lines now perfectly aligned at X: 0-6, Y: 0-25, Z: 0-6

## [v0.1.1] - 2025-11-11

### Fixed
- Fixed null pointer crash when accessing chain after lockChain()
- Fixed double-spawn bug causing chains to spawn on top of each other
- Added spawnScheduled flag to prevent immediate re-spawning after lock
- Chains now properly spawn → fall → lock → wait → spawn with correct timing

## [v0.1.0] - 2025-11-11

### Added
- Initial game implementation
- 3D grid system (6×18×6) with Three.js rendering
- 4-camera rotation system (North, East, South, West) with Q/E controls
- WASD movement controls with proper axis remapping for all camera angles
- Falling chain physics with gravity (9.81 units/s²)
- Space bar fast drop (2.25× speed multiplier)
- Lock-grace timer (200ms) before chains lock to grid
- Consensus detection algorithm (BFS 6-neighbor clustering)
- Dynamic clearing threshold (4-6 blocks based on level)
- Gravity compaction with cascade detection
- Combo system (1.0× to 5.0× multiplier, 2s decay timer)
- Score-based level progression (every 1000 points)
- 4 base link types (ZEC-A, ZEC-B, ZEC-C, ZEC-D)
- Pause system with overlay menu (ESC key)
- Settings panel with localStorage persistence
  - Music volume control
  - SFX volume control
  - Music/SFX toggle switches
- Achievement system with 50 achievements across 5 tiers
  - 10 Easier achievements
  - 10 Easy achievements
  - 10 Medium achievements
  - 10 Medium-Hard achievements
  - 10 Very Hard achievements
- Achievement notification popups
- Achievement panel UI with tier grouping
- High score system (top 10 saved to localStorage)
- Statistics tracking (chains placed, clusters cleared, cascades, etc.)
- Randomized spawn positions across grid
- Arrow key piece rotation (visual rotation)
- Game over detection and restart flow
- Responsive canvas with window resize support
- HUD overlay with score, level, and combo displays

### Fixed
- Camera zoom distance increased (8→16 units) for better visibility
- Field of view widened (55°→65°) for improved perspective
- Pause system replaced alert() with proper overlay UI
- Consensus threshold enforces minimum 6 blocks requirement
- Collision detection improved for ground and block interactions
- Spawn position randomization prevents center-only spawns
- WASD movement now correctly applies both X and Z components from movement vectors
- All 4 camera angles now have fully functional directional controls

### Technical Details
- Single-file HTML implementation (~1500 lines)
- Three.js r128 from CDN
- LocalStorage for settings, high scores, and achievements
- DAS (180ms) and ARR (90ms) input timing
- Phong materials with emissive effects and edge highlighting
- Fog effect for depth perception
- Inter font family (400, 600, 700, 900 weights)
- JetBrains Mono for monospaced numbers

---

## Upcoming Features (Planned)

### v0.2.0 - Visual Effects & Polish
- Clearing animation with 5-stage sequence
- Particle system (700 particles max)
- Enhanced lighting effects
- Emissive glow scaling with combo multiplier
- Holographic grid layers

### v0.3.0 - Special & Hazard Links
- 10 Special link types with unique abilities
- 5 Hazard link types with challenge mechanics
- Special link trigger conditions and effects
- Hazard spawn probability ramping

### v0.4.0 - Audio System
- Web Audio API implementation
- Procedural sound generation
- Multi-layer music system (base, pulse, drive, apex)
- SFX for moves, clears, combos, and hazards

### v0.5.0 - Veil Protocol
- Level 99+ endgame mode
- 1000-move challenge system
- Enhanced difficulty mechanics
- Veil-specific achievements

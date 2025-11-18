# Particle Effect Editor - Changelog

## v0.19.7 - Compact 2-Column Layout (2025-01-XX)

### Layout Optimization
- **2-Column Grid Layout:**
  - Reorganized all editor controls into efficient 2-column and 3-column grids
  - Paired related controls: Size Start/End, Opacity Start/End, Color Start/End
  - 3-column layout for velocity direction (X/Y/Z) and gravity controls
  - Added section headers: Emission, Size & Opacity, Velocity, Rotation, Physics, Rendering

- **Compact Sizing:**
  - Reduced label font size from 13px to 11px
  - Reduced value input width from 80px to 60px
  - Reduced control group margins from 15px to 8px
  - Reduced label margins from 5px to 3px
  - Tighter padding throughout (5px → 3px)

- **Space Efficiency:**
  - Editor panel now much shorter and easier to navigate
  - All controls remain accessible and functional
  - Prepared layout for future expansion with many more particle options
  - Maintains visual clarity while maximizing space usage

## v0.19.6 - UI/UX Improvements (2025-11-17)

### UI Improvements
- **Compact Template List:**
  - Reduced template item padding from 12px to 8px
  - Reduced margins from 5px to 3px
  - Smaller font size (13px) for template names
  - Single-line display per template for better density
  - Now shows many more templates at once in the list

- **Template Sorting:**
  - Added sort dropdown above template list
  - Sort by "Last Updated" (default) - shows most recently edited first
  - Sort by "Name (A-Z)" - alphabetical order
  - Templates automatically timestamped when saved or duplicated
  - Duplicated templates get fresh timestamp for "Last Updated" sorting

- **Button Layout Optimization:**
  - Action buttons arranged in 2-column grid for space efficiency
  - Compact button labels: "+ New", "Export", "Import", "Save"
  - Duplicate and delete buttons now properly side-by-side inline
  - Reduced button sizes (20x20px) for cleaner look
  - Smaller gaps between buttons (3px)

- **Save Notifications:**
  - Replaced popup alert with toast notification
  - Green notification appears in top-right corner
  - Auto-dismisses after 2 seconds
  - No need to click "OK"
  - "Save Current" button moved to left panel under "Import"

- **Atlas Grid Default:**
  - Changed default grid from 8x5 to 6x6
  - Grid settings now saved with templates
  - Grid values properly persist across sessions

### Technical Changes
- Added `sortMode` state variable ('updated' or 'name')
- Added `lastUpdated` timestamp field to templates
- Template list sorts before rendering based on selected mode
- Grid columns and rows now part of template data structure

## v0.19.5 - Particle Loop System Fix (2025-11-17)

### Bug Fixes
- **Fixed particle looping behavior:**
  - Changed loop logic to restart based on emitter duration only (not emitter + particle lifetime)
  - Loops now restart immediately when emission ends, not when last particle dies
  - Enables seamless continuous particle effects with overlapping particles
  - New particles spawn while previous particles are still alive and fading out
  - Fixes gap between loop iterations that prevented seamless effects

### Technical Changes
- Updated loop restart condition to check `!isEmitting` instead of `particles.length === 0`
- Removed particle lifetime from loop duration calculation
- Loop now triggers at `emitDuration` boundary for perfect seamless loops

## v0.19.4 - LocalStorage Persistence Fix (2025-11-16)

### Bug Fixes
- **Fixed localStorage not saving template changes:**
  - Added `saveTemplatesToStorage()` call after `updateCurrentTemplateFromControls()`
  - All slider and input changes now persist automatically to localStorage
  - Fixed template array initialization that was preventing proper storage loading
  - Templates are now correctly loaded from localStorage on page load
  
- **Fixed atlas and UV coordinate changes not persisting:**
  - Added `saveTemplatesToStorage()` in `onAtlasClick()` function
  - Added `saveTemplatesToStorage()` in `updateUV()` function
  - UV selections now save when clicking atlas or manually entering coordinates

### New Features
- **File Import for JSON Templates:**
  - Added file input button to import modal
  - Can now upload .json particle files directly
  - Created `loadJsonFile()` function to read uploaded files
  - Import modal supports both file upload AND paste JSON text

### Improvements
- **Debug Logging:**
  - Added console.log messages for template save/load operations
  - Shows number of templates loaded from localStorage
  - Indicates when defaults are used vs. stored templates
  - Helps diagnose persistence issues

### Technical Changes
- Removed redundant template array pre-initialization with defaults
- Improved `loadTemplatesFromStorage()` to properly handle empty storage
- All template modifications now trigger automatic save to localStorage

## v1.0.0 - Initial Release (2025-11-15)

### Core Features
- **Visual Particle Effect Editor:**
  - Real-time preview of particle effects with Three.js renderer
  - Interactive controls for all particle properties
  - Live updates as you adjust parameters
  - Active particle count display

### Texture Atlas Support
- **Atlas Texture System:**
  - Load texture atlases (PNG sprite sheets)
  - Interactive canvas preview with click-to-select sprite regions
  - Adjustable grid overlay (1-16 columns/rows)
  - Manual UV coordinate input (0-1 range with 0.0001 precision)
  - Support for multiple atlas files or solid color particles
  - Included atlases: smoke_effects.png, misc1_effects.png

### Particle Properties
- **Emission Controls:**
  - Particle Count (1-5000)
  - Emission Rate (0-1000 particles/second)
  - Emit Duration (0.1-60 seconds)
  - Emission Shapes: Point, Sphere, Box, Cone, Ring

- **Particle Lifecycle:**
  - Lifetime (0.1-60 seconds)
  - Size Start/End (0-20 units)
  - Start/End Color (hex color pickers)
  - Opacity Start/End (0-1)

- **Velocity & Direction:**
  - Initial Velocity (0-100)
  - Spread Angle (0-180 degrees)
  - Velocity Direction X/Y/Z (-50 to 50)
  - No unwanted acceleration (fixed gravity bug)

- **Physics:**
  - Rotation Speed (-20 to 20)
  - Turbulence (0-10)

- **Rendering:**
  - Blend Modes: Normal, Additive, Multiply
  - Particle Type: Sprite (billboard) or Plane
  - Face Camera toggle
  - Double Sided toggle

### Template System
- **Template Management:**
  - Save/load custom particle effects
  - 20 built-in templates (fireworks, smoke, sparkles, magic, etc.)
  - LocalStorage persistence
  - Duplicate templates with "_copy" suffix
  - Rename templates (double-click name)
  - Delete templates with confirmation
  - Active template highlighting

### Camera Controls
- **Camera Modes:**
  - Orbit: Slow automatic orbit around effect
  - Rotate: Continuous rotation
  - Static: Manual control with OrbitControls

### Playback Controls
- **Effect Playback:**
  - Play/Stop buttons
  - Loop toggle for continuous playback
  - Restart effect button
  - Save current template
  - Auto-restart when looping enabled

### Export System
- **JSON Export:**
  - Export current effect as JSON file
  - Downloadable configuration files
  - Compatible with game particle system
  - All properties preserved

### Pre-built Templates
1. **Firework Burst** - Explosive orange-to-red burst
2. **Smoke Plume** - Rising gray smoke
3. **Magic Sparkles** - Cyan-to-magenta twinkling
4. **Fire** - Upward orange-to-red flames
5. **Rain** - Falling blue droplets
6. **Snow** - Gentle falling snowflakes
7. **Dust** - Swirling brown particles
8. **Energy Ball** - Glowing cyan sphere
9. **Explosion** - Rapid outward blast
10. **Healing Aura** - Rising green glow
11. **Poison Cloud** - Spreading green mist
12. **Electric Spark** - Yellow lightning effect
13. **Portal** - Spinning purple vortex
14. **Shield** - Blue protective shimmer
15. **Teleport** - White flash effect
16. **Blood Splatter** - Red splatter particles
17. **Ice Shards** - Cyan sharp fragments
18. **Leaves** - Falling brown leaves
19. **Coins** - Sparkling gold coins
20. **Stars** - Yellow twinkling stars

### Technical Implementation
- **Particle Creation:**
  - Sprite or plane geometry support
  - Texture atlas UV mapping
  - Color interpolation over lifetime
  - Size scaling over lifetime
  - Opacity fade over lifetime
  - Rotation animation

- **Particle Updates:**
  - Delta time-based animation
  - Velocity-based movement
  - Directional movement (separate from velocity)
  - Turbulence noise
  - Billboard effect for planes (optional)
  - Automatic particle removal when lifetime expires

- **Performance:**
  - Emission accumulator for fractional rates
  - Efficient particle pooling
  - Texture cloning for independent UV mapping
  - Three.js LinearFilter for smooth textures

### User Interface
- **Layout:**
  - Template sidebar (280px) with scrollable list
  - Central 3D preview canvas
  - Controls sidebar (380px) with all parameters
  - Stats display showing active particle count

- **Styling:**
  - Dark theme (#1a1a1a background)
  - Color-coded active template (green)
  - Hover effects on buttons
  - Value displays next to sliders
  - Organized control groups by category

### Known Features
- Templates persist in browser localStorage
- Camera controls work in static mode
- Grid helper visible in preview
- Directional lighting for depth perception
- Export generates properly formatted JSON files

# AUDIO SYSTEM AUDIT - Complete Removal Guide

## CSS STYLES TO REMOVE

### Line 673-726: Music Control Styles
```css
#musicControls { ... }
#musicTrackInfo { ... }
#musicButtons { ... }
.musicBtn { ... }
.musicBtn:hover { ... }
.musicBtn:active { ... }
```

## HTML ELEMENTS TO REMOVE

### Line 1365-1378: Settings Panel Audio Controls
- Music Volume slider
- SFX Volume slider  
- Music Enabled checkbox
- SFX Enabled checkbox

### Line 1720-1726: Music Button Classes (keep buttons, just remove musicBtn class)
- Lines use class="musicBtn" for styling

### Line 1729-1737: Music Controls Panel
```html
<div id="musicControls">
    <div id="musicTrackInfo">🎵 Track 1/10</div>
    <div id="musicButtons">
        <button class="musicBtn" onclick="previousTrack()">⏮️</button>
        <button class="musicBtn" onclick="stopMusic()">⏹️</button>
        <button class="musicBtn" id="playPauseBtn" onclick="togglePlayPause()">▶️</button>
        <button class="musicBtn" onclick="nextTrack()">⏭️</button>
        <button class="musicBtn" id="muteBtn" onclick="toggleMute()">🔊</button>
    </div>
</div>
```

## JAVASCRIPT VARIABLES TO REMOVE

### Line 2124-2138: Music System Variables
- `let musicContext = null;`
- `let musicStarted = false;`
- `let musicIntensity = 0;`

### Line 2152-2158: Music Notes Object
- `const musicNotes = { ... }`

### Line 2159-2211: Music Playlist System
- `let isMusicPlaying = false;`
- `let isMusicMuted = false;`
- `const musicPlaylist = [ ... ]` (10 tracks)

### Line 2213-2216: Settings Object Audio Properties
- `musicVolume: 0.7`
- `sfxVolume: 0.8`
- `musicEnabled: true`
- `sfxEnabled: true`

## JAVASCRIPT FUNCTIONS TO REMOVE

### Line 3062-3091: initMusicSystem()
Creates AudioContext, reverb, compressor, master gain

### Line 3094-3193: generateChordProgression() and related
Music generation logic

### Line 3194-3290: startMusic()
Main music playback function

### Line 3291-3293: stopMusic()
Stops music playback

### Line 3295-3348: createAtmosphere()
Creates ambient atmosphere sounds

### Line 3350-3449: playBassNote()
Plays bass notes

### Line 3452-3473: playStab()
Plays stab sounds

### Line 3475-3587: playKick(), playSnare(), playHihat(), playClap()
Drum sounds

### Line 3589-3625: playLinkNote()
Plays notes when links are cleared

### Additional music functions:
- previousTrack()
- nextTrack()
- togglePlayPause()
- toggleMute()
- updateMusicTrackDisplay()

## JAVASCRIPT FUNCTION CALLS TO REMOVE

### Line 9152: playLinkNote() call in clearCluster()
```javascript
playLinkNote(grid[x][y][z].type, 0); // Play note immediately
```

### Any calls to:
- startMusic()
- stopMusic()
- initMusicSystem()
- Music control button handlers

## SETTINGS SYSTEM UPDATES NEEDED

### updateSettings() function
Remove references to:
- musicVolume
- sfxVolume
- musicEnabled
- sfxEnabled

### loadSettings() function
Remove audio-related localStorage loading

### Default settings object
Remove audio properties

## SUMMARY

**Total Components:**
- ~6 CSS style blocks
- ~8 HTML elements/sections
- ~15 global variables
- ~15 functions
- ~5 function call sites
- Settings system updates

**Approach:**
1. Remove CSS styles (lines 673-726)
2. Remove HTML music controls (lines 1729-1737)
3. Remove HTML settings sliders (lines 1365-1378)
4. Remove JS variables (lines 2124-2216)
5. Remove JS functions (lines 3062-3625+)
6. Remove function calls (line 9152+)
7. Update settings system
8. Remove onclick handlers from buttons

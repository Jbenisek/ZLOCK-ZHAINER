# ZLOCK CHAINER

A 3D blockchain-themed puzzle game inspired by classics like Lumines and Columns. Match colored chain links in a 6×6×25 grid to clear blocks and unleash devastating special abilities!

**Arcade Version:** 0.21.2  
**Tunnels Version:** 0.4.13  
**Created by:** CyberAxe of [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

---

## About

ZLOCK CHAINER is a **two-game universe** combining arcade puzzle action with dungeon crawler RPG adventure:

### **ZLOCK CHAINER (Arcade Game)** - `zlock_consensus.html`
A fast-paced 3D puzzle game where you drop falling chains into a grid and match 6 or more connected blocks of the same color to clear them. As you progress through levels, unlock new chain types including encrypted chains, glowing chains, and multi-colored chains. Charge up four unique character abilities to turn the tide when the grid gets full!

### **TUNNELS OF PRIVACY (Dungeon Crawler)** - `tunnels_of_privacy.html`
A classic dungeon crawler RPG inspired by TI-99's "Tunnels of Doom". Take the same four heroes from the arcade game into a 10-level dungeon quest to find the king's scepter. Features D&D-style stats, turn-based combat, AI-powered NPC conversations, and multiplayer co-op!

### **Portal System - Seamless Game Integration**
Both games share a unified save file system with **bidirectional hero progression**:
- Play arcade, power up heroes, enter portal → continue in dungeon with same heroes
- Explore dungeon, level up heroes, exit portal → return to arcade with upgraded stats
- Single save file (`top_shared_save`) stores progress for both games
- Download/upload save files for backups and cross-browser play

---

## 🚀 Quick Start

### Windows (Local Development)
```powershell
# Navigate to game folder
cd path\to\zlock

# Start the server
python zlock_server.py
```
Then open your browser to `http://localhost:4243/zlock_consensus.html`

### Linux Server (Production/Hosting)
```bash
# Navigate to game folder
cd ~/webhosting/zlock/wwwroot

# Stop any existing server
bash zlock_server.sh stop

# Start the server (runs in background)
bash zlock_server.sh start

# Check server status
bash zlock_server.sh status

# View logs
cat /tmp/zlock_server.log
```

### Server Commands Reference

| Platform | Start | Stop | Status |
|----------|-------|------|--------|
| **Windows** | `python zlock_server.py` | Ctrl+C | (runs in foreground) |
| **Linux** | `bash zlock_server.sh start` | `bash zlock_server.sh stop` | `bash zlock_server.sh status` |

**⚠️ Important:** Always use `zlock_server.py` - do NOT use `python -m http.server` or other simple servers. They won't serve 3D model files (.glb) correctly!

---

## 🤖 AI Features (Optional)

The dungeon crawler includes **AI-powered NPC conversations** and **text-to-speech voices**. These are optional features - the game works fine without them!

### Setting Up AI Chat (LLM)

On first run, the server will ask for API keys:

```
🔑 API KEY SETUP
============================================================
LLM features require API keys for Groq and/or OpenRouter.
Press Enter to skip (LLM chat will be disabled).

GROQ API Key (FREE - get one at console.groq.com):
  > 

OpenRouter API Key (PAID - get one at openrouter.ai):
  > 
```

**Groq (Recommended - FREE):**
1. Go to [console.groq.com](https://console.groq.com)
2. Create a free account
3. Generate an API key
4. Paste it when prompted

**OpenRouter (Optional - PAID):**
1. Go to [openrouter.ai](https://openrouter.ai)
2. Create an account and add credits
3. Generate an API key
4. Paste it when prompted

**What do they do?**
- **With API keys:** NPCs respond with unique AI-generated dialogue based on their personality
- **Without API keys:** NPCs use pre-written fallback responses (game still fully playable)

**Resetting API Keys:**
Delete the `.zlock_api_keys.json` file and restart the server to be prompted again.

### Text-to-Speech (TTS)

The server automatically installs **Piper TTS** for character voices. On first run you'll see:
```
📦 Installing piper-tts (first-time setup)...
✓ piper-tts installed successfully

🎤 Checking TTS voice models...
   (20 voices for variety - ~200MB total on first run)
```

This downloads ~200MB of voice models on first run. After that, voices work offline!

**What does TTS do?**
- Heroes and NPCs speak their dialogue aloud with unique voices
- 20 different British/American voices for variety
- Fully optional - game works without it

---

## 🎮 Multiplayer Co-op (Dungeon Crawler)

Tunnels of Privacy supports **4-player online co-op**!

### How to Play Together

**Host a Game:**
1. Start the dungeon crawler
2. Click **HOST CO-OP GAME**
3. Share the 6-character room code with friends
4. Each player picks one of the four heroes
5. Start the adventure!

**Join a Game:**
1. Start the dungeon crawler
2. Click **JOIN CO-OP GAME**
3. Enter the room code from your host
4. Pick an available hero
5. Wait for host to start

### Multiplayer Requirements
- All players connect to the same server (host's IP:8765 for WebSocket)
- Host controls game flow and saves progress
- Clients see real-time updates but don't save locally

---

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
- **AI NPC Chat** - Talk to NPCs with AI-generated responses (requires API key)
- **Text-to-Speech** - Characters speak with neural TTS voices
- **4-Player Co-op** - Team up online for dungeon adventures
- **Educational Ticker** - Learn about Zcash and privacy tech while browsing menu
- **Music System** - 10 theme tracks with scrolling ticker display
- **Exit Portal** - Return to arcade game with preserved progress

### Portal Save System
- **Unified Save Format** - Single save file with hero stats + game states for both games
- **Download Save File** - Backup your progress as JSON file to computer
- **Load Save File** - Upload save files to restore progress or play across browsers
- **Cross-Game Progression** - Hero stats update in real-time across both games
- **localStorage Persistence** - Automatic save on portal entry/exit

---

## How to Play

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

---

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

---

## Troubleshooting

### "Port 4243 is already in use"
Another server is running. On Linux:
```bash
bash zlock_server.sh stop
# or manually:
sudo lsof -ti:4243,8765 | xargs sudo kill -9
```

### 3D models not loading / GLB errors
You're using the wrong server. Always use `python zlock_server.py` - never use `python -m http.server`.

### API key prompt not appearing
Keys are already saved. Delete `.zlock_api_keys.json` to reset:
```bash
rm .zlock_api_keys.json
```

### TTS not working on Linux
The server auto-installs piper-tts. If it fails, manually install:
```bash
pip install piper-tts --break-system-packages
```

### Multiplayer not connecting
- Make sure port 8765 is open (WebSocket)
- All players must connect to the same server
- Check firewall: `sudo ufw allow 8765/tcp`

---

## Support the Developer

If you enjoy ZLOCK CHAINER, consider donating:

**Zcash Address:**  
`u1gvnthgukm0ecnan3tgj3h6pdhrmmv8zyqx8ayup9yg9er4t5l7nesas6leavc4x3rsj98n65nn2w3ekzur9yejadlmv7k4vjgu8kp58q`

---

**License:** All rights reserved  
**Website:** [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

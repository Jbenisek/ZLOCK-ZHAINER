# ZLOCK CHAINER

A 3D blockchain-themed puzzle game inspired by classics like Lumines and Columns. Match colored chain links in a 6×6×25 grid to clear blocks and unleash devastating special abilities!

**Version:** 0.20.43  
**Created by:** CyberAxe of [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

---

## About

ZLOCK CHAINER is a fast-paced 3D puzzle game where you drop falling chains into a grid and match 6 or more connected blocks of the same color to clear them. As you progress through levels, unlock new chain types including encrypted chains, glowing chains, and multi-colored chains. Charge up four unique character abilities to turn the tide when the grid gets full!

## Features

- **3D Puzzle Gameplay** - 6×6×25 grid with full 3D chain placement
- **Four Character Abilities** - Each with unique board-clearing powers
- **Progressive Difficulty** - Speed increases each level, new chain types unlock at levels 10, 25, and 50
- **Gamepad Support** - Full Xbox/PlayStation/Steam controller support
- **20 Visual Grid Effects** - Customize the grid with effects like Pulse Wave, Rainbow Spectrum, Plasma Field, and more
- **Particle System** - Custom particle effects for abilities and chain destruction
- **High Score Tracking** - Local high score persistence

## How to Play

### Objective
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

1. Clone or download this repository
2. Open `zlock_consensus.html` in a modern web browser
3. No build process required - runs entirely in the browser!

## Development

The game is built with:
- Three.js for 3D rendering
- GLTFLoader for 3D models
- Custom particle system with sprite sheet animation
- LocalStorage for settings and high score persistence

Includes a particle effect editor (`particle_editor.html`) for creating and editing particle effects.

## Support the Developer

If you enjoy ZLOCK CHAINER, consider donating:

**Zcash Address:**  
`u1gvnthgukm0ecnan3tgj3h6pdhrmmv8zyqx8ayup9yg9er4t5l7nesas6leavc4x3rsj98n65nn2w3ekzur9yejadlmv7k4vjgu8kp58q`

---

**License:** All rights reserved  
**Website:** [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)

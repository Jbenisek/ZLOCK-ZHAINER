# ZLOCK ZHAINER - Complete Game Documentation

**Version:** 0.19.45  
**Last Updated:** November 18, 2025

**Created by:** CyberAxe of [OutlandishlyCrafted.com](https://OutlandishlyCrafted.com)  
**Donate with Zcash:** `u1gvnthgukm0ecnan3tgj3h6pdhrmmv8zyqx8ayup9yg9er4t5l7nesas6leavc4x3rsj98n65nn2w3ekzur9yejadlmv7k4vjgu8kp58q`

---

## GRID SYSTEM

**Dimensions:** 6 wide (X) × 25 tall (Y) × 6 deep (Z)  
**Storage:** `grid[x][y][z] = { type: LinkType, mesh: THREE.Object3D, rotation: number }` or `null`  
**Coordinates:** Standard 3D array indexing

---

## LINK TYPES

- **ZEC-A** (Gold `#F2C94C`) - Assigned to Nate
- **ZEC-B** (Blue `#2D9CDB`) - Assigned to CyberAxe
- **ZEC-C** (Green `#27AE60`) - Assigned to Zancas
- **ZEC-D** (Red `#EB5757`) - Assigned to Zooko

---

## CONTROLS

| Key | Action |
|-----|--------|
| **Arrow Up/Down** | Move chain forward/backward (Z-axis) |
| **Arrow Left/Right** | Rotate chain 90° |
| **Space (hold)** | Fast drop (2.5× speed) |
| **Space (double-tap)** | Instant drop (20× speed) |
| **Q/E** | Rotate camera counter-clockwise/clockwise |
| **T** | Toggle top-down view |
| **1/2/3/4** | Activate character specials |
| **+** | Cheat - charge all abilities to 100% |

---

## MATCHING LOGIC

### Connection Algorithm

```javascript
// Flood-fill in 6 directions (±X, ±Y, ±Z)
// Minimum 3 connected links of same color to clear
// Skip encrypted or glowing links (they don't connect)

function findConnectedLinks(startX, startY, startZ, targetType) {
  // Flood-fill search
  // Returns array of connected blocks
  // if (connected.length >= 3) clearLinks(connected);
}
```

---

## GRAVITY SYSTEM

```javascript
function applyGravity() {
  let moved = true;
  while (moved) {
    moved = false;
    // Bottom-up scan (Y=0 to Y=24)
    // If cell below empty and cell above has block:
    //   Move block down, update mesh position
    //   moved = true
  }
  // After settling, checkMatches() for cascades
}
```

---

## DROP PHYSICS

```javascript
// Speed scaling by level (uncapped exponential)
const baseSpeed = 0.15;
const levelScaling = baseSpeed + (level - 1) * 0.004;

// Gravity multipliers
normalDrop: levelScaling
fastDrop: levelScaling * 2.5
instantDrop: 20

// Velocity accumulation
chainVelocity += gravity * gravityMultiplier * deltaTime;
const newY = fallingChain.y - (chainVelocity * deltaTime);

// Collision = lock chain and spawn new one
```

---

## CHARACTER SPECIAL ABILITIES

### 🔴 ZOOKO (Press 1)

**Charge:** Clear red (ZEC-D) links  
**Ability:** Destroys all blocks of most common type over 5 seconds

**Logic:**
1. Count all block types in grid
2. Find most common type
3. Collect all matching blocks
4. Destroy over 5000ms (staggered):
   - `delayPerBlock = 5000 / blockCount`
   - Each: particle effect + remove + null grid
5. `applyGravity()`
6. Restore time scale

**Particles:**
- `zooko_special.json` (camera-relative, distance 8)
- `zooko_special_link_break.json` (world coords, y+1.0)

---

### 🟡 NATE (Press 2)

**Charge:** Clear gold (ZEC-A) links  
**Ability:** Destroys glowing links, then tornado shuffle

**Phase 1: Destroy all glowing links**
- Award 100 points each
- Particle explosion
- Remove from grid

**Phase 2: Tornado (5 waves, 200ms apart)**
- Move blocks toward center (±1 on X/Z)
- 20% chance per block per wave
- Animate mesh positions

**After:** `applyGravity()`  
**Particle:** `nate_special.json` (camera-relative)

---

### 🟢 ZANCAS (Press 3)

**Charge:** Clear green (ZEC-C) links  
**Ability:** Transforms 2 most common types to gold

**Logic:**
1. Count all block types
2. Get top 2 most common
3. Transform all to Gold (ZEC-A):
   - Clone mesh with gold material
   - Set emissive `#F2C94C`
   - Update type

**Immediate effect (no time slow)**

---

### 🔵 CYBERAXE (Press 4)

**Charge:** Clear blue (ZEC-B) links  
**Ability:** Laser down falling chain's column  
**REQUIRES:** Falling chain must exist

**Logic:**
1. Check `fallingChain` exists or abort
2. Freeze chain (`cyberAxeSpecialActive = true`)
3. Store column: `x = fallingChain.x`, `z = fallingChain.z`
4. Visual: lights flicker, walls flash
5. Fire lasers every 200ms (or 400ms in AI mode):
   - Destroy entire column from top to bottom
   - Purple laser tube + particles
   - Shockwave rings
6. After 5 seconds:
   - `cyberAxeSpecialActive = false` (MUST BE IMMEDIATE)
   - `chainVelocity = 0` (MUST RESET)
   - `currentTimeScale = 1.0` (RESTORE TIME)
   - Restore lights/walls
   - `applyGravity()`
   - If no chain, `spawnChain()`

**CRITICAL:** Unfreeze BEFORE `applyGravity()` or chain won't drop

---

## CHARGE SYSTEM

```javascript
// Each character 0-100 charge
zookoCharge, nateCharge, zancasCharge, cyberaxeCharge

// On clear:
if (link.type === ZEC_D) zookoCharge += chargePerLink;
if (link.type === ZEC_A) nateCharge += chargePerLink;
if (link.type === ZEC_C) zancasCharge += chargePerLink;
if (link.type === ZEC_B) cyberaxeCharge += chargePerLink;

// Cap at 100
charge = Math.min(100, charge);

// Activate at 100%
if (charge >= 100) {
  triggerSpecial();
  charge = 0;
}
```

---

## PARTICLE SYSTEM

### Spawn Modes

```javascript
// Camera-relative (special abilities)
spawnParticleEffect('effect.json', 8, 0, 0, {
  // x = distance forward from camera
  // y = vertical offset
  // z = horizontal offset
});

// World coordinates (block destruction)
spawnParticleEffect('effect.json', x+0.5, y+1.0, z+0.5, {
  spawnMode: 'world'
});
```

### Velocity System

```javascript
// Initial velocity (spread randomness)
particle.velocity = random spread

// Per-frame directional movement (constant)
particle.position += velocityDir * deltaTime

// NO ACCELERATION (gravity removed - was buggy)
```

---

## SPECIAL CHAIN TYPES

### Encrypted (5% chance)
- Gray appearance, decrypt over 9 seconds (3 levels)
- Cannot connect until fully decrypted
- Every 3 seconds: level 3 → 2 → 1 → 0 (decrypted)

### Glowing/Broken (3% chance)
- White glowing, pulsing emissive
- Breaks connection chains
- Nate special destroys all (100 pts each)

### Multi-Color (8% chance)
- Each link random color
- Chain length 2-6 links

---

## GAME START

```javascript
function startGame(startingLevel = 1, preFillGrid = false) {
  // Reset grid, score, etc.
  score = (startingLevel - 1) * 1000;
  level = startingLevel;
  
  // Set notifications based on level
  hasShownMultiColorNotification = (startingLevel >= 10);
  hasShownEncryptedNotification = (startingLevel >= 25);
  hasShownGlowingNotification = (startingLevel >= 50);
  
  if (preFillGrid) {
    fillGridWithRandomLinks(); // 3-6 rows, 70% fill
  }
  
  initializeChainQueue();
  updateHUD();
}
```

---

## TIME SCALING

```javascript
let currentTimeScale = 1.0; // Normal
const slowTimeScale = 0.3;  // During specials

// Applied to all physics
const deltaTime = clock.getDelta() * 1000 * currentTimeScale;

// MUST reset to 1.0 after specials complete
```

---

## CRITICAL BUGS FIXED (v0.19.3)

### CyberAxe freeze: Chain wouldn't drop after special
- **Fix:** Set `cyberAxeSpecialActive = false` IMMEDIATELY before `applyGravity()`
- **Fix:** Reset `chainVelocity = 0`
- **Fix:** Restore `currentTimeScale = 1.0` immediately (no setTimeout)

### Fog crash: TypeError accessing scene.fog.color
- **Fix:** Removed all fog references (scene has no fog - indoors)

### Particle offset: zooko_special_link_break too low
- **Fix:** Spawn at y+1.0 instead of y+0.5

---

## FILE STRUCTURE

```
zlock_consensus.html           # Main game (8000+ lines)
particle_editor.html           # Particle editor
CHANGELOG.md                   # Version history
PARTICLE_EDITOR_CHANGELOG.md   # Editor changelog
effect/
  ├── smoke_effects.png        # 1168×784, 8×5 grid
  ├── zooko_special.json
  ├── zooko_special_link_break.json
  └── nate_special.json
people/
  ├── *.glb                    # Character models
  └── *_head_compressed.png    # UI portraits
```

---

## IMPORTANT IMPLEMENTATION RULES

- Special abilities MUST call `applyGravity()` after completion
- CyberAxe MUST unfreeze chain before `applyGravity()`
- Always reset `chainVelocity = 0` after special freezes
- Time scale MUST return to 1.0 after specials
- No fog references - `scene.fog` is null (indoors)
- Particle spawn: camera-relative for specials, world for blocks
- Connection algorithm skips encrypted and glowing links
- Minimum 3 links to clear, flood-fill in 6 directions

---

## FOR AI ASSISTANTS

- **Primary docs:** This README + CHANGELOG.md
- **Ignore:** Any `gpt_part_*.md` files (deleted/outdated)
- **Code location:** All in `zlock_consensus.html`
- **Version:** Update in `<title>` tag and CHANGELOG.md
- **Common pitfall:** Specials that don't call `applyGravity()` leave floating blocks
- **Testing:** Press `+` to charge abilities, CyberAxe needs falling chain

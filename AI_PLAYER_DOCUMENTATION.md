# ZLOCK CHAINER - AI Player Documentation

## Overview
ZLOCK CHAINER features an intelligent AI player system designed for automated gameplay testing, game balance validation, and overnight stress testing. The AI uses a **greedy best-first search** algorithm with sophisticated scoring heuristics to make decisions.

---

## Architecture

### AI State Object
The AI maintains state through the `aiState` object:

```javascript
{
    enabled: false,              // Whether AI is currently active
    nextMoveTime: 0,            // Timestamp for rate-limiting moves
    moveDelay: 100,             // Milliseconds between AI actions
    targetX: null,              // Calculated target X position
    targetZ: null,              // Calculated target Z position
    targetRotation: 0,          // Target rotation (0-3 = 0°, 90°, 180°, 270°)
    hasDecided: false,          // Whether AI has made placement decision
    lastDropTime: 0,            // When the last chain was dropped
    dropDelay: 1000             // 1 second delay between drops
}
```

---

## Decision Making Process

### 1. Evaluation Phase (`aiMakeDecision()`)

When a new chain spawns, the AI evaluates **every possible placement**:
- **6 X positions** × **6 Z positions** × **4 rotations** = **144 total positions**
- Each position is scored using `aiEvaluatePosition(x, z, rotation)`
- The position with the **highest score** is selected

### 2. Position Scoring (`aiEvaluatePosition()`)

Each potential position receives a score based on multiple weighted factors:

#### **A. Critical Game Over Prevention**
```javascript
if (landY >= GRID_HEIGHT - 1) {
    return -100000;  // Absolutely avoid losing
}
```
- **Penalty**: -100,000 points
- **Purpose**: Never place a piece that would reach the top of the grid
- **Priority**: Highest (prevents game over completely)

#### **B. Graduated Height Penalties**
```javascript
if (landY >= GRID_HEIGHT * 0.8) {
    score -= 5000;   // Very dangerous (80%+ full)
} else if (landY >= GRID_HEIGHT * 0.7) {
    score -= 1000;   // Dangerous (70%+ full)
} else if (landY >= GRID_HEIGHT * 0.6) {
    score -= 300;    // Getting risky (60%+ full)
}
```
- **Purpose**: Strong aversion to stacking too high
- **Impact**: Encourages spreading blocks across grid instead of creating towers

#### **C. Available Space Bonus**
```javascript
const availableSpace = GRID_HEIGHT - landY;
score += availableSpace * 50;
```
- **Bonus**: +50 points per available height unit
- **Example**: 10 units of space = +500 points
- **Purpose**: Heavily favor columns with more room to grow

#### **D. Height Distribution Bonus**
```javascript
score += (GRID_HEIGHT - landY) * 30;
```
- **Bonus**: +30 points per available height unit
- **Purpose**: Additional incentive for even distribution across grid
- **Combined with (C)**: Total of +80 per available unit

#### **E. Vertical Match Bonus**
```javascript
if (landY > 0 && grid[x][landY - 1][z] !== null) {
    if (chainType === belowType) {
        score += 75;  // Match directly below
    }
}
```
- **Bonus**: +75 points
- **Purpose**: Create vertical chains for potential combos
- **Note**: Lower than horizontal to encourage spreading patterns

#### **F. Horizontal Match Bonus**
```javascript
neighbors.forEach(([nx, nz]) => {
    if (grid[nx][landY][nz]?.type === fallingChain.type) {
        score += 100;  // Match on each side
    }
});
```
- **Bonus**: +100 points per matching neighbor (max +400 for all 4 sides)
- **Purpose**: Create horizontal matches for combo opportunities
- **Priority**: Highest match bonus (encourages spreading over stacking)

#### **G. Board Clear Opportunity Detection**
```javascript
// Count remaining floor blocks
let floorBlockCount = 0;
for (let gx = 0; gx < GRID_WIDTH; gx++) {
    for (let gz = 0; gz < GRID_DEPTH; gz++) {
        if (grid[gx][0][gz] !== null) {
            floorBlockCount++;
        }
    }
}

// Near board clear (5 or fewer blocks on floor)
if (floorBlockCount > 0 && floorBlockCount <= 5 && lowLevelMatchCount > 0) {
    score += 500;
}

// Very close to board clear (2 or fewer blocks)
if (floorBlockCount > 0 && floorBlockCount <= 2 && landY <= 2) {
    score += 1000;
}
```
- **Bonus**: +500 to +1000 points
- **Purpose**: Recognize that clearing the board awards 10,000 points
- **Activation**: Only when floor is nearly empty (strategic opportunity)
- **Impact**: AI actively pursues board clears when feasible

#### **H. Randomness**
```javascript
score += Math.random() * 5;
```
- **Variation**: ±5 points
- **Purpose**: Add slight unpredictability to prevent robotic patterns
- **Note**: Kept small so survival logic dominates

---

## Execution Phase (`aiExecuteMove()`)

After deciding on a target position, the AI executes moves systematically:

### Move Sequence:
1. **Rotation**: Rotate piece to target orientation (one 90° turn per cycle)
2. **Horizontal Movement**: Move toward target X/Z position (one grid cell per cycle)
3. **Drop**: Once at target position and 1 second has elapsed, trigger drop
   - **Fast Play Mode ON**: Uses `instantDrop` (immediate placement)
   - **Fast Play Mode OFF**: Uses `fastDrop` (accelerated fall)

### Rate Limiting:
- **Normal Speed**: 100ms between actions
- **CyberAxe Special**: 300ms (3× slower during time-slow effect)

---

## Scoring Example

Let's evaluate a position at coordinates (2, 3) with 8 units of available height:

| Factor | Calculation | Score |
|--------|-------------|-------|
| Game Over Check | landY < GRID_HEIGHT - 1 | ✓ Pass |
| Height Penalty | landY = 6 (60%) | -300 |
| Available Space | 8 × 50 | +400 |
| Height Distribution | 8 × 30 | +240 |
| Vertical Match | Match below | +75 |
| Horizontal Matches | 2 neighbors match | +200 |
| Board Clear Bonus | Floor has 3 blocks, low match | +500 |
| Randomness | Random | +3 |
| **TOTAL** | | **+1118** |

---

## AI Behavior Patterns

### Survival Strategy
The AI prioritizes survival through:
1. **Never stacking to the top** (critical -100k penalty)
2. **Avoiding dangerous heights** (graduated penalties)
3. **Seeking empty/short columns** (+80 per available unit)
4. **Distributing blocks evenly** across the grid

### Combo Strategy
The AI creates matches by:
1. **Vertical stacking** (+100 for match below)
2. **Horizontal clustering** (+50 per neighbor)
3. **Balancing** survival vs. score optimization

### Adaptation
- **Early Game**: Focuses on spreading blocks evenly
- **Mid Game**: Balances matches with distribution
- **Late Game**: Prioritizes survival, avoiding high stacks

---

## Special Mechanics

### CyberAxe Time-Slow Integration
```javascript
const effectiveMoveDelay = cyberAxeSpecialActive 
    ? aiState.moveDelay * 3 
    : aiState.moveDelay;
```
- AI slows down 3× during CyberAxe's time manipulation
- Maintains game balance during special abilities

### Tutorial Suppression
```javascript
if (settings.aiEnabled && currentState === GameState.PLAYING) {
    usedAI = true;
    level10NotificationShown = true;
    level20NotificationShown = true;
    level50NotificationShown = true;
    glowingLinksGuideShown = true;
}
```
- All tutorial notifications are auto-dismissed when AI is enabled
- Prevents UI clutter during automated testing

---

## Performance Characteristics

### Computational Cost
- **Positions Evaluated**: 144 per chain (6×6×4)
- **Per Position**: ~15 operations (grid lookups, arithmetic)
- **Total**: ~2,160 operations per decision
- **Impact**: Negligible (< 1ms on modern hardware)

### Play Speed
- **100ms move delay**: ~10 moves/second
- **1s drop delay**: ~60 chains/minute (varies with match clearing)
- **Typical Session**: Can play for hours without issue

---

## Configuration

### User Controls
Located in Settings Panel:

**AI Player Toggle**
- Enables/disables AI player
- Shows 🤖 indicator when active

**AI Fast Play Toggle**
- **ON**: Instant drop (immediate placement)
- **OFF**: Fast drop (accelerated fall)

### Developer Tuning
Key constants in `aiState` object:
```javascript
moveDelay: 100,    // Speed of AI movements (ms)
dropDelay: 1000    // Delay between chain drops (ms)
```

---

## Use Cases

### 1. Overnight Testing
Enable AI with auto-restart to:
- Validate game stability over extended periods
- Test for memory leaks or performance degradation
- Stress-test achievement system

### 2. Balance Testing
Observe AI gameplay to:
- Identify overpowered/underpowered mechanics
- Evaluate difficulty progression
- Test special ability effectiveness

### 3. Visual Demonstrations
Use AI for:
- Recording gameplay footage
- Creating promotional materials
- Demonstrating game mechanics

---

## Known Limitations

### Strategic Depth
- AI doesn't plan multiple moves ahead
- No long-term strategy (purely greedy)
- Doesn't optimize for specific achievements

### Match Optimization
- Doesn't actively seek combo chains
- Only evaluates immediate adjacent matches
- No cascade planning

### Rotation Optimization
- Evaluates all 4 rotations equally
- Doesn't account for asymmetric piece shapes (all pieces are currently symmetric)

---

## Future Improvements

### Potential Enhancements
1. **Look-Ahead**: Evaluate next 2-3 chains for better planning
2. **Combo Detection**: Actively seek cascade opportunities
3. **Achievement Targeting**: Adapt strategy based on achievement progress
4. **Difficulty Scaling**: Adjust aggressiveness based on current level
5. **Multi-Objective Optimization**: Balance survival, score, and style points

### Performance Optimizations
1. **Early Pruning**: Skip evaluation of obviously bad positions
2. **Cached Evaluations**: Remember scores for repeated positions
3. **Incremental Updates**: Only re-evaluate changed grid positions

---

## Conclusion

The ZLOCK CHAINER AI represents a **survival-focused, greedy-search** approach that balances:
- **Primary Goal**: Never lose (avoid game over)
- **Secondary Goal**: Create matches (maximize score)
- **Tertiary Goal**: Maintain variety (slight randomness)

This design makes the AI an effective tool for testing and demonstration while remaining beatable by skilled human players who can plan ahead and execute advanced combo strategies.

---

**Version**: v0.20.92  
**Last Updated**: November 24, 2025  
**Maintained By**: ZLOCK CHAINER Development Team

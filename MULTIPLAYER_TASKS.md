# MULTIPLAYER CO-OP TASKS

## Overview
Add 4-player co-op where the host generates a room code, friends join using that code, each controls one hero, and turns are processed in real-time.

---

## Task List

### ✅ COMPLETED
- (none yet)

### 🚧 TODO

#### 1. Backend Server Setup
- [ ] Extend `zlock_server.py` to include WebSocket support
- [ ] Add room management system
  - [ ] Generate unique 6-character room codes
  - [ ] Store active rooms with host connection, client connections, and game state
  - [ ] Handle client join requests with room code validation
  - [ ] Broadcast state updates to all players in a room
  - [ ] Handle disconnections and cleanup empty rooms

#### 2. Settings Panel Changes
- [ ] Add "Host Multiplayer" section
  - [ ] Button: "Create Room" (generates code, starts hosting)
  - [ ] Display: Current room code (if hosting)
  - [ ] Button: "Change Code" (regenerates code, kicks all clients)
  - [ ] Button: "Stop Hosting" (closes room, returns to solo)
- [ ] Add "Join Multiplayer" section
  - [ ] Text input: Room code entry
  - [ ] Button: "Join Room" (connects to host)
  - [ ] Display: Connection status
  - [ ] Button: "Leave Room" (disconnect from host)

#### 3. Room Code Input on Title Screen
- [ ] Add to bottom right corner
  - [ ] Small text input box (6 characters max)
  - [ ] Button: "Join" next to input
  - [ ] Style to match game aesthetic
  - [ ] Hide when already in a room or hosting

#### 4. Hero Selection Screen
- [ ] Create new modal panel
  - [ ] Show all 4 hero portraits (Zooko, Nate, Zancas, CyberAxe)
  - [ ] Gray out portraits if hero already taken by another player
  - [ ] Click portrait to select hero
  - [ ] Display "Waiting for other players..." until all join
  - [ ] Host can see which players control which heroes
  - [ ] "Start Battle" button (host only, enabled when all players ready)

#### 5. Client-Server Communication
- [ ] Implement WebSocket message types:
  - [ ] `create_room` - Host requests new room
  - [ ] `join_room` - Client requests to join with code
  - [ ] `select_hero` - Player selects their hero
  - [ ] `player_action` - Player submits their action choice
  - [ ] `state_update` - Server broadcasts full game state
  - [ ] `kick_player` - Host kicks a specific player
  - [ ] `skip_turn` - Host skips AFK player's turn
  - [ ] `change_code` - Host generates new room code

#### 6. Battle System Refactoring
- [ ] Split `battleAction()` into:
  - [ ] `sendActionToHost()` - Clients send action to host
  - [ ] `processAction()` - Host validates and executes action locally
  - [ ] `broadcastState()` - Host sends updated state to all clients
- [ ] Update `advanceTurn()`
  - [ ] Check if current hero is controlled by local player
  - [ ] Enable/disable action buttons based on whose turn it is
  - [ ] Display "Waiting for [PlayerName]..." when not your turn
- [ ] Add turn timer (optional)
  - [ ] 30-second countdown per turn
  - [ ] Auto-skip turn if timeout (host decision)

#### 7. Host Controls Panel
- [ ] Create new modal (host only)
  - [ ] List all connected players with their hero names
  - [ ] "Kick" button next to each player
  - [ ] "Skip Turn" button (only enabled during AFK player's turn)
  - [ ] "Change Room Code" button with confirmation
  - [ ] Accessible via new button in pause menu

#### 8. UI Changes During Multiplayer
- [ ] Battle screen updates
  - [ ] Show player names above hero cards (e.g., "ZOOKO (You)")
  - [ ] Gray out action buttons when not your turn
  - [ ] Display "Waiting for [Hero Name]'s turn..." during other players' turns
  - [ ] Add connection status indicator (top right corner)
  - [ ] Show latency ping (optional)

#### 9. State Synchronization
- [ ] Host-authoritative model
  - [ ] Host runs full battle logic locally
  - [ ] Clients only send input and receive state updates
  - [ ] Host sends state after every action: HP changes, turn order, positions, etc.
- [ ] Client-side updates
  - [ ] Receive state from host
  - [ ] Update local `battleState` object
  - [ ] Re-render battle scene
  - [ ] Update hero/enemy cards

#### 10. Disconnection Handling
- [ ] If client disconnects
  - [ ] Host marks hero as "AI-controlled"
  - [ ] AI takes over turns for that hero
  - [ ] Notify other players: "[PlayerName] disconnected - AI taking over"
- [ ] If host disconnects
  - [ ] All clients kicked back to title screen
  - [ ] Show message: "Host disconnected - returning to menu"

#### 11. Error Handling
- [ ] Invalid room code
  - [ ] Display: "Room not found - check code"
- [ ] Room full (4 players already)
  - [ ] Display: "Room full - cannot join"
- [ ] Connection timeout
  - [ ] Auto-kick after 10 seconds of no response
- [ ] Duplicate hero selection
  - [ ] Server rejects, client must pick different hero

#### 12. Testing & Debugging
- [ ] Add debug mode in settings
  - [ ] Toggle: "Show Network Debug Info"
  - [ ] Display: Message log showing all sent/received WebSocket messages
  - [ ] Display: Current room state (players, heroes, turn order)

---

## Implementation Order

1. Backend WebSocket server (Task 1)
2. Settings panel UI (Tasks 2, 3)
3. WebSocket client connection code (Task 5)
4. Hero selection screen (Task 4)
5. Battle system refactoring (Task 6)
6. Host controls panel (Task 7)
7. UI updates for multiplayer (Task 8)
8. State sync logic (Task 9)
9. Disconnection handling (Task 10)
10. Error handling (Task 11)
11. Testing mode (Task 12)

---

## File Changes Summary

- **`zlock_server.py`** - Add WebSocket server, room management
- **`tunnels_of_privacy.html`** - All UI, client WebSocket code, battle refactoring
- **New file: `multiplayer_state.js`** (optional) - Could extract WebSocket logic into separate file for cleanliness

---

## Technical Notes

### Room Code Format
- 6 characters: uppercase letters + digits (e.g., "A3K9Z2")
- Generated server-side to avoid collisions
- Expires when host disconnects or manually changes code

### Network Architecture
- **Host-Authoritative**: Host runs all game logic, clients are "dumb terminals"
- **State Broadcasting**: Host sends full state snapshot after each action
- **Action Submission**: Clients send only their action choice + target info

### Hero Assignment
- First player to join picks first
- Host always controls at least one hero
- Players cannot switch heroes mid-battle

### AI Takeover Rules
- Disconnected player's hero becomes AI-controlled
- Uses same AI logic as enemy AI (closest targeting, random actions)
- If player reconnects, they can reclaim their hero (optional feature)

---

## Future Enhancements (Post-MVP)

- [ ] Voice chat integration
- [ ] Text chat in-game
- [ ] Reconnection support (rejoin same room after disconnect)
- [ ] Spectator mode (5th+ players can watch)
- [ ] Room browser (see all public rooms)
- [ ] Private/public room toggle
- [ ] Friend list system
- [ ] Match history/stats tracking
- [ ] Cross-save between solo and multiplayer

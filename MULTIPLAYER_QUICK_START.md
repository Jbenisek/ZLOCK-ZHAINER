# QUICK START - MULTIPLAYER TESTING

## 1. Install Dependencies
```powershell
pip install websockets
```

## 2. Start Server
```powershell
python zlock_server.py
```
Should see:
```
WebSocket server started on ws://0.0.0.0:8765
Serving HTTP on 0.0.0.0 port 4243 (http://0.0.0.0:4243/) ...
```

## 3. Open 4 Browser Windows
Open these URLs (Ctrl+Click each):
- [Player 1 - HOST](http://localhost:4243/tunnels_of_privacy.html)
- [Player 2 - CLIENT](http://localhost:4243/tunnels_of_privacy.html)
- [Player 3 - CLIENT](http://localhost:4243/tunnels_of_privacy.html)
- [Player 4 - CLIENT](http://localhost:4243/tunnels_of_privacy.html)

## 4. Host Creates Room (Player 1)
1. Click "SETTINGS" (Y button)
2. Scroll to "MULTIPLAYER CO-OP" section
3. Click "CREATE ROOM"
4. Note the 6-character code (e.g., "A3X9K2")

## 5. Clients Join (Players 2-4)
**Option A: Settings Panel**
1. Click "SETTINGS" (Y button)
2. In "Join Game" section, type room code
3. Click "JOIN ROOM"

**Option B: Quick Join (Faster)**
1. On title screen, bottom-right corner
2. Type room code in text box
3. Click "JOIN"

## 6. Select Heroes
- Modal appears for all players
- Each player clicks ONE hero
- Heroes turn gray when taken
- Host waits for all players to select

## 7. Start Battle (Host Only)
- Host clicks "START BATTLE" button
- All players enter battle

## 8. Play Battle
- Watch turn indicator "(YOU)" vs "Waiting for..."
- Only current player's buttons are enabled
- Actions sync automatically

## 9. Enable Debug Mode (If Issues)
1. Click "SETTINGS"
2. Enable "Network Debug" checkbox
3. Debug panel appears top-right
4. Shows connection status, room state, messages

---

## Troubleshooting

### "WebSocket connection failed"
- Make sure server is running
- Check firewall (allow port 8765)
- Try `http://127.0.0.1:4243` instead of localhost

### "Room not found"
- Double-check room code (case-sensitive)
- Make sure host created room first
- Try creating new room

### "Hero already taken"
- Another player selected that hero first
- Choose different hero
- Check debug panel for current selections

### "Not syncing in battle"
- Check debug panel message log
- Verify all clients show same room code
- Host should see state_update messages going out
- Clients should see state_update messages coming in

### Game freezes/lag
- Check browser console (F12) for errors
- Verify WebSocket status in debug panel
- Try refreshing all browsers and rejoining

---

## Quick Test Checklist

- [ ] Server starts without errors
- [ ] Host creates room, gets code
- [ ] 3 clients join with code
- [ ] All players see hero selection modal
- [ ] Each player selects different hero
- [ ] Host clicks START BATTLE
- [ ] Battle screen appears for all players
- [ ] Turn indicator shows correct player
- [ ] Only current player's buttons enabled
- [ ] Actions sync across all clients
- [ ] Next turn advances correctly
- [ ] Try KICK player (host)
- [ ] Try SKIP TURN (host)
- [ ] Try disconnecting client (AI takeover)

---

## Expected Behavior

### When Working Correctly:
- ✅ Host sees room code immediately after CREATE ROOM
- ✅ Clients see "Connected to room: CODE" after joining
- ✅ Hero modal shows which heroes are taken
- ✅ Battle starts simultaneously for all players
- ✅ Turn info updates in real-time
- ✅ No delays or desyncs between clients

### Debug Panel Should Show:
- ✅ Connection Status: "✅ Connected"
- ✅ Room State: Shows role, code, player count
- ✅ Message Log: Updates with each action
- ✅ Arrows: ⬆️ for sent, ⬇️ for received

---

## If Everything Works:
🎉 **CONGRATULATIONS!** The multiplayer system is fully functional!

## If Something Breaks:
1. Check debug panel message log
2. Check browser console (F12)
3. Check server terminal for errors
4. Report issue with:
   - What you did
   - Error message (if any)
   - Debug panel screenshot
   - Server terminal output

---

**Ready to test! Let me know how it goes!** 🚀

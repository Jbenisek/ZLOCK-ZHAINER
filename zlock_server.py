#!/usr/bin/env python3
"""
ZLOCK Web Server with proper MIME types for GLB files
Fixes binary file serving issues on Linux
Includes WebSocket server for multiplayer co-op
"""

import http.server
import socketserver
import mimetypes
import sys
import os
import re
import asyncio
import json
import random
import string
from threading import Thread

try:
    import websockets
except ImportError:
    print("⚠️  WARNING: 'websockets' module not installed!")
    print("Run: pip install websockets")
    print("Multiplayer features will be disabled.\n")
    websockets = None

PORT = 4243
WS_PORT = 8765

# Add proper MIME types for game assets
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('audio/wav', '.wav')
mimetypes.add_type('audio/ogg', '.ogg')
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper binary file support"""
    
    # Increase timeout for large file transfers (videos)
    timeout = 300  # 5 minutes instead of default 60 seconds
    
    def end_headers(self):
        # Add CORS headers for cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Enable aggressive caching for large static assets (models, videos, audio)
        # HTML files: no cache (for development iteration)
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        # Large binary assets: cache for 24 hours (browser stores in memory/disk)
        elif self.path.endswith(('.glb', '.gltf', '.mp4', '.mp3', '.wav', '.ogg', '.png', '.jpg', '.jpeg')):
            self.send_header('Cache-Control', 'public, max-age=86400')  # 24 hours cache
            self.send_header('Expires', 'Thu, 31 Dec 2026 23:59:59 GMT')  # Far future expiry
        else:
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        
        super().end_headers()
    
    def guess_type(self, path):
        """Override to ensure proper binary MIME types"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Force binary for GLB files
        if path.endswith('.glb'):
            return 'model/gltf-binary'
        # Force video/mp4 for MP4 files
        elif path.endswith('.mp4'):
            return 'video/mp4'
        
        return mimetype or 'application/octet-stream'
    
    def do_GET(self):
        """Override to handle Range requests for video streaming"""
        # Check if this is a video file request
        if self.path.endswith('.mp4'):
            return self.send_video_range()
        else:
            return super().do_GET()
    
    def send_video_range(self):
        """Handle HTTP Range requests for video streaming"""
        path = self.translate_path(self.path)
        
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        
        try:
            fs = os.fstat(f.fileno())
            file_len = fs.st_size
            
            # Check for Range header
            range_header = self.headers.get('Range')
            
            if range_header:
                # Parse range header
                match = re.search(r'bytes=(\d+)-(\d*)', range_header)
                if match:
                    start = int(match.group(1))
                    end = int(match.group(2)) if match.group(2) else file_len - 1
                    
                    # Validate range
                    if start >= file_len:
                        self.send_error(416, "Range Not Satisfiable")
                        return None
                    
                    # Clamp end
                    end = min(end, file_len - 1)
                    content_len = end - start + 1
                    
                    # Send 206 Partial Content
                    self.send_response(206)
                    self.send_header('Content-type', 'video/mp4')
                    self.send_header('Content-Range', f'bytes {start}-{end}/{file_len}')
                    self.send_header('Content-Length', str(content_len))
                    self.send_header('Accept-Ranges', 'bytes')
                    self.end_headers()
                    
                    # Send partial content
                    f.seek(start)
                    self.wfile.write(f.read(content_len))
                else:
                    # Invalid range format, send full file
                    self.send_full_video(f, file_len)
            else:
                # No range header, send full file
                self.send_full_video(f, file_len)
        finally:
            f.close()
    
    def send_full_video(self, f, file_len):
        """Send complete video file"""
        self.send_response(200)
        self.send_header('Content-type', 'video/mp4')
        self.send_header('Content-Length', str(file_len))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        self.wfile.write(f.read())
    
    def handle(self):
        """Override to catch BrokenPipeError from client disconnects"""
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):
            # Client disconnected, silently ignore
            pass
    
    def log_message(self, format, *args):
        """Custom logging to show request details"""
        print(f"[{self.log_date_time_string()}] {format % args}")

# ===== MULTIPLAYER WEBSOCKET SERVER =====

# Room storage: { room_code: { 'host': websocket, 'clients': [], 'state': {}, 'heroes': {} } }
rooms = {}

def generate_room_code():
    """Generate unique 6-digit room code (numbers only)"""
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        if code not in rooms:
            return code

async def handle_websocket(websocket, path):
    """Handle WebSocket connections for multiplayer"""
    client_room = None
    client_role = None
    
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get('type')
            
            # CREATE ROOM (host)
            if msg_type == 'create_room':
                room_code = generate_room_code()
                player_id = id(websocket)
                rooms[room_code] = {
                    'host': websocket,
                    'clients': [],
                    'state': {},
                    'heroes': {},  # { hero_name: { 'playerId': id, 'playerName': str } }
                    'players': { player_id: { 'id': player_id, 'name': 'Player 1', 'ws': websocket } }  # All players
                }
                client_room = room_code
                client_role = 'host'
                await websocket.send(json.dumps({
                    'type': 'room_created',
                    'code': room_code,
                    'player_id': player_id,
                    'players': [{ 'id': player_id, 'name': 'Player 1', 'hero': None }]
                }))
                print(f"[WS] Room {room_code} created")
            
            # JOIN ROOM (client)
            elif msg_type == 'join_room':
                room_code = data.get('code', '').upper()
                if room_code not in rooms:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Room not found - check code'
                    }))
                elif len(rooms[room_code]['clients']) >= 3:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': 'Room full - cannot join'
                    }))
                else:
                    rooms[room_code]['clients'].append(websocket)
                    player_id = id(websocket)
                    player_num = len(rooms[room_code]['clients']) + 1
                    player_name = f'Player {player_num}'
                    rooms[room_code]['players'][player_id] = { 'id': player_id, 'name': player_name, 'ws': websocket }
                    client_room = room_code
                    client_role = 'client'
                    
                    # Build current players list
                    players_list = []
                    for pid, pdata in rooms[room_code]['players'].items():
                        hero = None
                        for h, hdata in rooms[room_code]['heroes'].items():
                            if hdata['playerId'] == pid:
                                hero = h
                                break
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'hero': hero })
                    
                    await websocket.send(json.dumps({
                        'type': 'joined',
                        'code': room_code,
                        'player_id': player_id,
                        'players': players_list
                    }))
                    
                    # Broadcast player list update to all
                    broadcast_msg = json.dumps({
                        'type': 'players_update',
                        'players': players_list
                    })
                    await rooms[room_code]['host'].send(broadcast_msg)
                    for client in rooms[room_code]['clients']:
                        if client != websocket:
                            await client.send(broadcast_msg)
                    
                    print(f"[WS] Client joined room {room_code} as {player_name}")
            
            # SELECT HERO
            elif msg_type == 'select_hero':
                if client_room and client_room in rooms:
                    hero_name = data.get('hero')
                    player_name = data.get('playerName', 'Player')
                    player_id = id(websocket)
                    
                    # Check if hero already taken by someone else
                    if hero_name in rooms[client_room]['heroes']:
                        if rooms[client_room]['heroes'][hero_name]['playerId'] != player_id:
                            await websocket.send(json.dumps({
                                'type': 'error',
                                'message': 'Hero already taken'
                            }))
                            continue
                    
                    # Update player name if provided
                    if player_id in rooms[client_room]['players']:
                        rooms[client_room]['players'][player_id]['name'] = player_name
                    
                    # Store hero selection with player info
                    rooms[client_room]['heroes'][hero_name] = {
                        'playerId': player_id,
                        'playerName': player_name
                    }
                    
                    # Build players list with hero arrays
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        heroes = []
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                heroes.append(h)
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'heroes': heroes })
                    
                    # Broadcast hero selection to all in room
                    msg = json.dumps({
                        'type': 'hero_selected',
                        'hero': hero_name,
                        'player_id': player_id,
                        'heroes': rooms[client_room]['heroes'],
                        'players': players_list
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # DESELECT HERO
            elif msg_type == 'deselect_hero':
                if client_room and client_room in rooms:
                    hero_name = data.get('hero')
                    player_id = id(websocket)
                    
                    # Remove hero if owned by this player
                    if hero_name in rooms[client_room]['heroes']:
                        if rooms[client_room]['heroes'][hero_name]['playerId'] == player_id:
                            del rooms[client_room]['heroes'][hero_name]
                    
                    # Build players list with hero arrays
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        heroes = []
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                heroes.append(h)
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'heroes': heroes })
                    
                    # Broadcast update
                    msg = json.dumps({
                        'type': 'hero_selected',
                        'heroes': rooms[client_room]['heroes'],
                        'players': players_list
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # UPDATE PLAYER NAME
            elif msg_type == 'update_name':
                if client_room and client_room in rooms:
                    player_id = id(websocket)
                    player_name = data.get('playerName', 'Player')
                    
                    # Update player name
                    if player_id in rooms[client_room]['players']:
                        rooms[client_room]['players'][player_id]['name'] = player_name
                    
                    # Update hero if player has one selected
                    for hero, hdata in rooms[client_room]['heroes'].items():
                        if hdata['playerId'] == player_id:
                            hdata['playerName'] = player_name
                            break
                    
                    # Build players list
                    players_list = []
                    for pid, pdata in rooms[client_room]['players'].items():
                        hero = None
                        for h, hdata in rooms[client_room]['heroes'].items():
                            if hdata['playerId'] == pid:
                                hero = h
                                break
                        players_list.append({ 'id': pid, 'name': pdata['name'], 'hero': hero })
                    
                    # Broadcast players update
                    msg = json.dumps({
                        'type': 'players_update',
                        'players': players_list,
                        'heroes': rooms[client_room]['heroes']
                    })
                    await rooms[client_room]['host'].send(msg)
                    for client in rooms[client_room]['clients']:
                        await client.send(msg)
            
            # PLAYER ACTION (client sends to host)
            elif msg_type == 'player_action':
                if client_room and client_room in rooms:
                    # Forward action to host
                    await rooms[client_room]['host'].send(json.dumps(data))
            
            # STATE UPDATE (host broadcasts to clients)
            elif msg_type == 'state_update':
                if client_room and client_room in rooms and client_role == 'host':
                    rooms[client_room]['state'] = data.get('state', {})
                    # Broadcast to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # KICK PLAYER (host only)
            elif msg_type == 'kick_player':
                if client_room and client_room in rooms and client_role == 'host':
                    player_id = data.get('player_id')
                    for client in rooms[client_room]['clients'][:]:
                        if id(client) == player_id:
                            await client.send(json.dumps({
                                'type': 'kicked',
                                'message': 'You were kicked by the host'
                            }))
                            await client.close()
                            rooms[client_room]['clients'].remove(client)
            
            # SKIP TURN (host only)
            elif msg_type == 'skip_turn':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast skip to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
            
            # GAME START (host only)
            elif msg_type == 'game_start':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast game start to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host started game in room {client_room}: {data.get('mode', 'unknown')}")
            
            # BATTLE INIT (host only)
            elif msg_type == 'battle_init':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast battle initialization to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent battle_init to room {client_room}")
            
            # BATTLE END (host only)
            elif msg_type == 'battle_end':
                if client_room and client_room in rooms and client_role == 'host':
                    # Broadcast battle end to all clients
                    for client in rooms[client_room]['clients']:
                        await client.send(message)
                    print(f"[WS] Host sent battle_end to room {client_room}: {data.get('reason', 'unknown')}")
            
            # CHANGE CODE (host only)
            elif msg_type == 'change_code':
                if client_room and client_room in rooms and client_role == 'host':
                    # Kick all clients
                    for client in rooms[client_room]['clients'][:]:
                        await client.send(json.dumps({
                            'type': 'kicked',
                            'message': 'Host changed room code'
                        }))
                        await client.close()
                    # Generate new code
                    new_code = generate_room_code()
                    rooms[new_code] = rooms.pop(client_room)
                    rooms[new_code]['clients'] = []
                    client_room = new_code
                    await websocket.send(json.dumps({
                        'type': 'code_changed',
                        'code': new_code
                    }))
                    print(f"[WS] Room code changed to {new_code}")
    
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[WS] Error: {e}")
    finally:
        # Cleanup on disconnect
        if client_room and client_room in rooms:
            if client_role == 'host':
                # Host disconnected - kick all clients and delete room
                for client in rooms[client_room]['clients']:
                    try:
                        await client.send(json.dumps({
                            'type': 'host_disconnected',
                            'message': 'Host disconnected - returning to menu'
                        }))
                        await client.close()
                    except:
                        pass
                del rooms[client_room]
                print(f"[WS] Room {client_room} closed (host disconnect)")
            elif websocket in rooms[client_room]['clients']:
                # Client disconnected
                rooms[client_room]['clients'].remove(websocket)
                # Notify host
                try:
                    await rooms[client_room]['host'].send(json.dumps({
                        'type': 'player_disconnected',
                        'player_id': id(websocket)
                    }))
                except:
                    pass
                print(f"[WS] Client disconnected from room {client_room}")

async def start_websocket_server():
    """Start WebSocket server for multiplayer"""
    if websockets is None:
        print("[WS] WebSocket server disabled (module not installed)")
        return
    
    async with websockets.serve(handle_websocket, "0.0.0.0", WS_PORT):
        print(f"[WS] WebSocket server started on ws://0.0.0.0:{WS_PORT}")
        await asyncio.Future()  # Run forever

def run_websocket_server():
    """Run WebSocket server in asyncio event loop"""
    asyncio.run(start_websocket_server())

# ===== END WEBSOCKET SERVER =====

def main():
    print(f"Starting ZLOCK Game Server on port {PORT}...")
    print(f"Binary MIME types configured for .glb, .gltf, audio files")
    print(f"Server URL: http://0.0.0.0:{PORT}/zlock_consensus.html")
    if websockets:
        print(f"WebSocket server will start on ws://0.0.0.0:{WS_PORT}")
    print(f"Press Ctrl+C to stop\n")
    
    # Start WebSocket server in separate thread
    if websockets:
        ws_thread = Thread(target=run_websocket_server, daemon=True)
        ws_thread.start()
    
    # Enable address reuse to prevent "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    
    # Increase request queue size for handling multiple simultaneous video requests
    # Safe to set high for local dev - allows browser to queue all 4 videos + assets at once
    socketserver.TCPServer.request_queue_size = 50
    
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", PORT), GameHTTPRequestHandler)
        
        # Set socket timeout to prevent hanging connections
        httpd.socket.settimeout(300)  # 5 minute socket timeout
        
        print(f"Server successfully bound to port {PORT}")
        print(f"Server is now running and accepting connections...\n")
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\n❌ ERROR: Port {PORT} is already in use!")
            print(f"Run: sudo lsof -ti:{PORT} | xargs sudo kill -9")
            print(f"Or use a different port.\n")
            sys.exit(1)
        else:
            print(f"\n❌ ERROR: Failed to start server: {e}\n")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        httpd.server_close()
        print("Server stopped cleanly.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

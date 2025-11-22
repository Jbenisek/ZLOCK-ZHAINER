#!/usr/bin/env python3
"""
ZLOCK Web Server with proper MIME types for GLB files
Fixes binary file serving issues on Linux
"""

import http.server
import socketserver
import mimetypes
import sys
import os
import re

PORT = 4243

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

def main():
    print(f"Starting ZLOCK Game Server on port {PORT}...")
    print(f"Binary MIME types configured for .glb, .gltf, audio files")
    print(f"Server URL: http://0.0.0.0:{PORT}/zlock_consensus.html")
    print(f"Press Ctrl+C to stop\n")
    
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

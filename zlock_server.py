#!/usr/bin/env python3
"""
ZLOCK Web Server with proper MIME types for GLB files
Fixes binary file serving issues on Linux
"""

import http.server
import socketserver
import mimetypes
import sys

PORT = 4243

# Add proper MIME types for game assets
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('audio/wav', '.wav')
mimetypes.add_type('audio/ogg', '.ogg')
mimetypes.add_type('image/png', '.png')
mimetypes.add_type('image/jpeg', '.jpg')
mimetypes.add_type('image/jpeg', '.jpeg')

class GameHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler with proper binary file support"""
    
    def end_headers(self):
        # Add CORS headers for cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Disable caching for development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def guess_type(self, path):
        """Override to ensure proper binary MIME types"""
        mimetype, encoding = mimetypes.guess_type(path)
        
        # Force binary for GLB files
        if path.endswith('.glb'):
            return 'model/gltf-binary'
        
        return mimetype or 'application/octet-stream'
    
    def log_message(self, format, *args):
        """Custom logging to show request details"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    print(f"Starting ZLOCK Game Server on port {PORT}...")
    print(f"Binary MIME types configured for .glb, .gltf, audio files")
    print(f"Server URL: http://0.0.0.0:{PORT}/zlock_consensus.html")
    print(f"Press Ctrl+C to stop\n")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), GameHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()
            print("Server stopped.")
            sys.exit(0)

if __name__ == "__main__":
    main()

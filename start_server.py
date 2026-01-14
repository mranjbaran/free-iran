"""
Simple HTTP server for serving the Iran Solidarity PLZ-to-MP Finder frontend
Serves static files from the static/ directory
"""

import http.server
import socketserver
import os

# Change to the static directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
os.chdir(static_dir)

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

print("="*70)
print("🇮🇷 FREE IRAN - PLZ-TO-MP FINDER")
print("="*70)
print(f"\nStarting server on http://localhost:{PORT}")
print(f"\nOpen this URL in your browser:")
print(f"  → http://localhost:{PORT}/index.html")
print(f"\nPress Ctrl+C to stop the server")
print("="*70)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

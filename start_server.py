"""
Simple HTTP server to serve the HTML and JSON files
This solves CORS issues when loading JSON locally
"""

import http.server
import socketserver
import os

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

print("="*70)
print("BUNDESTAG FINDER - LOCAL SERVER")
print("="*70)
print(f"\nStarting server on http://localhost:{PORT}")
print(f"\nOpen this URL in your browser:")
print(f"  → http://localhost:{PORT}/bundestag_finder.html")
print(f"\nPress Ctrl+C to stop the server")
print("="*70)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

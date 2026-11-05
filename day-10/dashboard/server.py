"""Tiny local server for the Day 10 static dashboard and exported reports."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)

class DashboardHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Keep all served paths anchored inside day-10.
        clean = path.split("?", 1)[0].lstrip("/")
        candidate = (ROOT / clean).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            return str(ROOT / "__not_found__")
        return str(candidate)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if __name__ == "__main__":
    host, port = "127.0.0.1", 8000
    print("Student ML Intelligence dashboard")
    print(f"Open http://{host}:{port}/dashboard/")
    print("Press Ctrl+C to stop.")
    ThreadingHTTPServer((host, port), DashboardHandler).serve_forever()

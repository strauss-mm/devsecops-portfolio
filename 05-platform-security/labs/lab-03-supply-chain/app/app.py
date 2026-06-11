"""Simple Flask app for supply chain security lab."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {
            "app": "supply-chain-lab",
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "signed": True,
            "sbom_attached": True,
        }
        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Starting server on :8080")
    server.serve_forever()

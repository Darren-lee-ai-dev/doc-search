"""Local-only HTTP interface. Uploaded text is processed in memory, never saved."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from search import search

MAX_BYTES = 2_000_000

class Handler(BaseHTTPRequestHandler):
    def respond(self, status, data, kind='application/json'):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != '/':
            return self.respond(404, {'error': 'Not found'})
        self.respond(200, Path(__file__).with_name('index.html').read_bytes(), 'text/html; charset=utf-8')

    def do_POST(self):
        if self.path != '/search':
            return self.respond(404, {'error': 'Not found'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= MAX_BYTES:
                return self.respond(413, {'error': 'Request must be under 2 MB.'})
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError()
            docs, query = data.get('documents'), data.get('query')
            if not isinstance(query, str) or not query.strip() or len(query) > 500:
                raise ValueError()
            if not isinstance(docs, list) or not 1 <= len(docs) <= 10:
                raise ValueError()
            if any(not isinstance(d, dict) or not isinstance(d.get('name'), str) or not isinstance(d.get('text'), str) for d in docs):
                raise ValueError()
            self.respond(200, {'results': search(docs, query)})
        except (ValueError, UnicodeDecodeError):
            self.respond(400, {'error': 'Provide 1–10 text documents and a query of 1–500 characters.'})

if __name__ == '__main__':
    print('Open http://127.0.0.1:8000 — Ctrl+C to stop')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()

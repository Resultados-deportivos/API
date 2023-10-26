import http.server
import socketserver
import json

# Define the request handler
class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='text/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        # Handle GET requests
        self._set_response()
        response = {'message': 'Hello, this is a simple API! (GET)'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        # Handle POST requests
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        # You can process the data here as needed
        response = {'message': 'Hello, this is a simple API! (POST)', 'data_received': post_data}

        self._set_response()
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Define the server parameters
host = 'localhost'
port = 8000

# Create and start the server
with socketserver.TCPServer((host, port), MyHandler) as httpd:
    print(f'Serving at http://{host}:{port}')
    httpd.serve_forever()

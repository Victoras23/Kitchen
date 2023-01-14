from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import queue

class Kitchen(BaseHTTPRequestHandler):
    shared_resource = queue.Queue() # or stack.LifoQueue()

    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        if self.path == '/consume':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            # Consume data and populate shared resource
            shared_resource.put(data)
            self._send_response('Data consumed')
        else:
            self._send_response('Invalid request')

    def consume_data():
        while True:
            data = shared_resource.get()
            # Extract one element from shared resource and send back to Server 1
            self.send_to_server1(data)
            shared_resource.task_done()

    def send_to_server1(self, data):
        # Send data to Server 1 over HTTP
        print("sending")
        conn = http.client.HTTPConnection('server1:8000')
        conn.request("POST", "/receive", json.dumps(data))

def run():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, Kitchen)
    print('Starting consumer server...')
    httpd.serve_forever()

run()
import json
import os
import socket
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse


# HTTP Handler
class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/':
            self.send_html_response('index.html')
        elif path == '/style.css':
            self.send_css_response('style.css')
        elif path == '/logo.png':
            self.send_image_response('logo.png')
        elif path == '/message.html':
            self.send_html_response('message.html')
        else:
            self.send_error_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        socket_client = SocketClient()
        socket_client.send_data(post_data)

        self.send_response(303)
        self.send_header('Location', '/message.html')
        self.end_headers()

    def send_html_response(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_css_response(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_image_response(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_error_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('error.html', 'rb') as file:
            self.wfile.write(file.read())


# Socket Client
class SocketClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        self.socket.sendto(data, (self.host, self.port))


# Socket Server
class SocketServer:
    def __init__(self, host='', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))

    def receive_data(self):
        while True:
            data, address = self.socket.recvfrom(1024)
            try:
                data = data.decode("utf-8")
                data_dict = {}

                for query in data.split("&"):
                    if "=" in query:
                        data_dict[query.split("=")[0]] = query.split("=")[1]
                    else:
                        data_dict[query] = None

                self.save_data(data_dict)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    def save_data(self, data_dict):
        filename = 'storage/data.json'

        timestamp = str(datetime.now())

        new_entry = {
            timestamp: {
                "username": data_dict["username"],
                "message": data_dict["message"]
            }
        }

        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                data.update(new_entry)
        except FileNotFoundError:
            data = new_entry

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def start(self):
        print(f'Starting socket server on {self.host}:{self.port}...')
        self.receive_data()


# Main Function
if __name__ == '__main__':
    # Start HTTP Server
    http_server = HTTPServer(('localhost', 3000), HttpHandler)
    http_thread = threading.Thread(target=http_server.serve_forever)
    http_thread.daemon = True
    http_thread.start()

    # Start Socket Server
    socket_server = SocketServer()
    socket_thread = threading.Thread(target=socket_server.start)
    socket_thread.daemon = True
    socket_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        http_server.shutdown()

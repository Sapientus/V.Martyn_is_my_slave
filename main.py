from http.server import HTTPServer, BaseHTTPRequestHandler  # import necessary modules
import urllib.parse
from mimetypes import guess_type as d
from pathlib import Path
import socket
import json
from threading import Thread
from datetime import datetime

# Here I ordered to my slave Volodya Martyn to name constants
HTTP_IP = "0.0.0.0"
HTTP_PORT = 3000
SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # Here my handsome slave indicates the path
        div_url = urllib.parse.urlparse(self.path)
        if div_url.path == "/":
            self.send_html_file("index.html")
        if div_url.path == "/message":
            self.send_html_file("message.html")
        else:
            if Path().joinpath(div_url.path[1:]).exists():
                self.static_handler()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_sock.sendto(data, (SOCKET_IP, SOCKET_PORT))
        client_sock.close()
        self.send_response(302)
        self.send_header("location", "/")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def static_handler(self):
        # My slave likes to observe beauty by eyes, and static handler allows it for us.
        self.send_response(200)
        mt = d(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def saving(data, db):
    parse_data = urllib.parse.unquote_plus(data.decode()).replace("\r\n", "\n")
    try:
        # Here my slaves made a structure for out future dict
        parse_dict = {
            key: value
            for key, value in [el.split("=", 1) for el in parse_data.split("&", 1)]
        }
        # I don't remember what exactly happened here, it seems like this reads and loads all recieved messages, classifying them by time
        with open(db, "r", encoding="utf-8") as file:
            load_dict = json.load(file)
            load_dict[datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")] = parse_dict
        with open(db, "w", encoding="utf-8") as file:
            json.dump(load_dict, file, ensure_ascii=False, indent=4)
    except (ValueError, OSError) as error:
        print(error)


def run_socket(host, port, db):
    # Our socket server to work with messages
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_server.bind((host, port))
    try:
        while True:
            data, *_ = socket_server.recvfrom(1024)
            saving(data, db)
    finally:
        socket_server.close()


def run(host, port):
    # My slave worked hard under the Sun in order to create this http server that actually provides our work
    httpserver = HTTPServer((host, port), HttpHandler)
    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        httpserver.server_close()


def main():
    # this sh*t didn't want to work so I made my slave to solve it.
    db = Path(__file__).resolve().parent / "storage" / "data.json"
    if not db.parent.exists():
        db.parent.mkdir(parents=True, exist_ok=True)
    if not db.exists() or not db.stat().st_size:
        with open(db, "w", encoding="utf-8") as fh:
            json.dump({}, fh)
    server_http = Thread(target=run, args=(HTTP_IP, HTTP_PORT))
    server_http.start()
    server_socket = Thread(target=run_socket, args=(SOCKET_IP, SOCKET_PORT, db))
    server_socket.start()


if __name__ == "__main__":
    main()
    # Actually this all is a joke and I don't have real slaves, except you know who :)

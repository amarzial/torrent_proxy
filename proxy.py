import http.server
import socketserver
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import unquote_to_bytes
from urllib.parse import urlencode


class MyProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        parsed_url = urlparse(url)
        args = {p[0]: unquote_to_bytes(p[1])
                for p in [x.split("=") for x in parsed_url.query.split("&")]}

        # sovrascrivo alcune info
        args["downloaded"] = 0
        args["left"] = 0
        args["peer_id"] = 'bt123456789012345678'
        parsed_url = parsed_url._replace(query=urlencode(args))
        url = urlunparse(parsed_url)
        print(url)

        self.send_response(200)
        self.end_headers()
        self.copyfile(urllib.request.urlopen(url), self.wfile)


PORT = 7777

httpd = None

try:
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('', PORT), MyProxy)
    print(f"Proxy at: http://localhost:{PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Pressed Ctrl+C")
finally:
    if httpd:
        httpd.shutdown()

import sys
import cgi
import os
from subprocess import run
from http.server import HTTPServer, SimpleHTTPRequestHandler

class QrServer(SimpleHTTPRequestHandler):
    """
    Python HTTP Server that handles GET and POST requests

    """
    
    QR_FORM_PATH = "./templates/qr_form.html"

    def do_GET(self):
        try:
            with open(self.QR_FORM_PATH) as f:
                template = f.read()
        except Exception as ex:
            template = ex

        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes(template, "utf-8"))

    def do_POST(self):
        if self.path == '/update_qr':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                qr_url = fields.get("qr_url")[0]
                run(["python", "/usr/app/update-display.py", "--qr", qr_url])
                html = f"<html><head></head><body><h3>Success!!!</h3></body></html>"
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))

if __name__ == "__main__":
    HOST_NAME = os.environ["HOST_NAME"] if "HOST_NAME" in os.environ else '0.0.0.0'
    PORT = os.environ["PORT"] if "PORT" in os.environ else 80

    server = HTTPServer((HOST_NAME, PORT), QrServer)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)

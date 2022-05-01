# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpServer(BaseHTTPRequestHandler):
    def __init__(self, port):
        self.port = port
        return

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>안녕하세요</h1>'.encode('utf-8'))
        return

    def run(self):
        httpd = HTTPServer('0.0.0.0', self.port), HttpServer)
        httpd.serve_forever()
        return

def main():
    hs = HttpServer(9999)
    return

if __name__ == '__main__':
    main()

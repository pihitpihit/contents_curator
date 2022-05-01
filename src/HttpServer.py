# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer

class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>안녕하세요</h1>'.encode('utf-8'))
        return

def main():
    httpd = HTTPServer(('0.0.0.0', 8888), HttpServer)
    httpd.serve_forever()
    return

if __name__ == '__main__':
    main()

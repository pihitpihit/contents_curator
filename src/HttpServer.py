#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from Daemonize import Daemon

class HttpServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>안녕하세요</h1>'.encode('utf-8'))
        return

    def do_POST(self):
        contentLength = self.contentLength()
        data = self.data()

        print('[do_POST] path          = %s' % self.path)
        print('[do_POST] contentLength = %d' % contentLength)
        print('[do_POST] data          = %s' % data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        dataRes = (json.dumps(self.helloWorldResponse()) + '\n').encode('utf-8')
        self.wfile.write(dataRes)
        return

    def contentLength(self):
        return int(self.headers.get('Content-Length'))

    def data(self):
        return json.loads(self.rfile.read(self.contentLength()))

    def helloWorldResponse(self):
        dictRes = {}
        dictRes['version'] = '1.0'
        dictRes['data'] = {
            'msg': 'Hello Eightanium'
        }
        return dictRes

class HttpServer(Daemon):
    def __init__(self, name = 'HttpServer'):
        Daemon.__init__(self, name)
        return

    def run(self):
        httpd = HTTPServer(('0.0.0.0', 8888), HttpServerHandler)
        httpd.serve_forever()
        return

def main(argv):
    daemon = HttpServer()
    daemon.main(argv)
    return

if __name__ == '__main__':
    main(sys.argv)

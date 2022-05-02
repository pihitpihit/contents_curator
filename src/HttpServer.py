#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import os
import json
import importlib
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from Daemonize import Daemon
from ChangeMonitor import ChangeMonitor

class HttpServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>안녕하세요</h1>'.encode('utf-8'))
        return

    def do_POST(self):
        contentLength = self.ContentLength()
        data = self.Data()

        print('[do_POST] path          = %s' % self.path)
        print('[do_POST] contentLength = %d' % contentLength)
        print('[do_POST] data          = %s' % data)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        dataRes = (json.dumps(self.HelloWorldResponse()) + '\n').encode('utf-8')
        self.wfile.write(dataRes)
        return

    def ContentLength(self):
        return int(self.headers.get('Content-Length'))

    def Data(self):
        return json.loads(self.rfile.read(self.ContentLength()))

    def HelloWorldResponse(self):
        dictRes = {}
        dictRes['version'] = '1.0'
        dictRes['data'] = {
            'msg': 'Hello Eightanium3'
        }
        return dictRes

class HttpServer(Daemon):
    def __init__(self, name = 'HttpServer'):
        self.stopOnModified = False
        self.monitor = ChangeMonitor()
        Daemon.__init__(self, name)
        return

    def StopOnModified(self, listFile):
        for path in listFile:
            self.monitor.Add(path)
        self.stopOnModified = True
        return

    def ChangeMonitor(self):
        self.monitor.Run()
        self.httpd.shutdown()
        return

    def Run(self):
        if self.stopOnModified:
            monitorThread = threading.Thread(target=self.ChangeMonitor)
            monitorThread.start()

        self.httpd = HTTPServer(('0.0.0.0', 8888), HttpServerHandler)
        self.httpd.serve_forever()

        if self.stopOnModified:
            monitorThread.join()
        return

if __name__ == '__main__':
    daemon = HttpServer()
    daemon.StopOnModified([
        os.path.join('.', 'HttpServer.py'),
    ])
    daemon.Main(argv)

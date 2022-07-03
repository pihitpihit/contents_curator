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
import Util

class HttpServerHandler(BaseHTTPRequestHandler):
    name = "DefaultHttpServer"
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>안녕하세요</h1>'.encode('utf-8'))
        return

    def do_POST(self):
        self.requestJson = None
        contentLength = self.ContentLength()
        data = self.GetRequestJson()

        print('[do_POST] path          = %s' % self.path)
        print('[do_POST] contentLength = %d' % contentLength)
        print('[do_POST] data          = %s' % data)

        try:
            dictRes = self.MakeResponse()
            jsonRes = (json.dumps(dictRes) + '\n').encode('utf-8')

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            self.wfile.write(jsonRes)
            #print('[do_POST][RESPONSE]', dictRes)

        except:
            self.send_response(500)
            print('[do_POST][RESPONSE] Error 500')
            raise

        #finally:
        #    print('[do_POST] dictRes       = %s' % Util.DictToPretty(dictRes))

        return

    def ContentLength(self):
        return int(self.headers.get('Content-Length'))

    def GetRequestJson(self):
        if self.requestJson is None:
            self.requestJson = json.loads(self.rfile.read(self.ContentLength()))
        return self.requestJson

    def MakeResponse(self):
        return self.HelloWorldMessage()

    def HelloWorldMessage(self):
        return 'Hello Eightanium'

class HttpServer(Daemon):
    def __init__(self, handler = None):
        self.stopOnModified = False
        self.monitor = ChangeMonitor()
        self.handler = handler

        if self.handler is None:
            self.handler = HttpServerHandler

        Daemon.__init__(self, self.handler.name)
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

        self.httpd = HTTPServer(('0.0.0.0', 8888), self.handler)
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
from HttpServer import HttpServer
from KakaoBotHandler import KakaoBotHandler


if __name__ == '__main__':
    try:
        daemon = HttpServer(KakaoBotHandler)
        daemon.StopOnModified([
            os.path.join('.', 'HttpServer.py'),
            os.path.join('.', 'ChangeMonitor.py'),
            os.path.join('.', 'BotServer.py'),
            os.path.join('.', 'KakaoBotHandler.py'),
            os.path.join('.', 'Util.py'),
        ])
        daemon.Main(sys.argv)
    except SyntaxError as e:
        time.sleep(1)
        raise e

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
from HttpServer import HttpServer
from ContentsCuratorHandler import ContentsCuratorHandler


if __name__ == '__main__':
    try:
        daemon = HttpServer(ContentsCuratorHandler)
        daemon.StopOnModified([
            os.path.join('.', 'ChangeMonitor.py'),
            os.path.join('.', 'Daemonize.py'),
            os.path.join('.', 'Util.py'),
            os.path.join('.', 'HttpServer.py'),
            os.path.join('.', 'BotServer.py'),
            os.path.join('.', 'KakaoBotHandler.py'),
            os.path.join('.', 'KakaoBotButton.py'),
            os.path.join('.', 'KakaoBotOutput.py'),
            os.path.join('.', 'ContentsCuratorHandler.py'),
        ])
        daemon.Main(sys.argv)
    except SyntaxError as e:
        time.sleep(1)
        raise e

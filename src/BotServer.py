#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import HttpServer


if __name__ == '__main__':
    try:
        daemon = HttpServer.HttpServer()
        daemon.StopOnModified([
            os.path.join('.', 'HttpServer.py'),
            os.path.join('.', 'ChangeMonitor.py'),
            os.path.join('.', 'BotServer.py'),
        ])
        daemon.Main(sys.argv)
    except SyntaxError as e:
        time.sleep(1)
        raise e

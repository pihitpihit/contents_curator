# -*- coding: utf-8 -*-

import os
import sys
import time
import hashlib
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class ChangeMonitor:
    def __init__(self):
        self.dictPath = {}
        self.cv = threading.Condition()
        return

    def Add(self, path: str):
        absPath = os.path.abspath(path)
        if not os.path.exists(absPath):
            raise ValueError('path is not exists.')
        if absPath in self.dictPath:
            raise ValueError('path is already registered.')
        self.dictPath[absPath] = self.GetFileInfo(absPath)
        return

    def OnCreated(self, event):
        pass

    def OnDeleted(self, event):
        pass

    def OnModified(self, event):
        path = os.path.abspath(event.src_path)
        if path not in self.dictPath:
            return
        if self.GetFileSize(path) == 0:
            return

        info  = self.GetFileInfo(path)
        if self.dictPath[path] == info:
            return

        print('MODIFIED:' , path)
        #print('\t-  md5 = ', info[0])
        #print('\t- size = ', info[1])

        self.dictPath[path] = info
        self.cv.acquire()
        self.cv.notify()
        self.cv.release()
        return

    def OnMoved(self, event):
        pass

    def GetFileSize(self, path):
        return os.path.getsize(path)

    def GetFileMd5(self, data):
        return hashlib.md5(data).hexdigest()

    def GetFileInfo(self, path):
        try:
            with open(path, 'rb') as f:
                return (self.GetFileMd5(f.read()), self.GetFileSize(path))
        except:
            return (None, None)

    def Run(self):
        patterns = ['*']
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(
                               patterns,
                               ignore_patterns,
                               ignore_directories,
                               case_sensitive
                           )

        my_event_handler.on_created = self.OnCreated
        my_event_handler.on_deleted = self.OnDeleted
        my_event_handler.on_modified = self.OnModified
        my_event_handler.on_moved = self.OnMoved

        path = '.'
        recursive = True
        observer = Observer()
        observer.schedule(my_event_handler, path, recursive)

        observer.start()
        try:
            self.cv.acquire()
            self.cv.wait()
            self.cv.release()
        except KeyboardInterrupt:
            pass
        finally:
            observer.stop()
            observer.join()
        return

if __name__ == '__main__':
    cd = ChangeMonitor()
    cd.Add(os.path.join('.', 'ChangeMonitor.py'))
    cd.Add(os.path.join('.', 'HttpServer.py'))
    cd.Run()

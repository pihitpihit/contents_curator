# -*- coding: utf-8 -*-

import sys
import os
import daemon
import time
from abc import *
from daemon import pidfile
from daemon import DaemonContext

class Daemon(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        self.pidPath = os.path.join(os.getcwd(), '%s.pid' % self.name)
        self.pidLockFile = pidfile.PIDLockFile(self.pidPath)
        return

    def WaitForUnlock(self):
        time.sleep(0.1)
        count = 0
        while True:
            if self.pidLockFile.is_locked():
                print('%s daemon - wait for refresh (try:%d)' % (self.name, count))
                time.sleep(0.5)
                count += 1
            else:
                if 0 < count:
                    print('%s daemon - unlocked' % self.name)
                break
        return

    @abstractmethod
    def Run(self):
        pass

    def Start(self):
        if self.pidLockFile.is_locked():
            print(
                '%s deamon is already running (pid:%d)' % (
                    self.name,
                    self.pidLockFile.read_pid()
                )
            )
            return

        print('%s daemon - start' % self.name)
        with daemon.DaemonContext(pidfile = self.pidLockFile):
            self.Run()
        return

    def Stop(self):
        if self.pidLockFile.is_locked():
            os.system('kill %d' % self.pidLockFile.read_pid())
            print('%s daemon - stopped' % self.name)
        else:
            print('%s daemon - not running' % self.name)
        return

    def Restart(self):
        self.stop()
        self.WaitForUnlock()
        self.start()
        return

    def Main(self, argv):
        op = None
        if 2 <= len(argv):
            op = argv[1]

        if op == 'start':
            self.Start()
        elif op == 'stop':
            self.Stop()
        elif op == 'restart':
            self.Restart()
        elif op == 'block':
            self.Run()
        else:
            print('[Error] Unknown operation.')
            self.Usage()
        return

    def Usage(self):
        print('Usage:')
        print('\tstart')
        print('\tstop')
        print('\trestart')
        print('\tblock')
        print()

if __name__ == '__main__':
    class TestDaemon2(Daemon):
        def __init__(self):
            Daemon.__init__(self, 'TestDaemon2')
            return

        def Run(self):
            while True:
                os.system('echo BB >> /home/pihit/workspace/contents_curator/src/test.txt')

    if True:
        d = TestDaemon2()
    else:
        d = Daemon('TestDaemon')
    d.Main(sys.argv)

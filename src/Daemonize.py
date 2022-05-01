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

    def waitForUnlock(self):
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
    def run(self):
        pass

    def start(self):
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
            self.run()
        return

    def stop(self):
        if self.pidLockFile.is_locked():
            os.system('kill %d' % self.pidLockFile.read_pid())
            print('%s daemon - stopped' % self.name)
        else:
            print('%s daemon - not running' % self.name)
        return

    def restart(self):
        self.stop()
        self.waitForUnlock()
        self.start()
        return

    def main(self, argv):
        if len(argv) < 2:
            self.usage()
            return

        op = argv[1]
        if op == 'start':
            self.start()
        elif op == 'stop':
            self.stop()
        elif op == 'restart':
            self.restart()
        else:
            print('[Error] Unknown operation.')
            self.usage()
        return

    def usage(self):
        print('Usage:')
        print('\tstart')
        print('\tstop')
        print('\trestart')
        print()

if __name__ == '__main__':
    class TestDaemon2(Daemon):
        def __init__(self):
            Daemon.__init__(self, 'TestDaemon2')
            return

        def run(self):
            while True:
                os.system('echo BB >> /home/pihit/workspace/contents_curator/src/test.txt')

    if True:
        d = TestDaemon2()
    else:
        d = Daemon('TestDaemon')
    d.main(sys.argv)

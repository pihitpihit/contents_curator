# -*- coding: utf-8 -*-
import os
import time
import random
from datetime import datetime

class BenchClock:
    def __init__(self):
        self.start = time.time_ns()
        return

    def __del__(self):
        self.finish = time.time_ns()
        print('duration(sec): %f' % self.nsToSec(self.finish - self.start))
        return

    def nsToSec(self, ns):
        return ns // 1000 / 1000 / 1000

def TestCase1_Arithmetic():
    bc = BenchClock()
    counter = 0
    for i in range(1000*1000*100):
        counter += random.random()
    return

def main():
    TestCase1_Arithmetic()
    return

if __name__ == '__main__':
    main()


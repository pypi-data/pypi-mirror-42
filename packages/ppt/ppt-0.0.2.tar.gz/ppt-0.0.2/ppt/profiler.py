#!/usr/bin/env python3

from __future__ import print_function

import cProfile
import pstats


class Profiler(object):

    def __init__(self):
        self.profiler = cProfile.Profile()

    def start(self):
        self.profiler.enable()

    def stop(self):
        self.profiler.disable()

    def stats(self):
        ps = pstats.Stats(self.profiler).sort_stats('cumulative')
        ps.print_stats()

    def summary(self):
        ps = pstats.Stats(self.profiler).sort_stats('cumulative')
        fn_calls = sum([ps.stats[s][0] for s in ps.stats])
        cumtime = sum([ps.stats[s][2] for s in ps.stats])
        print(fn_calls, 'function calls in', cumtime, 'seconds')


class SessionsProfiler(object):

    def __init__(self):
        self.sessions = {}
        self.current_session = None

    def time(self, name=None):
        session = self.start(name)
        self.current_session = session

    def start(self, name=None):
        if name not in self.sessions:
            self.sessions[name] = Profiler()
        self.sessions[name].start()
        return self.sessions[name]

    def stop(self, name=None):
        if name is None:
            self.current_session.stop()
            self.current_session = None
        else:
            self.sessions[name].stop()

    def stats(self, name=None):
        if name is not None:
            self.sessions[name].stats()
        else:
            for name in self.sessions:
                print('*' * 10, name, '*' * 10)
                self.sessions[name].stats()

    def summary(self, name=None):
        if name is not None:
            print(name, end=': ')
            self.sessions[name].summary()
        else:
            for name in self.sessions:
                print(name, end=': ')
                self.sessions[name].summary()

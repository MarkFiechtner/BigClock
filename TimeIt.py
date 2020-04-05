
"""

    This is part of the BigClock program.  It displays the time on a set of four,
    6.5", seven-segment characters from Sparkfun.com.
    
    Copyright (C) 2018-2020 Mark Fiechtner
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author: Mark_Fiechtner@Rocketmail.com

"""

import time

class TIMERObj():
    def __init__(self, txt, verbose):
        self.txt = txt
        self.verbose = verbose
        self.endtime = self.starttime = time.time()
    def __repr__(self):
        elapsed = self.endtime- self.starttime
        if self.verbose:
            return "{} start {:12.4f} end {:12.4f} elapsed {:1.4f}".format(self.txt, self.starttime, self.endtime, elapsed)
        else:
            return "{} elapsed {:1.4f}".format(self.txt, elapsed)
    def complete(self):
        self.endtime = time.time()

class TIMER():
    NONE = None
    ALL = 1
    MAIN = 2
    
    def __init__(self, txt="TIMER:", prnt=NONE, verbose=False):
        self.event_list = {}
        self.txt = txt
        self.prnt = prnt
        self.verbose = verbose
        self.starttime = None
        self.endtime = None
        self.elapsed = None
        self.next = 0
    def _print_main(self):
        if self.verbose:
            print("{} start {:12.4f} end {:12.4f} elapsed {:1.4f}".format(self.txt, self.starttime, self.endtime, self.elapsed))
        else:
            print("{} elapsed {:1.4f}".format(self.txt, self.elapsed))
    def _print_minor(self):
        for _, to in self.event_list.items():
            print("{}: {}".format(self.txt, to))
    def _print_all(self):
        self._print_main()
        self._print_minor()
    def __enter__(self):
        self.starttime = time.time()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.endtime = time.time()
        self.elapsed = self.endtime-self.starttime
        # terminated by exception
        if exc_type or exc_value or traceback:
            self._print_all()
        # want to see it all
        elif self.type == self.ALL:
            self._print_all()
        # just the main one
        elif self.type == self.MAIN:
            self._print_main()
    def startevent(self, txt):
        if self.type == self.ALL:
            cur = self.next
            self.next += 1
            self.event_list[cur] = TIMERObj(txt, self.verbose)
            return cur
        else:
            return None
    def endevent(self, eventtype):
        if self.type == self.ALL and eventtype:
            self.event_list[eventtype].complete()
    @property
    def type(self):
        return self.prnt


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

# class that encapsulates the current time and our control functions
class TimeControl:
    def __init__(self, polling=.01, tm=time.localtime()):
        self.tm = tm
        self.old_tm = tm
        # internal value
        self.polling_interval = polling
    # figure the remaining fraction of a second to sleep to reduce
    # polling in wait_for_second_to_change()
    def variable_sleep(self):
        # get current time including fractional seconds
        number = time.time()
        # isolate the fractional seconds left in this second
        frac = 1 - (number - int(number))
        frac -= ((int(frac*10))/10.0)
        # should only sleep if remaining time is greater than .1
        if frac >= .1:
            # sleep for frac
            time.sleep(frac)
        # after this sleep we should have less than .1 of a second
        # left until the next second
        return
    # wait for the next second
    def wait_for_second_to_change(self):
        # save old current time
        self.old_tm = self.tm
        # get new current time
        self.tm = time.localtime()
        # has the next second already come?
        if self.tm.tm_sec == self.old_tm.tm_sec:
            # wait for most of the remaining second to elapse
            self.variable_sleep()
            # get current time
            self.tm = time.localtime()
            # while the second changed hasn't changed
            while self.tm.tm_sec == self.old_tm.tm_sec:
                # wait part of a second 
                # see the polling rate defined in __init__
                time.sleep(self.polling_interval)
                # get current time
                self.tm = time.localtime()
        return
    # has the new hour changed from the old hour?
    def hour_changed(self):
        return (self.tm.tm_hour != self.old_tm.tm_hour)
    # has the new minute changed from the old minute?
    def minute_changed(self):
        return (self.tm.tm_min != self.old_tm.tm_min)
    def UTC(self):
        return time.time()

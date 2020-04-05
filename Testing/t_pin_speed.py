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


# see how fast the Raspbery PI Zero W can toggle a pin.
from pyLDD import gpioOutPin

from TimeIt import TIMER

pin = gpioOutPin(21)

reps = 100000

print("{} reps".format(reps))

try:
    with TIMER(txt="", prnt=TIMER.ALL, verbose=True):
        for i in range(reps):
            pin.Set(True)
            pin.Set(False)

finally:
    pin.Done()    
    

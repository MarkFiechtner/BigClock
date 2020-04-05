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


from pyLDD.BitBanger import BitBanger
# GPIO pins for controlling digit shift register
# (use BCM numbering, active high)
CLOCK = 22 # clock pin
DATA = 23 # data pin
LATCH = 24 # latch pin
MyBitBanger = BitBanger(CLOCK, DATA, LATCH)

import time

try:
    segment = 0
    # forever
    while True:
        # slow it down a bit
        time.sleep(.1)
        # write the list of bytes (4 of them) to the shift register and latch them
        MyBitBanger.WriteBytes([segment,segment,segment,segment])
        # next
        segment += 1
        # each byte can range from 0 to 255
        if segment > 255:
            segment = 0
        # print the next one
        print(segment)

finally:
    # clean up the digits
    MyBitBanger.WriteBytes([0,0,0,0,0,0])
    # clean up GPIO
    MyBitBanger.Done()


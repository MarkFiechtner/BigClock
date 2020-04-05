
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

"""
    This is more of a container than a program.  It holds
    all the specific information for this installation.
    It creates:
        A BitBanger encapsulating the logic to send bytes to the attached shift register(s)
        Three StandardDigit encapsulating the value-to-bits logic for a seven-segment display digit
        A NonStandardDigit encapsulating the value-to-bits logic for a seven-segment display digit (upside down)
        A FourDigitClock encapsulating the hardware wiring considerations and "clockiness"
        A TimeControl encapsulating the logic that waits for the second to change
"""

from pyLDD.BitBanger import BitBanger
# GPIO pins for controlling digit shift register
# (use BCM numbering, active high)
CLOCK = 22 # clock pin
DATA = 23 # data pin
LATCH = 24 # latch pin
MyBitBanger = BitBanger(CLOCK, DATA, LATCH)

from pyLDD.Digit import StandardDigit, NonStandardDigit
from FourDigitClock import FourDigitClock
# create a "clock" with four digits (hour 10's, hour 1's, minute 10's (upside down), minute 1's)
MyClock = FourDigitClock(StandardDigit(), StandardDigit(), NonStandardDigit(), StandardDigit())

# light it up (default segments are lit)
MyBitBanger.WriteBytes(MyClock.Bytes)
"""
# count from 0 to 10000 as fast as possible
for bites in MyClock.GenerateBytes():
    MyBitBanger.WriteBytes(bites)
"""

# update time from time server
from UpdateTime import DoUpdate
DoUpdate()

from TimeControl import TimeControl
# polling freq for determining when seconds change
POLLING = .01
MyTimeControl = TimeControl(POLLING)

try:
    # forever
    while True:
        # show the current time

        # once a second
        MyTimeControl.wait_for_second_to_change()
        # convert current time to bytes for the display
        timebytes = MyClock.GetTime12Bytes(MyTimeControl.tm) # 12 hour (am/pm)
        #timebytes = MyClock.GetTime24Bytes(MyTimeControl.tm) # 24 hour (military)
        #print(timebytes)
        # write the list of bytes to the shift register and latch them
        MyBitBanger.WriteBytes(timebytes)
        
        # if hour is midnight, update time from time server
        if MyTimeControl.tm.tm_sec == 0 and MyTimeControl.tm.tm_min == 0 and (MyTimeControl.tm.tm_hour == 0 or MyTimeControl.tm.tm_hour == 24):
            DoUpdate()

finally:
    # clear display segments
    MyBitBanger.WriteBytes([0,0,0,0])
    # clean up GPIO
    MyBitBanger.Done()

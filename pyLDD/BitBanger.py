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
Use this to operate the large digit driver hardware from SparkFun -
https://www.sparkfun.com/products/13279

Hooking up this device requires 3 GPIO pins.
Latch - latches the current shift register values into the output register
Clock - used to shift one bit into/out of the shift register
Data - bit shifted into shift register by clock
"""

from pyLDD import gpioOutPin

# This encapsulates the communications channel of the shift register
class BitBanger:
    def __init__(self, clock, data, latch):
        # create GPIO Output pins for each signal
        self.CLK = gpioOutPin(clock)
        print("Clock: {}".format(self.CLK))
        self.DATA = gpioOutPin(data)
        print("Data: {}".format(self.DATA))
        self.LATCH = gpioOutPin(latch)
        print("Latch: {}".format(self.LATCH))

    # interface

    # clock out the bytes to the shift register
    def WriteBytes(self, bites):
        for byte in bites:
            self._writebyte(byte)
        # latch shift registers to output registers
        self._latchbytes()
    # cleanup
    def Done(self):
        # use any of the GPIO pin objects to clean up
        self.CLK.Done()

    # internal routines

    # clock out 8 bits
    def _writebyte(self, byte):
        for i in [0,1,2,3,4,5,6,7]:
            self._writebit(byte & (1 << (7-i))) # msb first (dp)
    # latch shift register bytes in output registers
    def _latchbytes(self):
        # data is moved from shift to output on rising edge of latch (toggle signal)
        self.LATCH.Set(True)
        self.LATCH.Set(False)
# clock one bit
    def _writebit(self, bit):
        # set data based on bit
        self.DATA.Set(True if bit else False)
        # data bit is sampled on rising edge of clock (toggle signal)
        self.CLK.Set(True)
        self.CLK.Set(False)

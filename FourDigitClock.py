
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


# this encapsulates the four digit clock

# wiring should be daisy chained as:
#   hour 10's -> hour 1's -> minute 10's -> minute 1's
# NOTE: Due to the above wiring, the byte ordering is REVERSED
#    from what you would expect (minutes 1's is index 0)
Hrs10s=3; Hrs1s=2; Min10s=1; Min1s=0;

class FourDigitClock:
    # define each digit
    def __init__(self, h10, h1, m10, m1):
        # initialize arrays
        self._digits = [0,0,0,0]
        self._timebytes = bytearray([0,0,0,0])
        # save digits
        self._digits[Hrs10s] = h10
        self._digits[Hrs1s] = h1
        self._digits[Min10s] = m10
        self._digits[Min1s] = m1
        # save initial output bytes
        self._timebytes[Hrs10s] = self._digits[Hrs10s].byte
        self._timebytes[Hrs1s] = self._digits[Hrs1s].byte
        self._timebytes[Min10s] = self._digits[Min10s].byte
        self._timebytes[Min1s] = self._digits[Min1s].byte

    @property
    def Bytes(self):
        return self._timebytes
    
    def GenerateBytes(self):
        for i in range(10000):
            j = i
            self._timebytes[Min1s] = self._digits[Min1s].IntToByte(j%10)
            j = int(j/10)
            self._timebytes[Min10s] = self._digits[Min10s].IntToByte(j%10)
            j = int(j/10)
            self._timebytes[Hrs1s] = self._digits[Hrs1s].IntToByte(j%10)
            j = int(j/10)
            self._timebytes[Hrs10s] = self._digits[Hrs10s].IntToByte(j%10)
            yield self.Bytes 

    # for both routines:
    # change hours and minutes into output bytes
    # this is the "clockiness"
    
    # for this routine:
    # 12 hour format
    # blank leading 0 for hours
    # blink colon on seconds
    # light am/pm indicator
    def GetTime12Bytes(self, tm):
        # second indicator (colon) toggles on-off on even-odd seconds
        second = False if (tm.tm_sec % 2) == 1 else True
        hour = tm.tm_hour
        # assume morning
        am = True
        # using AM/PM - 12 hour time
        if hour >= 12:
            hour -= 12
            # afternoon
            am = False
        # midnight/noon are still 12, not 0
        if hour == 0:
            hour = 12
        # isolate hour 10's digit
        z = int(hour/10)
        # 10's digit != 0
        if z != 0:
            # no decimal point
            self._timebytes[Hrs10s] = self._digits[Hrs10s].IntToByte(z, False)
        else:
            # blank (10's == 0) using invalid value, no decimal point
            self._timebytes[Hrs10s] = self._digits[Hrs10s].IntToByte(-1, False)
        # isolate 1's hour digit
        hour -= int(z*10)
        # be sure to show second indicator
        self._timebytes[Hrs1s] = self._digits[Hrs1s].IntToByte(hour, second)
        # isolate 10's minute digit
        y = int(tm.tm_min/10)
        # be sure to show second indicator
        self._timebytes[Min10s] = self._digits[Min10s].IntToByte(y, second)
        # isolate 1's minute digit
        x = int(tm.tm_min - (y*10))
        # be sure to show AM/PM indicator
        self._timebytes[Min1s] = self._digits[Min1s].IntToByte(x, am)
        # return the new timebytes
        return self.Bytes

    # for this routine:
    # 24 hour format (midnight is 24, not 0)
    # blink colon on seconds
    def GetTime24Bytes(self, tm):
        # second indicator (colon) toggles on-off on even-odd seconds
        second = False if (tm.tm_sec % 2) == 1 else True
        hour = tm.tm_hour
        # midnight is 24, not 0
        if hour == 0:
            hour = 24
        # isolate hour 10's digit
        z = int(hour/10)
        # no decimal point
        self._timebytes[Hrs10s] = self._digits[Hrs10s].IntToByte(z, False)
        # isolate 1's hour digit
        hour -= int(z*10)
        # be sure to show second indicator
        self._timebytes[Hrs1s] = self._digits[Hrs1s].IntToByte(hour, second)
        # isolate 10's minute digit
        y = int(tm.tm_min/10)
        # be sure to show second indicator
        self._timebytes[Min10s] = self._digits[Min10s].IntToByte(y, second)
        # isolate 1's minute digit
        x = int(tm.tm_min - (y*10))
        # no decimal point
        self._timebytes[Min1s] = self._digits[Min1s].IntToByte(x, False)
        # return the new timebytes
        return self.Bytes

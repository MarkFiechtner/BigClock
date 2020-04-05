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

# The Digit class encapsulates one 7-segment digit  
#
#    standard           nonstandard
# (right-side up)      (upside down)
#
#       a                dp   d   
#      ___               x   ___
#     |   |                 |   |
#   f |   | b             c |   | e
#     | g |                 | g |
#      ___        OR         ___
#     |   |                 |   |
#   e |   | c             b |   | f
#     |   |                 |   |
#      ___   x               ___
#       d    dp               a
#
# segment indexes
a=0;b=1;c=2;d=3;e=4;f=5;g=6;dp=7
# reusable routines
class _digit:
    # create the bitmap for each digit using the passed in segment ordering
    def _setdigits(self, seg):
        # start with none
        self.digits = {}
        # add a bit for each segment that needs to be lit for a particular number character 
        self.digits[0] = seg[a]|seg[b]|seg[c]|seg[d]|seg[e]|seg[f]
        self.digits[1] = seg[b]|seg[c]
        self.digits[2] = seg[a]|seg[b]|seg[d]|seg[e]|seg[g]
        self.digits[3] = seg[a]|seg[b]|seg[c]|seg[d]|seg[g]
        self.digits[4] = seg[b]|seg[c]|seg[f]|seg[g]
        self.digits[5] = seg[a]|seg[c]|seg[d]|seg[f]|seg[g]
        self.digits[6] = seg[a]|seg[c]|seg[d]|seg[e]|seg[f]|seg[g]
        self.digits[7] = seg[a]|seg[b]|seg[c]
        self.digits[8] = seg[a]|seg[b]|seg[c]|seg[d]|seg[e]|seg[f]|seg[g]
        self.digits[9] = seg[a]|seg[b]|seg[c]|seg[f]|seg[g]
        # hex digits
        self.digits[10] = seg[a]|seg[b]|seg[c]|seg[e]|seg[f]|seg[g] # 'A'
        self.digits[11] = seg[c]|seg[d]|seg[e]|seg[f]|seg[g]        # 'b'
        self.digits[12] = seg[a]|seg[d]|seg[e]|seg[f]|seg[g]        # 'C'
        self.digits[13] = seg[a]|seg[b]|seg[c]|seg[d]|seg[e]|seg[g] # 'd'
        self.digits[14] = seg[a]|seg[d]|seg[e]|seg[f]|seg[g]        # 'E'
        self.digits[15] = seg[a]|seg[e]|seg[f]|seg[g]               # 'F'
        # decimal point value
        self.dp = seg[dp]
        # current byte (init to all on)
        self._byte = 255
    # convert the passed in integer into the proper byte to light segments in the display
    # includes the decimal point
    def IntToByte(self, char, dec=False):
        # if this is one of the ones we support
        if char in self.digits.keys():
            # get byte
            self._byte = self.digits[char]
        else:
            # default to nothing lit
            self._byte = 0
        # if we want the decimal point lit 
        if dec: self._byte |= self.dp
        return self._byte
    # get current byte value
    @property
    def byte(self):
        return self._byte

# "right-side up"
class StandardDigit(_digit):
    def __init__(self):
        # rightside up
        #       a, b,   c,   d,   e,   f,   g,   dp
        segs = [1,1<<6,1<<5,1<<4,1<<3,1<<1,1<<2,1<<7]
        # initialize the digits
        self._setdigits(segs)

# "upside down"
class NonStandardDigit(_digit):
    def __init__(self):
        # upside down
        #        d,   e,   f,  a, b,   c,   g,   dp
        segs = [1<<4,1<<3,1<<1,1,1<<6,1<<5,1<<2,1<<7]
        # initialize the digits
        self._setdigits(segs)


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


import platform
IsPICore = None
def IsPiCore():
    global IsPICore
    if IsPICore == None:
        temp = platform.platform()
        if "piCore" in temp:
            IsPICore = True
        else:
            IsPICore = False
    return IsPICore

import os
def DoUpdate():
    print("update time")
    # running on piCore?
    if IsPiCore():
        # send NTPD request to update time from time server
        os.system("sudo /usr/bin/getTime.sh")


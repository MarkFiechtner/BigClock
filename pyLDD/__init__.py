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
    A python driver for the Large Digit Driver from Sparkfun
    https://www.sparkfun.com/products/13279
"""

try:
    import RPi.GPIO as GPIO # only available on rPI
except:
    print("Could not import RPi.GPIO, creating dummy pin(s)")
    # constants
    HIGH = True
    LOW = False
    class gpio(): # stub for other platforms
        def __init__(self):
            self.BCM = 1
            self.HIGH = HIGH
            self.LOW = LOW
            self.OUT = HIGH
            self.IN = LOW
        def cleanup(self):
            return
        def output(self, pin, val):
            return
        def setmode(self, val):
            return
        def setup(self, pin, val, initial):
            return
    GPIO = gpio()

# This encapsulates the single GPIO output pin and it's attributes
class gpioOutPin:
    # default to Broadcom board mode
    def __init__(self, pin, bm=GPIO.BCM):
        # set up variables
        self.pin = pin
        # set up GPIO
        GPIO.setmode(bm)  # set board mode
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)  # set up pin
        #print ("pin:", self.pin)
    def __repr__(self):
        return "pin: {}".format(self.pin)
    def Set(self, val):
        # set the pin value to val
        GPIO.output(self.pin, val)
    def Done(self):
        # be nice, clean up your mess
        GPIO.cleanup()


I needed a clock in my garage that could be seen from all over the garage and through
a couple of doors when they are open.  This project creates a clock with big digits
(about 6" tall).  The clock is "always" right as it gets the current time from the
internet at startup and also each night at midnight.  The clock can be "rudely
interrupted" by power loss and never ruin the MicroSD card as it uses the piCore OS
which only reads from MicroSD card at boot and only writes when told to do so.  The
clock plugs into the wall (AC mains) for power so no batteries to worry about.



This is the hardware I used -

Raspberry PI Zero W (there is NO dependency on this so use what you want)
32GB MicroSD card (way too big; but, I got it cheap)
SparkFun Logic Level Converter - Bi-Directional (https://www.sparkfun.com/products/12009)
SparkFun ATX Power Connector Breakout Kit - 12V/5V (4-pin) (https://www.sparkfun.com/products/15701)
(4) 7-Segment Display - 6.5" (Red) (https://www.sparkfun.com/products/8530)
(4) SparkFun Large Digit Driver (https://www.sparkfun.com/products/13279)
(1) Jumper Wire - 0.1", 6-pin, 6" (https://www.sparkfun.com/products/10371)
(2) Jumper Wire - 0.1", 6-pin, 12" (https://www.sparkfun.com/products/10376)
Another 6-pin jumper to connect to the first digit (4", 6" or 12", depending on your need)

NOTE: The PI has power supplied to the GPIO header by the 5v portion of the power supply
NOTE: The PI Zero W has on-board wifi which attaches to my home network to get the time
	(NTP) and allow headless operation while supporting an SSH command line

I added some jumper wires and soldered some headers to create the proper circuits.
I use one of the 7-segment displays (minute 10's) upside down.  This allows me to blink the
	two decimal points (hour 1's, minute 10's) as a second indicator.
I used the two 12" jumpers to attach the upside down display (minute 10's) to the previous
	(hour 1's) and next (minute 1's) displays.


Building the Pi Zero W running piCore and the rest of this stuff - 

Use a piCore image file with wifi built in or create your own MicroSD card using images
and instructions at -

http://tinycorelinux.net/
http://tinycorelinux.net/ports.html 
http://forum.tinycorelinux.net/index.php/board,57.0.html

see TimeZone.txt and Hostname.txt to set the timezone and hostname



To set up the proper file structure and extensions on the Zero, use an SSH terminal and:

(Login: tc Password: piCore)

cd ~
mkdir src
mkdir src/BigClock
mkdir src/BigClock/pyLDD

echo 'home/tc/src' >> /opt/.filetool.lst
echo 'home/tc/src/BigClock' >> /opt/.filetool.lst
echo 'home/tc/src/BigClock/pyLDD' >> /opt/.filetool.lst

tce-load -wi python3.6
tce-load -wi python3.6-RPi.GPIO

optional:

tce-load -wi nano

NOTE: The source code (in BigClock\Clock.py) assumes:

# GPIO pins for controlling digit shift register
# (use BCM numbering, active high)
CLOCK = 22 # clock pin
DATA = 23 # data pin
LATCH = 24 # latch pin

If this is NOT right, change the definitions or the wiring.



In a PC command prompt, I use pscp to copy all the source to the destination PI.

NOTE: I have it wrapped by an interactive python script (not included in this project):

d:
cd "Python Dev"
python Transfer.py

In the Transfer program, choose BigClock, * (all).



Back in the Pi SSH terminal, use:

filetool.sh -b

Saves all the files for next time.

cd /home/tc/src/BigClock
sudo python3.6 Clock.py

If hooked up right, the clock should be running.

If you want this to run at startup, add those two lines to the end of /opt/bootlocal.sh



Troubleshooting:

Make sure you are using a level shifter for the PI's GPIO signals to boost them to 5v from 3.3
Make sure one of your power supplies outputs 12v for the LED segments
If the script doesn't run, make sure you use sudo in front of the command
If the time is wrong, see the TimeZone.txt file
If you want to use 24 hour (military) time, look at the commented line in Clock.py

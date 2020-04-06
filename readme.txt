
I needed a clock in my garage that could be seen from all over the garage and through
a couple of doors when they are open.  This project creates a clock with big digits
(about 6" tall).  The clock is "always" right as it gets the current time from the
internet at startup and also each night at midnight.  The clock can be "rudely
interrupted" by power loss and never ruin the MicroSD card as it uses the piCore OS
which only reads from MicroSD card at boot and only writes when told to do so.  The
clock plugs into the wall (AC mains) for power so no batteries to worry about.

Please note that I use this on piCore OS but the python3 code was tested on Buster
(Raspian), too.

The hardware directory contains information about the hardware I used to complete
this project.
The Testing directory contains some files I used to test during debug.
The pyLDD directory contains some low level hardware control stuff.



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
mkdir src/BigClock/Testing

echo 'home/tc/src' >> /opt/.filetool.lst
echo 'home/tc/src/BigClock' >> /opt/.filetool.lst
echo 'home/tc/src/BigClock/pyLDD' >> /opt/.filetool.lst
echo 'home/tc/src/BigClock/Testing' >> /opt/.filetool.lst

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



In a PC command prompt, I use pscp to copy all the source to the destination PI.  Something like:
pscp -batch -pw piCore d:BigClock/*.py tc@192.168.1.xxx:/src/BigClock

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

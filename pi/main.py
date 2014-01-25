import smbus
import curses
import time
import sys

bus = smbus.SMBus(1)
address = 0x1a
chars = [27]

output = False
if "-v" in sys.argv:
    output = True
    screen = curses.initscr()
    import atexit
    atexit.register(curses.endwin)
    
else:
    print "eve running..."

while True:
    val = bus.read_i2c_block_data(address, 0)
    
    if (output):
        screen.clear()
        screen.border(0)
        screen.addstr(1, 2, 'DX4:')
        screen.addstr(2, 4, 'Channel 1:')
        screen.addstr(2, 15, str(val[20]))    
        screen.addstr(3, 4, 'Channel 2:')
        screen.addstr(3, 15, str(val[21]))    
        screen.addstr(4, 4, 'Channel 3:')
        screen.addstr(4, 15, str(val[22]))    
        screen.addstr(5, 4, 'Channel 4:')
        screen.addstr(5, 15, str(val[23]))    
        screen.refresh()

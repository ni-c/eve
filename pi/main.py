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

def split(x):
    c = (x >> 8) & 0xff
    f = x & 0xff
    return c, f

def merge(c, f):
    r = (c << 8) + f
    return r

a,b = split(60000)
c,d = split(1)
e,f = split(2)
g,h = split(3)
bus.write_i2c_block_data(address, 2, [a, b, a, b, a, b, c, d, e, f, g, h])

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
        
        screen.addstr(7, 2, 'Stepper:')
        screen.addstr(8, 4, 'Remaining Steps X:')
        x = merge(val[2], val[3])
        screen.addstr(8, 23, str(x))    
        screen.addstr(9, 4, 'Remaining Steps Y:')
        y = merge(val[4], val[5])
        screen.addstr(9, 23, str(y))
        screen.addstr(10, 4,'Remaining Steps Z:')
        z = merge(val[6], val[7])
        screen.addstr(10, 23, str(z))
        
        screen.addstr(11, 4, 'Speed X:')
        x = merge(val[8], val[9])
        screen.addstr(11, 13, str(x))    
        screen.addstr(12, 4, 'Speed Y:')
        y = merge(val[10], val[11])
        screen.addstr(12, 13, str(y))
        screen.addstr(13, 4,'Speed Z:')
        z = merge(val[12], val[13])
        screen.addstr(13, 13, str(z))
        
        screen.refresh()

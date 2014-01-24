import smbus
import curses
import time
bus = smbus.SMBus(1)
address = 0x1a

while True:
    
    try:
        val = bus.read_i2c_block_data(address, 0)
    except:
        print "error"
    
    screen = curses.initscr()
    screen.clear()
    screen.border(0)
    
    window = curses.newwin(16, 16, 2, 2)
    window.border(0)
    
    screen.addstr(1, 2, 'Channel 1:')
    screen.addstr(1, 13, str(val[0]))    
    screen.addstr(2, 2, 'Channel 2:')
    screen.addstr(2, 13, str(val[1]))    
    screen.addstr(3, 2, 'Channel 3:')
    screen.addstr(3, 13, str(val[2]))    
    screen.addstr(4, 2, 'Channel 4:')
    screen.addstr(4, 13, str(val[3]))    
    screen.refresh()

curses.endwin()

import smbus
import time
bus = smbus.SMBus(1)
address = 0x1a

while True:
    time.sleep(1)
    write(0)
    time.sleep(1)
    write(255)
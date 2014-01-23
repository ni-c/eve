import smbus
import time
bus = smbus.SMBus(1)
address = 0x1a

def write(value):
    bus.write_byte_data(address, 0, value)
    return -1

while True:
    time.sleep(1)
    write(0)
    time.sleep(1)
    write(255)

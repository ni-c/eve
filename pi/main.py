import smbus
import time
bus = smbus.SMBus(1)
address = 0x1a

while True:
    time.sleep(1)
    bus.write_word_data(address, 0, 1337)
    time.sleep(1)
    bus.write_word_data(address, 0, 0)

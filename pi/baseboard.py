#!/usr/bin/python

import threading, smbus, time, wiringpi2, spidev

MOTOR_STEPS_POS = [2, 4, 6]
MOTOR_STEPS_ADD_POS = [14, 16, 18]
MOTOR_SPEED_POS = [8, 10, 12]
RC_CHANNEL_POS = [20, 21, 22, 23]
RC_OFFSET = [114, 114, 114, 114]

threadLock = threading.Lock()

class I2C (threading.Thread):
   
    def resetAD7705(self):
        # Reset
        wiringpi2.pinMode(23,1)
        wiringpi2.digitalWrite(23,0)
        wiringpi2.digitalWrite(23,1)
        # Initialize AD7705 
        self.spi.xfer2([0xff, 0xff, 0xff, 0xff, 0xff])
        self.spi.xfer2([0x20, 0x0c, 0x10, 0x40, 0x08])
        return 1
   
    def __init__(self, bus, address):
        threading.Thread.__init__(self)
        self.buffer = []
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.flushNeeded = False
        self.isActive = True

        # Initialize GPIO
        wiringpi2.wiringPiSetupGpio()
        # AD7705 CS
        wiringpi2.pinMode(24,1)
        wiringpi2.digitalWrite(24,0)
        
        # Setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 100000
        
        self.resetAD7705()
        
        self.update()
      
    def split(self, x):
        c = (x >> 8) & 0xff
        f = x & 0xff
        return c, f
    
    def merge(self, c, f):
        r = (c << 8) + f
        return r

    def setBit(self, v, index, x):
        mask = 1 << index
        v &= ~mask
        if x:
            v |= mask
        return v    

    def getBit(self, v, index):
        return ((v&(1<<index))!=0);
    
    def setMotorSteps(self, motor, steps):
        high, low = self.split(steps)
        self.buffer[MOTOR_STEPS_POS[motor]] = high
        self.buffer[MOTOR_STEPS_POS[motor] + 1] = low
        self.flushNeeded = True
        return self
    
    def addMotorSteps(self, motor, steps):
        high, low = self.split(steps)
        self.buffer[MOTOR_STEPS_ADD_POS[motor]] = high
        self.buffer[MOTOR_STEPS_ADD_POS[motor] + 1] = low
        self.flushNeeded = True
        return self
    
    def getMotorSteps(self, motor):
        return self.merge(self.buffer[MOTOR_STEPS_POS[motor]], self.buffer[MOTOR_STEPS_POS[motor] + 1])
    
    def setMotorSpeed(self, motor, speed):
        high, low = self.split(speed)
        self.buffer[MOTOR_SPEED_POS[motor]] = high
        self.buffer[MOTOR_SPEED_POS[motor] + 1] = low
        self.flushNeeded = True
        return self

    def getMotorSpeed(self, motor):
        return self.merge(self.buffer[MOTOR_SPEED_POS[motor]], self.buffer[MOTOR_SPEED_POS[motor] + 1])
    
    def setMotorDirection(self, motor, direction):
        self.buffer[0] = self.setBit(self.buffer[0], 2 + motor, direction)
        self.flushNeeded = True
        return self    
    
    def getMotorDirection(self, motor):
        return self.getBit(self.buffer[0], 2 + motor)
            
    def getRCChannel(self, channel):
        return self.buffer[RC_CHANNEL_POS[channel]] - RC_OFFSET[channel]

    def getRCChannels(self):
        return self.buffer[RC_CHANNEL_POS[0]] - RC_OFFSET[0], self.buffer[RC_CHANNEL_POS[1]] - RC_OFFSET[1], self.buffer[RC_CHANNEL_POS[2]] - RC_OFFSET[2], self.buffer[RC_CHANNEL_POS[3]] - RC_OFFSET[3]
    
    def update(self):
        self.buffer = self.bus.read_i2c_block_data(self.address, 0)
        return self

    def flush(self):
        self.flushNeeded = False
        self.bus.write_i2c_block_data(self.address, 0, self.buffer)
        return self
    
    def enableRC(self):
        self.buffer[0] = self.setBit(self.buffer[0], 1, 1)
        self.flushNeeded = True
        return self
    
    def disableRC(self):
        self.buffer[0] = self.setBit(self.buffer[0], 1, 0)
        self.flushNeeded = True
        return self    
    
    def isRCEnabled(self):
        return self.getBit(self.buffer[0], 1)
     
    def enableMotor(self):
        self.buffer[0] = self.setBit(self.buffer[0], 5, 1)
        self.flushNeeded = True
        return self
    
    def disableMotor(self):
        self.buffer[0] = self.setBit(self.buffer[0], 5, 0)
        self.flushNeeded = True
        return self    
    
    def isMotorEnabled(self):
        return self.getBit(self.buffer[0], 5)
   
    def getVoltage(self, channel):
        register = self.spi.xfer2([0x38, 0x00, 0x00])
        voltage = (self.merge(register[1], register[2]) - 32768) * 0.00079107
        return voltage
    
    def stop(self):
        self.isActive = False
    
    def run(self):
        while self.isActive:
            if self.flushNeeded:
                self.flush()
            self.update()
            time.sleep(0.01)
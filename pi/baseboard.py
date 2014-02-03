#!/usr/bin/python

import threading, smbus

MOTOR_STEPS_POS = [2, 4, 6]
MOTOR_STEPS_ADD_POS = [14, 16, 18]
MOTOR_SPEED_POS = [8, 10, 12]
RC_CHANNEL_POS = [20, 21, 22, 23]

class I2C (threading.Thread):
   
    def __init__(self, bus, address):
        threading.Thread.__init__(self)
        self.buffer = []
        self.bus = smbus.SMBus(bus)
        self.address = address
        self.flushNeeded = False
        self.isActive = True
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
    
    def getRCChannel(self, channel):
        return self.buffer[RC_CHANNEL_POS[channel]]
    
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
    
    def stop(self):
        self.isActive = False
    
    def run(self):
        while self.isActive:
            if self.flushNeeded:
                self.flush()
            self.update()
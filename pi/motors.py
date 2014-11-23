#!/usr/bin/python

import threading, time

class Motors (threading.Thread):

    def __init__(self, bb):
        threading.Thread.__init__(self)
        self.bb = bb
        self.isActive = True

    def stop(self):
        self.isActive = False

    def run(self):
        while self.isActive:
            """
            if self.bb.isRCEnabled:
                ch0, ch1, ch2, ch3 = self.bb.getRCChannels()

                Vx = ch1 * -1
                Vy = ch2
                Vr = ch3 * -1
                
                v = [0,0,0]
                
                v[0] = (Vx + Vr)
                v[1] = int(round((-0.5 * Vx) - (0.8660 * Vy) + Vr))
                v[2] = int(round((-0.5 * Vx) - (-0.8660 * Vy) + Vr))
                
                for i in range(0, 3):
                    if v[i] < 0:
                        v[i] = v[i] * -1
                        self.bb.setMotorDirection(i, 1)
                    else:
                        self.bb.setMotorDirection(i, 0)
                    self.bb.setMotorSpeed(i, 250 - v[i])
            """
            time.sleep(0.1)
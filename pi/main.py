#!/usr/bin/python

import sys, threading, time, log
from BaseHTTPServer import HTTPServer

import baseboard, webserver, motors

log.info("Starting up...")

try:

    threadLock = threading.Lock()

    bb = baseboard.I2C(1, 0x1a)
    bb.start()

    threadLock.acquire()
    bb.disableRC()
    bb.disableMotor()
    bb.setMotorSteps(0, 0).setMotorSpeed(0, 1).setMotorDirection(0, 0);
    bb.setMotorSteps(1, 0).setMotorSpeed(1, 1).setMotorDirection(1, 0);
    bb.setMotorSteps(2, 0).setMotorSpeed(2, 1).setMotorDirection(2, 1);
    threadLock.release()

    motors = motors.Motors(bb)
    motors.start()

    log.info("EVE running")

    class MyHTTPServer(HTTPServer):
        def __init__(self, *args, **kw):
            HTTPServer.__init__(self, *args, **kw)
            self.bb = bb
    server = MyHTTPServer(('', 80), webserver.JsonApi)
    server.serve_forever()

    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    log.info("Shutting down...")
    server.socket.close()
    bb.stop()
    motors.stop()
    sys.exit()

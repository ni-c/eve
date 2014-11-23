#!/usr/bin/python

import sys, threading, time
from BaseHTTPServer import HTTPServer

import baseboard, webserver, motors

try:

    threadLock = threading.Lock()

    print "eve running..."

    bb = baseboard.I2C(1, 0x1a)
    bb.start()

    threadLock.acquire()
    bb.disableRC()
    bb.setMotorSteps(0, 0).setMotorSpeed(0, 255).setMotorDirection(0, 0);
    bb.setMotorSteps(1, 0).setMotorSpeed(1, 255).setMotorDirection(1, 0);
    bb.setMotorSteps(2, 0).setMotorSpeed(2, 255).setMotorDirection(2, 0);
    threadLock.release()

    motors = motors.Motors(bb)
    motors.start()

    class MyHTTPServer(HTTPServer):
        def __init__(self, *args, **kw):
            HTTPServer.__init__(self, *args, **kw)
            self.bb = bb
    server = MyHTTPServer(('', 80), webserver.JsonApi)
    server.serve_forever()

    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    server.socket.close()
    bb.stop()
    motors.stop()
    sys.exit()

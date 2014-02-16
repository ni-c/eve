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
    bb.setMotorSteps(0, 10000).setMotorSpeed(0, 0).setMotorSteps(1, 10000).setMotorSpeed(1, 0).setMotorSteps(2, 10000).setMotorSpeed(2, 0)
    bb.disableRC()
    threadLock.release()

    motors = motors.Motors(bb)
    motors.start()    

    class MyHTTPServer(HTTPServer):
        def __init__(self, *args, **kw):
            HTTPServer.__init__(self, *args, **kw)
            self.bb = bb
    server = MyHTTPServer(('', 8080), webserver.JsonApi)
    server.serve_forever()
        
    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    server.socket.close()
    bb.stop()
    motors.stop()
    sys.exit()

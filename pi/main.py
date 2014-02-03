#!/usr/bin/python

import smbus, sys, threading, time
from BaseHTTPServer import HTTPServer

import baseboard, webserver

try:

    threadLock = threading.Lock()
    
    print "eve running..."
    
    bb = baseboard.I2C(1, 0x1a)
    bb.start()

    threadLock.acquire()
    bb.setMotorSteps(0, 30000).setMotorSpeed(0, 10).setMotorSteps(1, 30000).setMotorSpeed(1, 20).setMotorSteps(2, 30000).setMotorSpeed(2, 30)
    bb.disableRC()
    threadLock.release()
    
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
    sys.exit()

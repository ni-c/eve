#!/usr/bin/python

import json
from BaseHTTPServer import BaseHTTPRequestHandler

class JsonApi(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            result = json.dumps({'rc': { 
                                  'channel0': self.server.bb.getRCChannel(0),
                                  'channel1': self.server.bb.getRCChannel(1),
                                  'channel2': self.server.bb.getRCChannel(2),
                                  'channel3': self.server.bb.getRCChannel(3)
                                }, 'motors': {
                                  'motor0': {
                                    'steps': self.server.bb.getMotorSteps(0),
                                    'speed': self.server.bb.getMotorSpeed(0)  
                                  },
                                  'motor1': {
                                    'steps': self.server.bb.getMotorSteps(1),
                                    'speed': self.server.bb.getMotorSpeed(1)  
                                  },
                                  'motor2': {
                                    'steps': self.server.bb.getMotorSteps(2),
                                    'speed': self.server.bb.getMotorSpeed(2)  
                                  },
                                }, 'enabled': {
                                    'rc': self.server.bb.isRCEnabled()
                                  }
                                }, sort_keys=True)
            self.wfile.write(result)
        else:
            self.send_error(404, "Not Found")
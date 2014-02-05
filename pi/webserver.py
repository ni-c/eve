#!/usr/bin/python

import json
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler

class JsonApi(BaseHTTPRequestHandler):
    
    def do_POST(self):
        if self.path == '/data.json':
            try:
                content_len = int(self.headers.getheader('content-length'))
                post_body = self.rfile.read(content_len)
                post_data = json.loads(post_body)
                try:
                    if post_data['enabled']['rc']:
                        self.server.bb.enableRC()
                    else:
                        self.server.bb.disableRC()
                except:
                    pass
                self.send_response(200)
            except:
                self.send_error(400, "Bad Request")
        else:
            self.send_error(404, "Not Found")
            
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
            try:
                path = self.path.replace('..', '')
                if path == '/':
                    path = '/index.html'
                f = open(curdir + sep + 'client' + path)
                self.send_response(200)
                if path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif path.endswith('.js') or path.endswith('.js.map'):
                    self.send_header('Content-type', 'application/javascript')
                elif path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                else:
                    self.send_error(404, "Not Found")
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            except:
                self.send_error(404, "Not Found")
                
    def log_message(self, format, *args):
        return


#!/bin/bash

import multiprocessing
import os
import subprocess
import time
import BaseHTTPServer


HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.

Q = os.environ['Q']


def install_formula(name):
    output = subprocess.check_output(os.path.join(Q, name), shell=True, executable='/bin/bash')
    print output
    output = subprocess.check_output(['sqs_message', 'install', 'finished'], shell=True, executable='/bin/bash')
    print 'SQS_MESSAGE: ', output


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/plain")
        s.end_headers()

        path_items = s.path[1:].split('/')
        if len(path_items) == 2 and path_items[0] == 'formulas':
            formula_name = path_items[1]
            if os.access(os.path.join(Q, formula_name), os.F_OK):
                s.wfile.write('installing %s' % formula_name)
                p = multiprocessing.Process(target=install_formula, args=(formula_name,))
                p.start()
            else:
                s.wfile.write('unable to find formula %s' % formula_name)
        else:
            s.wfile.write('not sure what your trying to do')


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

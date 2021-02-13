import os
import socket
import sys
from protocols.servers.serverlibs.web import base_handler
from protocols.servers.serverlibs.web import threaded_http
from threading import Thread


class Server:

    def __init__(self, cli_object):
        self.protocol = 'http'
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 80

    def serve(self):
        try:
            print(f'[*] Starting an HTTP server on port {self.port}.')
            # bind to all interfaces
            Thread(target=self.serve_on_port).start()
            print('[*] The server is running.')
        # Handle keyboard interrupts
        except KeyboardInterrupt:
            print('[*] Shutting down the HTTP server.')

    def serve_on_port(self):
        try:
            server80 = threaded_http.ThreadingHTTPServer(
                ("0.0.0.0", self.port), base_handler.GetHandler)
            server80.serve_forever()
        except socket.error:
            print(f'f[*]Error: Port {self.port} is currently in use.')
            sys.exit()

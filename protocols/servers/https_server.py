import os
import socket
import ssl
import sys
from common import helpers
from protocols.servers.serverlibs.web import base_handler
from protocols.servers.serverlibs.web import threaded_http
from threading import Thread


class Server:

    def __init__(self, cli_object):
        self.protocol = 'https'
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 443

    def serve(self):
        try:
            print(f'[*] Starting an HTTPS server on port {self.port}.')
            # Bind to all interfaces
            Thread(target=self.serve_on_port).start()
            print('[*] The server is running.')
        # Handle keyboard interrupts
        except KeyboardInterrupt:
            print('[*] Shutting down the HTTPS server.')
        return

    def serve_on_port(self):
        try:
            cert_path = helpers.ea_path() +\
                '/protocols/servers/serverlibs/web/server.pem'
            server = threaded_http.ThreadingHTTPServer(
                ('0.0.0.0', self.port), base_handler.GetHandler)
            server.socket = ssl.wrap_socket(
                server.socket, certfile=cert_path, server_side=True)
            server.serve_forever()
        except socket.error:
            print(f'[*] Error: Port {self.port} is currently in use.')
            sys.exit()

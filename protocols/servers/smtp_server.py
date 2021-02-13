"""

This was based on code made available at http://pymotw.com/2/smtpd/

"""

import asyncore
import os
import socket
import sys
from common import helpers
from protocols.servers.serverlibs.smtp import smtp_class


class Server:

    def __init__(self, cli_object):

        self.protocol = 'smtp'
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 25

    def serve(self):

        exfil_directory = os.path.join(helpers.ea_path(), 'transfer/')

        if not os.path.isdir(exfil_directory):
            os.makedirs(exfil_directory)

        print(f'[*] Started an SMTP server on port {self.port}.')
        try:
            smtp_class.CustomSMTPServer(('0.0.0.0', self.port), None)
        except socket.error:
            print(f'[*] Error: Port {self.port} is currently in use.')
            print('[*] Error: Please re-start when not in use.')
            sys.exit()

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            print('[*] Shutting down the SMTP server.')
            sys.exit()

import os
import socket
import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Server:

    def __init__(self, cli_object):
        self.protocol = 'ftp'
        self.username = cli_object.username
        self.password = cli_object.password
        self.data_directory = ""
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 21

        if cli_object.ip:
            self.ip = cli_object.ip
        else:
            self.ip = None

    def serve(self):
        # Current directory
        exfil_directory = os.path.join(os.getcwd(), 'transfer')
        loot_path = exfil_directory + "/"

        # Check to make sure the agent directory exists, and a loot
        # directory for the agent. If not, make them
        if not os.path.isdir(loot_path):
            os.makedirs(loot_path)

        try:
            authorizer = DummyAuthorizer()
            authorizer.add_user(self.username, self.password, homedir=loot_path, perm="elradfmwM")

            handler = FTPHandler
            handler.authorizer = authorizer

            # Define a customized banner (string returned when client connects)
            handler.banner = "Connecting to Egress-Assess's FTP server!"
            # Define public address and passive ports making NAT configurations more predictable
            handler.masquerade_address = self.ip
            handler.passive_ports = range(60000, 60100)

            try:
                server = FTPServer(('', self.port), handler)
                server.serve_forever()
            except socket.error:
                print(f'[*] Error: Port {self.port} is currently in use.')
                sys.exit()
        except ValueError:
            print('[*] Error: The directory you provided does not exist.')
            print('[*] Error: Re-start with a valid directory.')
            sys.exit()

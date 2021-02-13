"""

This is the ftp client code

"""

import os
import socket
import sys
from common import helpers
from ftplib import FTP
from ftplib import error_perm


class Client:

    def __init__(self, cli_object):
        self.protocol = 'ftp'
        self.remote_server = cli_object.ip
        self.username = cli_object.username
        self.password = cli_object.password

        if cli_object.client_port is None:
            self.port = 21
        else:
            self.port = cli_object.client_port

        if cli_object.file is None:
            self.file_transfer = False
        else:
            if '/' in cli_object.file:
                self.file_transfer = cli_object.file
            else:
                self.file_transfer = cli_object.file.split('/')[-1]

    def transmit(self, data_to_transmit):

        try:
            ftp = FTP()
            ftp.connect(self.remote_server, self.port)
        except socket.gaierror:
            print('[*] Error: Cannot connect to FTP server.  Check provided IP.')
            sys.exit()

        try:
            ftp.login(self.username, self.password)
        except error_perm:
            print('[*] Error: Username or password is incorrect.  Please re-run.')
            sys.exit()

        if not self.file_transfer:
            ftp_file_name = helpers.writeout_text_data(data_to_transmit)
            ftp.storbinary("STOR " + ftp_file_name, open(helpers.ea_path() + "/" + ftp_file_name))
            os.remove(helpers.ea_path() + "/" + ftp_file_name)
        else:
            ftp.storbinary("STOR " + self.file_transfer, open(self.file_transfer))

        ftp.quit()
        print('[*] File sent')

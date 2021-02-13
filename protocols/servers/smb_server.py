import os
from impacket import smbserver
from impacket.ntlm import compute_lmhash, compute_nthash


class Server:

    def __init__(self, cli_object):
        self.protocol = "smb"
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 445

        self.smb2support = cli_object.no_smb2
        self.username = False
        self.password = False

        if cli_object.username and cli_object.password:
            self.username = cli_object.username
            self.password = cli_object.password
            self.lmhash = compute_lmhash(self.password)
            self.nthash = compute_nthash(self.password)

    def serve(self):
        try:

            # Current directory
            exfil_directory = os.path.join(os.getcwd(), 'transfer')
            loot_path = exfil_directory + "/"

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent. If not, create them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            server = smbserver.SimpleSMBServer('0.0.0.0', self.port)
            server.setSMB2Support(self.smb2support)

            if self.username and self.password:
                server.addCredential(self.username, 0, self.lmhash, self.nthash)

            server.addShare("TRANSFER", "transfer/", "Egress-Assess transfer share")

            # If you don't want log to stdout, comment the following line
            # If you want log dumped to a file, enter the filename
            server.setLogFile('')

            print(f'[*] SMB server is currently running on {self.port}.')
            print('[*] Note: port 445 is blocked by some ISPs.')

            # Rock and roll
            server.start()
        # Handle keyboard interrupts
        except KeyboardInterrupt:
            print('Stopping the SMB server.')

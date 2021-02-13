"""

Base code from https://searchcode.com/codesearch/raw/53300304/

"""

import os
import paramiko
import socket
import sys
import threading
import time
from common import helpers
from io import StringIO
from protocols.servers.serverlibs.sftp import sftp_classes


class Server:

    def __init__(self, cli_object):
        self.protocol = "sftp"
        self.username = cli_object.username
        self.password = cli_object.password
        self.sftp_directory = helpers.ea_path() + '/transfer'
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 22
        self.rsa_key = """
        -----BEGIN RSA PRIVATE KEY-----
MIIEoQIBAAKCAQEArJqP/6XFBa88x/DUootMmSzYa3MxcTV9FjNYUomqbQlGzuHa
n1Ef6YClJuBWu1eCdZfoeUoa56du1XV2eGKdDjWEqyie2uZ8RZeJZvT1wCuyvO6X
E143A4z3xHi6R6Qi7rimJFpxL6lGmYHx64wQgL93FXTe/HrmdPoxGeTEf+PnN/PV
Se321o/Ludqfu+8cldbuKaYRRZJSPT+sIMafvErL86I3JShYqaBjXcic8yYgaAZx
6Ieu6A19UJzZurQpCdnWoMMLEQ1EgU4LIkUg+SzVSTpBDV3uiBB0+iOdG+v0v+RO
53GAcKRx9Y38vQazpdAw4AhX97Hj6c/WcpET+QIBIwKCAQBsfmkkWZHJDxBDKao6
SO5RpyjzFTUFVNJIeAuhmFx/DSUxlUeXV5Bm4yX7Le1f0JslWCu59BDpYe3lQoT7
NqvdC7J6NspAc56SJLzEX3Xmgd4QW3Tnmk53QqpePUHj44Or/wlYreC+3240mtKU
DuXNRSZIAFGmBBvUgAGbP1bxTGRShWlebnDsEFuv8BnrjTB1GBN3SshgwTuApete
7yPPNNPhiAMHN27z5p5sMDU43+FgZd8GEJbHckmriIcwLr1Q0iwlmsrYRndRnA7u
bbl9D5SwTROE8mtACHBLOdkJ5glfp68GhKjZ+HPTkI+fKqv70DOB7TsP9F4EsNO/
FQUzAoGBANo2ScHL6RFHUpztE0+dc9g9Yk4S+tjW1sVHMOWGN/KmwiqBIwiusvWY
vXf/4i/kbehGnwedAtfRmjQSJbIyOEhMt1MxaN0Wn44YUgoWCbfplJG1Tmk25eEX
VrwOahTtzDGibtHNNmi97D2dFR7V36mhECTqwyzEE142yGrRJnLPAoGBAMp+YXd/
D2B0xhFMJmyzYHdBFCQHbm4DWZcGey09tSKo+mei+EDq+knSrjUmJV40PMXwxVjw
anLZJjEh72e71G28jlR5WEhciT5nJqN5pB8Oc9cHFCGC9mLQrEwW9MYqAz/WvCx4
lpa1Cge2b/lp7snc3Yt4BfAl35MIqElOg163AoGAGPBC8ZOlm5MfYmQ8uKRHwPES
jJR0cI2U41iX37eRXY9mpcWdmpefbIZ8DbbYBXkxIdwvbpWZ7Md/Vmh5VjGgCENI
JsPReFpbYLJShM9RkVyGAgYXlv71s1Mf2vpVRDhvG52JAgjTBKf9veYRCtadN/Um
ap58tKixwZ/cY/qlTvMCgYBFbSi7QYGdad2CRf6LqzcEUNO0lNVnjB63b++3vWKs
zDiYj6WSmbTmHFj8R5fIhvBD3YV9lEHA+f53PtW9KnS36OBXeg+jx/SKbIJGrVzX
cqtfqqfQ+bOPmACPHdBD8SWvfNLNayxQ7Z0J9Wg4QZOy7KO6yhCqG50cd/8vE5rB
YwKBgQCH9mHpdfORUCXVt1QScw29mhLskx5SA/9vU4lrKpwr0Kkce+d0Cex14jWG
cLz1fOlcctHsIQBMFxEBR0dM7RNX/kdvWfhiPDl1VgDQIyrAEC9euig92hKhmA2E
Myw1d5t46XP97y6Szrhcsrt15pmSKD+zLYXD26qoxKJOP9a6+A==
-----END RSA PRIVATE KEY-----
"""

    @staticmethod
    def accept_client(client, addr, root_dir, users, host_rsa_key, password):
        usermap = {}
        for user in users:
            usermap[user.username] = user

        host_key_file = StringIO(host_rsa_key)
        host_key = paramiko.RSAKey(file_obj=host_key_file)
        transport = paramiko.Transport(client)
        transport.load_server_moduli()
        transport.add_server_key(host_key)

        impl = sftp_classes.SimpleSftpServer
        transport.set_subsystem_handler("sftp", paramiko.SFTPServer, sftp_si=impl, transport=transport,
                                        fs_root=root_dir, users=usermap)

        server = sftp_classes.SimpleSSHServer(users=usermap)
        transport.start_server(server=server)
        channel = transport.accept()
        while transport.is_active():
            time.sleep(3)

        username = server.get_authenticated_user()
        if username is not None:
            user = usermap[username]
            os.system("svn commit -m 'committing user session for %s' %s" % (username, root_dir + "/" + user.home))
        return

    def serve(self):
        loot_path = os.path.join(helpers.ea_path(), 'transfer') + "/"
        # Check to make sure the agent directory exists, and a loot
        # directory for the agent. If not, make them
        if not os.path.isdir(loot_path):
            os.makedirs(loot_path)

        user_map = [sftp_classes.User(username=self.username, password=self.password, chroot=False), ]

        print(f'[*] Starting an SFTP server on port {self.port}.')

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen(10)
        except socket.error:
            print(f'[*] Error: Port {self.port} is currently in use.')
            sys.exit()

        print(f'[*] Starting an SFTP server on port {self.port}.')


        while True:
            try:
                client, addr = server_socket.accept()
                t = threading.Thread(target=self.accept_client, args=[
                    client, addr, self.sftp_directory, user_map,
                    self.rsa_key, self.password])
                t.daemon = True
                t.start()
            except KeyboardInterrupt:
                print('[*] Shutting down the SFTP server.')
                sys.exit()

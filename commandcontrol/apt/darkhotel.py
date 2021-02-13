"""

This module generates darkhotel traffic.

Resources:
https://securelist.com/blog/research/66779/the-darkhotel-apt/

"""

import random
import sys
import urllib.error
import urllib.parse
import urllib.request


class Actor:

    def __init__(self, cli_object):
        self.cli = "darkhotel"
        self.description = "darkhotel backdoor"
        self.type = "malware"
        self.server_requirement = "http"
        self.egress_server = cli_object.ip
        self.domains = [
            'micronaoko.jumpingcrab.com', 'microchsse.strangled.net',
            'microbrownys.strangled.net', 'microplants.strangled.net',
            'microlilics.crabdance.com']
        self.uris = [
            '/bin/read_i.php?a1=step2-down-b&a2=KJNSDFkjmdfH&a3=SW5mb1N5c0BVc2VyIE1ZQ09NUFVURVJATXlVc2VyICgwODUwKUMgUCBVIDogSW50ZWwoUikgQ29yZShUTSkgaTMtMTY2N1UgQ1BVIEAgMTYwMEdIelN5c3RlbSBPUzogTWljcm9zb2Z0IFdpbmRvd3MgWFAgKFNlcnZpY2UgUGFjayAzKU5ldCBjYXJkIDogMTkyLjE2OC4wLjIgKDEzMzc3MzMxMTMzNyk=&a4=KS',
            '/bin/read_i.php?a1=step2-down-r&a2=KDYEMDYWM&a3=SW5mb1N5c0BVc2VyIE1ZQ09NUFVURVJATXlVc2VyICgwODUwKUMgUCBVIDogSW50ZWwoUikgQ29yZShUTSkgaTctMTY2N1UgQ1BVIEAgMTYwMEdIelN5c3RlbSBPUzogTWljcm9zb2Z0IFdpbmRvd3MgNyAoU2VydmljZSBQYWNrIDIpTmV0IGNhcmQgOiAxOTIuMTY4LjI1LjIgKDEzMzc3MzMxMTMzNyk=&a4=TR',
            '/bin/read_i.php?a1=step2-down-u&a2=YEMDGEJEIMD&a3=SW5mb1N5c0BVc2VyIFdvcmtzdGF0aW9uQFNvbm9mRmx5bm4gKDA4NTApQyBQIFUgOiBJbnRlbChSKSBDb3JlKFRNKSBpNy0xNTBVIENQVSBAIDE2MDBHSHpTeXN0ZW0gT1M6IE1pY3Jvc29mdCBXaW5kb3dzIDguMSAoU2VydmljZSBQYWNrIDEpTmV0IGNhcmQgOiAxOTIuMTY4LjMzLjIgKDEzMzc3MzMxMTMzNyk=&a4=BD',
            '/bin/read_i.php?a1=step2-down-c&a2=MSNETJ&a3=SW5mb1N5c0BVc2VyIFNFUlZFUkRDQEFETUlOICgwODUwKUMgUCBVIDogSW50ZWwoUikgQ29yZShUTSkgaTctOTBVIENQVSBAIDIwMDBHSHpTeXN0ZW0gT1M6IE1pY3Jvc29mdCBXaW5kb3dzIDEwIE5ldCBjYXJkIDogMTkyLjE2OC4xMzMuMiAoMTMzNzczMzExMzM3KQ==&a4=AST',
            '/bin/read_i.php?a1=step2-down-k&a2=VSEJKNEF&a3=SW5mb1N5c0BVc2VyIERCQURCQFNZU0RCQSAoMDg1MClDUFUgOiBJbnRlbChSKSBDb3JlKFRNKSBpNy05MCBDUFUgQCAzMjAwR0h6U3lzdGVtIE9TOiBNaWNyb3NvZnQgV2luZG93cyBTZXJ2ZXIgMjAwMyBOZXQgY2FyZCA6IDE5Mi4xNjguMTUzLjIgKDEzMzc3MzMxMTMzNyk=&a4=NOD'
            '/bin/read_i.php?a1=step2-down-j&a2=ALFDOEJNKF&a3=SW5mb1N5c0BVc2VyIERBZG1pbkBEQ1N5cyAoMDk1MClDUFUgOiBJbnRlbChSKSBDb3JlKFRNKSBpNy05MDAgQ1BVIEAgMzgwMUdIelN5c3RlbSBPUzogTWljcm9zb2Z0IFdpbmRvd3MgU2VydmVyIDIwMDggTmV0IGNhcmQgOiAxOTIuMTY4LjE5My4yICgxMzM3NzMzMTEzMzcp&a4=NV']
        self.checkin_domains = [
            'autolace.twilightparadox.com', 'automachine.servequake.com']

    def emulate(self, data_to_exfil=None):

        # headers that are used in get requests
        darkhotel_headers = {
            "User-Agent": " Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache",
        }

        selected_checkin_domain = random.choice(self.checkin_domains)
        darkhotel_headers['Host'] = selected_checkin_domain

        get_request = urllib.request.Request(
            "http://" + self.egress_server + "/major/images/view.php",
            headers=darkhotel_headers)

        try:
            urllib.request.urlopen(get_request)
        except urllib.error.URLError:
            print("[*] Error: Cannot connect to darkhotel data exfil server!")
            print("[*] Error: Possible firewall, or proxy prventing this?")
            sys.exit(1)

        get_request2 = urllib.request.Request(
            "http://" + self.egress_server + "/major/txt/read.php",
            headers=darkhotel_headers)

        try:
            urllib.request.urlopen(get_request2)
        except urllib.error.URLError:
            print('[*] Error: Cannot connect to darkhotel data exfil server!')
            print('[*] Error: Possible firewall, or proxy prventing this?')
            sys.exit(1)

        # Iterate over get and post request 5 times
        for times_requested in range(1, 6):
            selected_domain = random.choice(self.domains)
            darkhotel_headers['Host'] = selected_domain
            darkhotel_uri = random.choice(self.uris)

            get_req2 = urllib.request.Request(
                "http://" + self.egress_server + darkhotel_uri, headers=darkhotel_headers)

            try:
                urllib.request.urlopen(get_req2)
            except urllib.error.URLError:
                print('[*] Error: Cannot connect to darkhotel data exfil server!')
                print('[*] Error: Possible firewall, or proxy prventing this?')
                print(f'URI == {darkhotel_uri}')

        print("[*] INFO: DarkHotel C2 comms complete!")
        return

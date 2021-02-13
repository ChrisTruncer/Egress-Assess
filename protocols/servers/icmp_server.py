import base64
import time
from scapy.layers.inet import ICMP
from common import helpers
from scapy.all import *


class Server:

    def __init__(self, cli_object):
        self.protocol = 'icmp'
        self.file_name = ''
        self.last_packet = ''
        self.loot_path = ''

    def custom_action(self, packet):
        if packet.haslayer(ICMP):
            if packet.haslayer(Raw):
                icmp_strings = repr(packet[Raw])
                try:
                    incoming_data = base64.b64decode(icmp_strings.split('\'')[1])
                    if incoming_data == self.last_packet:
                        pass
                    else:
                        if b".:::-989-:::." in incoming_data:
                            file_name = incoming_data.split(b".:::-989-:::.")[0].decode('utf-8')
                            file_data = incoming_data.split(b".:::-989-:::.")[1].decode('utf-8')
                            helpers.received_file(file_name)
                            with open(self.loot_path + file_name, 'a') as icmp_out:
                                icmp_out.write(file_data)
                            self.last_packet = incoming_data
                        else:
                            helpers.received_file(self.file_name)
                            with open(self.loot_path + self.file_name, 'a') as icmp_out:
                                icmp_out.write(incoming_data)
                            self.last_packet = incoming_data
                except TypeError:
                    pass
                except IndexError:
                    pass
        return

    def serve(self):
        self.loot_path = os.path.join(helpers.ea_path(), 'transfer') + '/'
        # Check to make sure the agent directory exists, and a loot
        # directory for the agent. If not, make them
        if not os.path.isdir(self.loot_path):
            os.makedirs(self.loot_path)

        # Get the date info
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        self.file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "text_data.txt"

        print('[*] Starting an ICMP server/sniffer.')
        sniff(prn=self.custom_action)

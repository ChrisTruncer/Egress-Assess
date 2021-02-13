"""

This is the template that should be used for client modules.
A brief description of the client module can/should be placed
up here.  All necessary imports should be placed between the
comments and class declaration.

Finally, be sure to rename your client module to a .py file

"""

import base64
import re
import socket
import sys

from scapy.layers.inet import IP, ICMP
from common import helpers
from scapy.all import *


class Client:

    def __init__(self, cli_object):
        self.protocol = "icmp"
        self.length = 1050   # Number of cleartext characters allowed before b64 encoded
        self.remote_server = cli_object.ip
        if cli_object.file is None:
            self.file_transfer = False
        else:
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        byte_reader = 0
        packet_number = 1

        # Determine if sending via IP or domain name
        if helpers.validate_ip(self.remote_server):
            final_destination = self.remote_server
        else:
            print('[*] Resolving IP of domain...')
            final_destination = socket.gethostbyname(self.remote_server)

        # calcalate total packets
        if (len(data_to_transmit) % self.length) == 0:
            total_packets = len(data_to_transmit) / self.length
        else:
            total_packets = (len(data_to_transmit) / self.length) + 1
        self.current_total = total_packets

        while byte_reader < len(data_to_transmit):
            if not self.file_transfer:
                encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + self.length])
            else:
                encoded_data = base64.b64encode(self.file_transfer +
                                                ".:::-989-:::." + data_to_transmit[byte_reader:byte_reader + self.length])

            print('[*] Packet Number/Total Packets:        ' + str(packet_number) + "/" + str(total_packets))

            # Craft the packet with scapy
            try:
                send(IP(dst=final_destination) / ICMP() / encoded_data, verbose=False)
            except KeyboardInterrupt:
                print('[*] Shutting down...')
                sys.exit()

            # Increment counters
            byte_reader += self.length
            packet_number += 1

"""
Author: @butlerallenj
Contributors: @khr0x40sh, @ruddawg26

This is an improved version of the DNS Server module. Using DNSLib, this module can listen and
respond to requests from both TXT and A records, decode the requests utilizing the correct format,
and write the output to a file:

    FORMATS
    -------

    A:
        <base64encoded filedata `=` => `.---`>.<base64encoded filename>.<fqdn>
    TXT:
        ! Supports Stacked Queries
        <base64encoded <<4Byte:int32 file_status><preamble><filedata>>.

"""

import time
import struct
import socketserver
import threading
import sys
import datetime
from dnslib import *
from common import helpers

# NOTE from @butlerallenj
# I REALLY hate using globals, unfortunately I am not aware of a better
# solution at this time. The problem that globals fix in this situation
# is that a dictionary is required to maintain the state of the DNS file data
# before writing it to a file. The state cannot be maintained in the class
# BaseRequestHandler, because it is run for every request
#
# A couple of things that may be able to solve this problem:
# 1. A way to pass a method from class Server to the class BaseRequestHandler
#    which can set/retrieve the attributes of the Server class from the BaseRequestHandler
# 2. Writing a custom SocketServer class that has additional attributes to maintain the state
#    of the FILE_DICT
# 3. Maintain the GLOBAL variables
#
# I would prefer #1 if possible, I am unaware of how to do this currently though.

LOOT_PATH = os.path.join(helpers.ea_path(), 'transfer') + "/"
FILE_DICT = {}
FILE_NAME = ""
FILE_STATUS = "0"
LAST_PACKET = ""


def set_file_name():
    global FILE_NAME

    current_date = time.strftime("%m/%d/%Y")
    current_time = time.strftime("%H:%M:%S")

    FILE_NAME = current_date.replace("/", "") + "_" + current_time.replace(":", "") + "text_data.txt"


class Server:
    def __init__(self, cli_object):
        self.protocol = 'dns'
        self.servers = []
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 53

    def start_dns_servers(self):
        self.servers = [
            socketserver.ThreadingUDPServer(('', self.port), UDPRequestHandler),
        ]
        for server in self.servers:
            # That thread will start one more thread for each request
            thread = threading.Thread(target=server.serve_forever)
            # Exit the server thread when the main thread terminates
            thread.daemon = True
            thread.start()
            print(f'{server.RequestHandlerClass.__name__[:3]} server loop running in thread: {thread.name}')

    def serve(self):
        print(f'[*] Starting a DNS server on UDP port {self.port}.')

        set_file_name()

        if not os.path.isdir(LOOT_PATH):
            os.makedirs(LOOT_PATH)

        self.start_dns_servers()
        
        try:
            while 1:
                time.sleep(0.5)
                sys.stderr.flush()
                sys.stdout.flush()

        except KeyboardInterrupt:
            pass

        finally:
            for server in self.servers:
                server.shutdown()

        return


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, *kargs):
        self.preamble = ".:|:."
        self.ENDFILESTRING = "ENDTHISFILETRANSMISSIONEGRESSASSESS"

        socketserver.BaseRequestHandler.__init__(self, *kargs)

    @staticmethod
    def clear_globals():
        global FILE_DICT, FILE_NAME, LAST_PACKET
        FILE_DICT = {}
        FILE_STATUS = "0"
        LAST_PACKET = ""
        set_file_name()

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        client = self.client_address[0]

        try:
            data = self.get_data()
            self.send_data(self.handle_dns_request(data, client))
        except Exception:
            pass

    @staticmethod
    def decode_file_status(encoded):
        return str(struct.unpack(">I", encoded)[0])

    def write_file(self, file_name, write_mode='w', data=None):
        global LOOT_PATH, FILE_DICT, FILE_STATUS

        if data:
            with open(LOOT_PATH + file_name, write_mode) as f:
                f.write(data)
        else:
            helpers.received_file(file_name)
            missing_keys = []
            write_dict = FILE_DICT
            if len(write_dict.keys()) < 2:
                return

            with open(LOOT_PATH + file_name, write_mode) as f:
                for dict_key in range(1, int(FILE_STATUS) + 1):
                    try:
                        content = write_dict[str(dict_key)]
                        f.write(content)
                    except Exception:
                        missing_keys.append(dict_key)

            if len(missing_keys):
                print('[-] ERROR: The following keys were missing from FILE_DICT!\n{}'.format(', '.join(missing_keys)))

            self.clear_globals()

        return

    @staticmethod
    def upload_feedback(message=""):
        global FILE_STATUS

        sys.stdout.write(f'[*] {message} Transfer initiated: {FILE_STATUS}\r')
        sys.stdout.flush()

    def handle_dns_txt(self, encoded_qname):
        global FILE_DICT, FILE_STATUS

        try:
            if self.ENDFILESTRING in encoded_qname:
                file_name = encoded_qname.split(self.ENDFILESTRING)[1].rstrip('.')
                self.write_file(file_name)
                return

            decoded = base64.b64decode(encoded_qname)

            if self.preamble not in decoded:
                self.write_file(FILE_NAME, 'a', data=decoded)
                return

            parts = decoded.split(self.preamble)
            FILE_STATUS = self.decode_file_status(parts[0])
            file_data = parts[1]

            if FILE_STATUS not in FILE_DICT:
                FILE_DICT[FILE_STATUS] = file_data
                self.upload_feedback()

        except Exception as e:
            print(f'[-] handle_dns_txt Error: {e} {encoded_qname}')

        return

    def handle_dns_resolved(self, encoded_qname):
        global FILE_DICT, FILE_NAME, LAST_PACKET, FILE_STATUS

        try:
            seperator = '.---'
            if seperator in encoded_qname:
                encoded_qname = encoded_qname.replace(seperator, '=')

            parts = encoded_qname.split('.')

            if self.ENDFILESTRING == parts[0]:
                file_name = base64.b64decode(parts[1])
                self.write_file(file_name)
                return

            data = base64.b64decode(parts[0])

            if self.preamble in data:
                try:
                    data_parts = data.split(self.preamble)

                    FILE_STATUS = self.decode_file_status(data_parts[0])
                    file_data = data_parts[1]

                    FILE_DICT[FILE_STATUS] = file_data
                    self.upload_feedback()
                except Exception as e:
                    print(f'[-] Error handle_dns_resolved: {e} {data}')
            else:
                # The request is not a file upload, write directly to the file in append mode

                self.write_file(FILE_NAME, 'a', data=data)
                return
        except Exception as e:
            print(f'[-] handle_dns_resolved Error: {e} {encoded_qname}')

        return

    def handle_dns_request(self, data, client):
        # The following code has been modified from @khr0x40sh's Galvatron by @butlerallenj
        # https://github.com/khr0x40sh/Galvatron/blob/master/servers/DNS/dns_serv.py
        request = DNSRecord.parse(data)
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
        try:

            qtype = QTYPE[request.q.qtype]

            for question in request.questions:
                qname = str(question.qname)
                if qtype == 'TXT':
                    self.handle_dns_txt(qname)
                if qtype == 'A':
                    self.handle_dns_resolved(qname)

        except Exception:
            pass

        return reply.pack()


class UDPRequestHandler(BaseRequestHandler):
    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)

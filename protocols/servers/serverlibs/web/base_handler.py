import os
import random
import time
from http.server import BaseHTTPRequestHandler
from common import helpers
from commandcontrol.apt import *
from commandcontrol.malware import *
from protocols.servers.serverlibs.web import malware_callbacks


class GetHandler(BaseHTTPRequestHandler):
    # Some of the http server code came from Dave Kennedy's AES shell
    # over http - the server specific code

    # should be performing GET requests Help from
    # http://pymotw.com/2/BaseHTTPServer/
    def do_GET(self):
        if self.path in malware_callbacks.malware_uris:
            self.send_response(200)
            self.end_headers()

        elif self.path == malware_callbacks.etumbot_checkin:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(malware_callbacks.etumbot_checkin_response)

        elif (self.path.startswith(malware_callbacks.etumbot_uri) or self.path.startswith(malware_callbacks.etumbot_uri2)) \
                and (self.path.endswith(malware_callbacks.etumbot_extensions) or self.path.endswith(malware_callbacks.etumbot_extensions2)) \
                or self.path.startswith(malware_callbacks.etumbot_uri3) \
                or self.path.startswith(malware_callbacks.etumbot_uri4) or self.path.startswith(malware_callbacks.etumbot_uri5):
            # current directory
            exfil_directory = os.path.join(helpers.ea_path(), 'transfer')
            loot_path = exfil_directory + '/'
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)
            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") + "_" + current_time.replace(":", "") + "actor_data.txt"

            with open(loot_path + screenshot_name, 'a') as cc_data_file:
                cc_data_file.write('METADATA: From: ' + str(self.client_address) + ' ' + str(self.address_string) + '\n\n')
                cc_data_file.write('etumbot just checked in here!\n')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(random.choice(malware_callbacks.encoded_response))

        elif self.path == malware_callbacks.darkhotel_checkin:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'DEXT8726.168.15.192')

        elif self.path == malware_callbacks.darkhotel_checkin2:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'DEXT87no')

        elif self.path.startswith(malware_callbacks.darkhotel_uri):
            exfil_directory = os.path.join(helpers.ea_path(), 'transfer')
            loot_path = exfil_directory + "/"
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)
            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") + "_" + current_time.replace(":", "") + "actor_data.txt"

            with open(loot_path + screenshot_name, 'a') as cc_data_file:
                cc_data_file.write('METADATA: From: ' + str(self.client_address) + ' ' + str(self.address_string) + '\n\n')
                cc_data_file.write('DarkHotel just checked in here!\n')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'DKCheckin good')

        else:
            # 404 since we aren't serving up any pages, only receiving data
            self.send_response(404)
            self.end_headers()
        return

    # handle post request
    def do_POST(self):

        # current directory
        exfil_directory = os.path.join(helpers.ea_path(), 'transfer')
        loot_path = exfil_directory + '/'

        # Info for this from -
        # http://stackoverflow.com/questions/13146064/simple-
        # python-webserver-to-save-file
        if self.path == "/post_data.php":

            self.send_response(200)
            self.end_headers()

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") + "_" + current_time.replace(":", "") + "web_data.txt"

            # Read the length of the file being uploaded
            screen_length = self.headers['content-length']
            screen_data = self.rfile.read(int(screen_length))

            # Write out the file
            with open(loot_path + screenshot_name, 'a') as cc_data_file:
                cc_data_file.write('METADATA: From: ' + str(self.client_address) + ' ' + str(self.address_string) + '\n\n')
                cc_data_file.write(str(screen_data))

        elif self.path == "/post_file.php":
            self.send_response(200)
            self.end_headers()

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            # Read the length of the file being uploaded
            screen_length = self.headers['content-length']
            screen_data = self.rfile.read(int(screen_length))

            file_name = screen_data.split(b".:::-989-:::.")[0].decode('utf-8')
            file_data = screen_data.split(b".:::-989-:::.")[1].decode('utf-8')

            with open(loot_path + file_name, 'wb') as cc_data_file:
                helpers.received_file(file_name)
                cc_data_file.write(bytes(file_data, encoding='utf-8'))

        elif self.path == "/posh_file.php":
            self.send_response(200)
            self.end_headers()

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)
            # Read the length of the file being uploaded
            length = self.headers['content-length']
            filename = self.headers['Filename']
            data = self.rfile.read(int(length))

            with open(loot_path + filename, 'wb') as cc_data_file:
                cc_data_file.write(data)

        elif (self.path in malware_callbacks.malware_uris) or (self.path.startswith(other_uri) for other_uri in malware_callbacks.other_apt_uris):

            self.send_response(200)
            self.end_headers()

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") + "_" + current_time.replace(":", "") + "actor_data.txt"

            # Read the length of the screenshot file being uploaded
            screen_length = self.headers['content-length']
            screen_data = self.rfile.read(int(screen_length))

            # Write out the file
            with open(loot_path + screenshot_name, 'a') as cc_data_file:
                cc_data_file.write('METADATA: From: ' + str(self.client_address) + ' ' + str(self.address_string) + '\n\n')
                cc_data_file.write(str(screen_data))

        # All other Post requests
        else:
            self.send_response(404)
            self.end_headers()

            print('Odd... someone else is trying to access this web server...')
            print('Might want to check that out...')

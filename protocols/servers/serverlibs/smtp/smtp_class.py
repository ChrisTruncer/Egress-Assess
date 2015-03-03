# Code from http://pymotw.com/2/smtpd/
# Code from https://github.com/trentrichardson/Python-Email-Dissector/blob/master/EDHelpers/EDServer.py

import base64
import email
from email.parser import Parser
import smtpd
import time
from common import helpers


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):

        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)

        loot_directory = helpers.ea_path() + '/data'

        p = Parser()
        msgobj = p.parsestr(data)
        for part in msgobj.walk():
            attachment = self.email_parse_attachment(part)
            if attachment is None:
                current_date = time.strftime("%m/%d/%Y")
                current_time = time.strftime("%H:%M:%S")
                file_name = current_date.replace("/", "") +\
                    "_" + current_time.replace(":", "") + "email_data.txt"

                with open(loot_directory + "/" + file_name, 'w') as email_file:
                    email_file.write(data)
            else:
                if attachment:
                    decoded_file_data = base64.b64decode(attachment['filedata'])
                    attach_file_name = attachment['filename']
                    with open(loot_directory + "/" + attach_file_name, 'wb') as attached_file:
                        attached_file.write(decoded_file_data)
                elif part.get_content_type() == "text/plain":
                    body_text += unicode(part.get_payload(decode=True),part.get_content_charset(),'replace').encode('utf8','replace')
                elif part.get_content_type() == "text/html":
                    body_html += unicode(part.get_payload(decode=True),part.get_content_charset(),'replace').encode('utf8','replace')
                
        return

    def email_parse_attachment(self, message_part):

        content_disposition = message_part.get("Content-Disposition", None)
        if content_disposition:
            dispositions = content_disposition.strip().split(";")
            if bool(content_disposition and dispositions[0].lower() == "attachment"):
                attachment = {
                        'filedata': message_part.get_payload(),
                        'content_type': message_part.get_content_type(),
                        'filename': "default"
                    }
                for param in dispositions[1:]:
                    name,value = param.split("=")
                    name = name.strip().lower()

                    if name == "filename":
                        attachment['filename'] = value.replace('"','')

                return attachment

        return None
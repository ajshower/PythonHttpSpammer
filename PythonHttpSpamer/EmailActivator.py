import sys
import imaplib
import getpass
import email
import email.header
import datetime

import quopri
from bs4 import BeautifulSoup

from termcolor import colored
from colorama import init

EMAIL_ACCOUNT = "xoxo@gmail.com"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.  
    For the sake of this example, print some headers.
    """

    #rv, data = M.search(None, "ALL")
    rv, data = M.search(None, "SUBJECT", "Rejestracja")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", num)
            return

        msg = email.message_from_bytes(data[0][1])

        #body = msg.get_payload()[0].get_payload()
        #print(body)   

        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        print('Message %s: %s' % (num, colored(subject, "yellow")))
        print('Raw Date:', msg['Date'])

        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype in ["text/plain", "text/html"]:
                    if part['Content-Transfer-Encoding'] in ["quoted-printable"]:
                        tmp = quopri.decodestring(part.get_payload())
                        print(tmp.decode(sys.stdout.encoding))
                    else:
                        print(part.get_payload())
                    
        else:
            body = msg.get_payload(decode=True)
            soup = BeautifulSoup(body, "html.parser")
            wynik = soup.select("a")[3]["href"]
            print(wynik)



        # Now convert to local date-time
        """date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print ("Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S"))"""


# use Colorama to make Termcolor work on Windows
init()

M = imaplib.IMAP4_SSL('imap.gmail.com')
# getpass.getpass()
try:
    rv, data = M.login(EMAIL_ACCOUNT, "xoxo")
except imaplib.IMAP4.error:
    print ("LOGIN FAILED!!! ")
    sys.exit(1)

print(rv, data)

rv, mailboxes = M.list()
if rv == 'OK':
    print("Mailboxes:")
    print(mailboxes)

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print("Processing mailbox...\n")
    process_mailbox(M)
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

M.logout()
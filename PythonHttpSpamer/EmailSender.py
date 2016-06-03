import sys
import smtplib
import getpass
import email
import email.header
import datetime

from queue import Queue
from threading import Thread

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

num_threads = 4
jobsQueue = Queue()
resultQueue = Queue()
startIndex = 1
stopIndex = 50

emailLogin = 'znajomy23@gmail.com'
emailPassword = 'gustaw32'
emailFrom = 'twoja@stara.com'
emailTo = 'urbanek32@gmail.com'

templateSubject = 'Eloszka'

def conntectToMailbox():
    #global smtpClient
    #print("Connecting to SMTP...")

    smtpClient = smtplib.SMTP('smtp.gmail.com', 587)
    out = smtpClient.ehlo()
    if out[0] != 250:
        print(out)
        return

    out = smtpClient.starttls()
    if out[0] != 220:
        print(out)
        return

    out = smtpClient.login(emailLogin, emailPassword)
    if out[0] != 235:
        print(out)
        return

    #print("Connected successful")
    return smtpClient

def sendEmail(toAddress, subject):
    #global smtpClient
    smtpClient = conntectToMailbox()
    #print("Preparing email to {}...".format(toAddress))

    msg = MIMEMultipart()
    msg['From'] = emailFrom
    msg['To'] = toAddress
    msg['Subject'] = subject

    body = "To jest moj super tekst z fajną zawartością"
    try:
        msg.attach(MIMEText(body, 'plain'))
        message = msg.as_string()
        out = smtpClient.sendmail(emailFrom, toAddress, message)
        if len(out) != 0:
            return out
        else:
            return 'Email send successfully'
    except:
        print("Erroro", sys.exc_info())
        return sys.exc_info()


def sendEmailWorker(index, jobsQueue, resultQueue):
    while True:
        subject = jobsQueue.get()
        print("[%s]" % (index + 1))
        out = sendEmail(emailTo, subject)
        if out in ['successfully']:
            resultQueue.put(subject)
        else:
            resultQueue.put(out)
        jobsQueue.task_done()

def main(args):
    #conntectToMailbox()
    #for i in range(startIndex, stopIndex):
    #    sendEmail(emailTo, "Eloszka {}".format(i+1))



    print("*** Launching workers")
    for i in range(num_threads):
        worker = Thread(target=sendEmailWorker, args=(i, jobsQueue, resultQueue,))
        worker.setDaemon(True)
        worker.start()

    print("*** Feeding queue with subjects")
    for i in range(startIndex, stopIndex):
        val = templateSubject #+ str(i)
        jobsQueue.put(val)

    print("*** Working...\n")
    jobsQueue.join()

    if resultQueue.empty():
        print("No emails sent :(")
    else:
        amount = 0
        while not resultQueue.empty():
            resultQueue.get()
            amount += 1
        print("*** Number of sent emails: {}".format(amount))

    print("*** Done")
    input()

if __name__ == "__main__":
    sys.exit(int(main(sys.argv[1:]) or 0))
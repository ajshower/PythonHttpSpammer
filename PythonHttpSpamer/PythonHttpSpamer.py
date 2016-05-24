import sys
import argparse
import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread

# set up some global variables
newAccountNameTemplate = "tester-"
num_threads = 4
jobsQueue = Queue()
resultQueue = Queue()
startIndex = 1
stopIndex = 10

def parseArgs(argv):
    # WIP
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int)
    parser.add_argument("--stop", type=int)
    args = parser.parse_args()


def post_request(username):
    payload = {
        "allcountries": "0",
        "username": username,
        "email": "xoxo+"+username+"@gmail.com",
        "password1": "1234",
        "password2": "1234",
        "TOS": "ON",
        "submit": "Zarejestruj się"
    }
    r = requests.post("http://opencaching.pl/register.php", data=payload)
    soup = BeautifulSoup(r.text, "html.parser")
    wynik = soup.select(".content2-pagetitle")[0].text
    return wynik

def createAccount(i, q, r):
    while True:
        username = q.get()
        print("[%s]" % (i+1))
        wynik = post_request(username)
        if "Nowy użytkownik" in wynik:
            r.put(username)
        q.task_done()

def main(argv):
    #parseArgs(argv)
    #input("Press RETURN to continue...")

    print("*** Launching workers")
    for i in range(num_threads):
        worker = Thread(target=createAccount, args=(i, jobsQueue, resultQueue,))
        worker.setDaemon(True)
        worker.start()

    print("*** Feeding queue with usernames")
    for i in range(startIndex, stopIndex):
        val = newAccountNameTemplate + str(i)
        jobsQueue.put(val)

    print("*** Working...\n")
    jobsQueue.join()
    
    if resultQueue.empty():
        print("No new users :(")
    else:
        print("*** List of created users")
        while not resultQueue.empty():
            print(resultQueue.get())

    print("*** Done")
    input()


if __name__ == "__main__":
    sys.exit(int(main(sys.argv[1:]) or 0))

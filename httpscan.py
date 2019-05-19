#!/usr/bin/env python
# coding:utf-8
# Author: Zeroh
# focked: thiswind

import optparse
import os
import Queue
import re
import sys
import threading

import requests
from IPy import IP
from requests import ConnectionError, ConnectTimeout, ReadTimeout

printLock = threading.Semaphore(1)  # lock Screen print
TimeOut = 5  # request timeout

# User-Agent
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
    'Connection': 'close'}


class Scan(object):

    def __init__(self, cidr, threads_num):
        self.threads_num = threads_num
        self.cidr = IP(cidr)
        # build ip queue
        self.IPs = Queue.Queue()
        for ip in self.cidr:
            ip = str(ip)
            self.IPs.put(ip)

    def request(self):
        with threading.Lock():
            while self.IPs.qsize() > 0:
                ip = self.IPs.get()
                try:
                    r = requests.Session().get(
                        'http://' + str(ip),
                        headers=header,
                        timeout=TimeOut
                    )
                    r.encoding = 'utf-8'
                    status = r.status_code
                    title = re.search(
                        r'<title>(.*)</title>',
                        r.text
                    )  # get the title
                    if title:
                        title = title.group(1).strip().strip("\r").strip("\n")[
                                :30]
                        title = title.encode('utf-8')
                    else:
                        title = "None"
                    banner = ''
                    try:
                        banner += r.headers['Server'][
                                  :20]  # get the server banner
                    except KeyError:
                        pass

                    printLock.acquire()

                    print "|%-16s|%-6s|%-20s|%-30s" % (
                        str(ip).strip(),
                        str(status).strip(),
                        str(banner).strip(),
                        str(title).strip()
                    )
                    print "+----------------+------+--------------------+------------------------------+"

                    # Save log
                    filename = "./logs/" + self.cidr.strNormal(3) + ".log"

                    with open(filename, 'a') as f:
                        f.write(ip + "\n")

                except ConnectTimeout:
                    printLock.release()
                except ConnectionError:
                    printLock.release()
                except ReadTimeout:
                    printLock.release()
                finally:
                    printLock.release()

    # Multi thread
    def run(self):

        if not os.path.exists(os.path.dirname('./logs/')):
            os.makedirs(os.path.dirname('./logs/'))

        for i in range(self.threads_num):
            t = threading.Thread(target=self.request)
            t.start()


if __name__ == "__main__":
    parser = optparse.OptionParser("Usage: %prog [options] target")
    parser.add_option(
        "-t", "--thread", dest="threads_num", default=10, type="int",
        help="[optional]number of  theads,default=10"
    )
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    print "+----------------+------+--------------------+------------------------------+"
    print "|     IP         |Status|       Server       |            Title             |"
    print "+----------------+------+--------------------+------------------------------+"

    s = Scan(cidr=args[0], threads_num=options.threads_num)
    s.run()

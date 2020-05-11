#!/usr/bin/env python3
import os
import sys
from time import time
from time import sleep
from random import choice as randchoice
from random import randrange
from random import randint
from ipaddress import IPv4Address

import zmq

CUR_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))

from config import Config


def generateBatch():
    data = []
    for i in range(Config.BATCH_SIZE):
        data.append("\t".join([
            str(time()),
            str(IPv4Address(randint(Config.MIN_IPADDRESS, Config.MAX_IPADDRESS))),
            str(randint(Config.MIN_BYTES, Config.MAX_BYTES)),
            str(randint(Config.MIN_BYTES, Config.MAX_BYTES)),
            randchoice(Config.IFACES)
        ]))
    return "\n".join(data).encode()


def main():
    cfg = Config.get("textSource")
    ctx = zmq.Context()
    socket = ctx.socket(zmq.PUSH)
    socket.connect(cfg["adapterEndpoint"])

    num = 0
    print("textSource connected to {}".format(cfg["adapterEndpoint"]))
    try:
        while True:
            socket.send(generateBatch())
            num += 1
            if num % 10 == 0:
                print("Packets sent: {}".format(num))
            sleep(1)
    finally:
        socket.close()


if __name__ == "__main__":
    main()
